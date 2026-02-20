

from datetime import datetime, timedelta, timezone
from typing import Any
from weakref import ref

import bcrypt
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.domain.auth.auth_errors import CredenciaisInvalidasError, InvalidTokenError
from app.domain.auth.dto.token import TokenResponse
from app.domain.usuarios.dto.criar_usuario import CriarUsuarioDTO
from app.domain.usuarios.interfaces.usurario_repository import UsuarioRepository
from app.domain.usuarios.usuario import Usuario
from app.settings import Settings




class AuthService:
    
    def __init__(self, settings: Settings, usuario_repository: UsuarioRepository):
        self.settings = settings
        self.usuario_repository = usuario_repository
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        
    async def signup(self, dto: CriarUsuarioDTO) -> TokenResponse:
        existing_user = await self.usuario_repository.usuario_existe(dto.get("email"), dto["telefone"])
        
        if existing_user.telefone_exists:
            raise RequestValidationError(errors=[{
                "loc": ["body", "telefone"],
                "msg": "Telefone já cadastrado",
                "type": "value_error"
            }])
            
        elif existing_user.email_exists:
            raise RequestValidationError(errors=[{
                "loc": ["body", "email"],
                "msg": "Email já cadastrado",
                "type": "value_error"
            }])
            
        usuario = Usuario.criar(dto)
        
        await self.usuario_repository.save(usuario)
        
        access_token = self._create_access_token(usuario)
        refresh_token = self._create_refresh_token(usuario)
        
        return TokenResponse(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
    
    async def login(self, telefone: str, password: str) -> TokenResponse:
        usuario = await self.usuario_repository.find_by("telefone", telefone)
        
        if not usuario:
            raise CredenciaisInvalidasError()
        
        if not self.verify_password(password, usuario.password_hash):
            raise CredenciaisInvalidasError()
        
        access_token = self._create_access_token(usuario)
        refresh_token = self._create_refresh_token(usuario)
        
        return TokenResponse(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
    
    async def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        try:
            payload = jwt.decode(refresh_token, self.settings.refresh_token_secret_key, algorithms=[self.settings.algorithm])
            user_id: str | None = payload.get("sub")
            if user_id is None:
                raise InvalidTokenError()
            
            user = await self.usuario_repository.find_by_id(user_id)
            if not user:
                raise InvalidTokenError()
            
            new_access_token = self._create_access_token(user)
            new_refresh_token = self._create_refresh_token(user)
            
            return TokenResponse(access_token=new_access_token, refresh_token=new_refresh_token, token_type="bearer")
        
        except jwt.PyJWTError:
            raise InvalidTokenError()
    
    def _create_access_token(self, usuario: Usuario, expires_delta: timedelta | None = None) -> str:
        data = usuario.model_dump(mode='json',exclude={"password_hash"})
        data["sub"] = usuario.id
        
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.settings.access_token_expire_minutes)
            
        data.update({"exp": expire})
        
        encoded_jwt = jwt.encode(data, self.settings.access_token_secret_key, algorithm=self.settings.algorithm)
        
        return encoded_jwt
    
    def _create_refresh_token(self, usuario: Usuario, expires_delta: timedelta | None = None) -> str:
        data: dict[str, Any] = {"sub": usuario.id}
        
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.settings.refresh_token_expire_minutes)
            
        data["exp"] = expire
        
        encoded_jwt = jwt.encode(data, self.settings.refresh_token_secret_key, algorithm=self.settings.algorithm)
        
        return encoded_jwt
    
    async def get_current_user(self, token: str) -> Usuario | None:
        try:
            payload = jwt.decode(token, self.settings.access_token_secret_key, algorithms=[self.settings.algorithm])
            user_id: str | None = payload.get("sub")
            if user_id is None:
                raise InvalidTokenError()
            
            user = await self.usuario_repository.find_by_id(user_id)
            
            return user  # Placeholder, substitua pela lógica de busca do usuário    
        
        except jwt.PyJWTError:
            raise InvalidTokenError()
        