

from typing import Annotated
import bcrypt
from fastapi import APIRouter, Body, Cookie, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.dependencies import get_auth_service
from app.domain.auth.auth_errors import InvalidTokenError, TokenNotFoundError
from app.domain.auth.auth_service import AuthService
from app.domain.usuarios.dto.criar_usuario import CriarUsuarioDTO
from app.http.cookies import Cookies



class AuthRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, prefix="/auth", tags=["auth"], **kwargs)
        
        self.registrar_rotas()
    
    def registrar_rotas(self):
        
        @self.post("/signup")
        async def signup(
            response: Response,
            body: Annotated[CriarUsuarioDTO, Body()],
            auth_service: Annotated[AuthService, Depends(get_auth_service)]
        ):
            
            
            
            result = await auth_service.signup(body)
            response.set_cookie(key="refresh_token", value=result.refresh_token, httponly=True, secure=True)
            
            return {"access_token": result.access_token, "token_type": result.token_type}
        
        @self.post("/signin")
        async def login(
            response: Response,
            form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
            auth_service: Annotated[AuthService, Depends(get_auth_service)],
        ):
            
            result = await auth_service.login(form_data.username, form_data.password)
            
            response.set_cookie(key="refresh_token", value=result.refresh_token, httponly=True, secure=True)
            
            return {"access_token": result.access_token, "token_type": result.token_type}
        
        @self.post("/refresh")
        async def refresh_token(
            cookies: Annotated[Cookies, Cookie()],
            auth_service: Annotated[AuthService, Depends(get_auth_service)],
        ):
            if not cookies.refresh_token:
                raise TokenNotFoundError()
            
            res = await auth_service.refresh_access_token(cookies.refresh_token)
            
            cookies.refresh_token = res.refresh_token
            
            return {"access_token": res.access_token, "token_type": res.token_type}
        
        @self.delete("/logout")
        async def logout(response: Response):
            response.delete_cookie(key="refresh_token")
            return {"message": "Logout bem-sucedido"}