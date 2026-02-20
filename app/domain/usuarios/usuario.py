from pydantic import BaseModel, EmailStr, Field
from enum import Enum
import bcrypt
from uuid import uuid7
from app.domain.usuarios.dto.criar_usuario import CriarUsuarioDTO


class ETipoUsuario(Enum):
    ADMIN = "admin"
    CLIENTE = "cliente"
    VENDEDOR = "vendedor"


class Usuario(BaseModel):
    id: str
    nome: str
    email: EmailStr | None
    password_hash: str
    telefone: str
    tipo: ETipoUsuario
    ativo: bool = Field(default=True)
    
    
    @classmethod
    def criar(cls, dto: CriarUsuarioDTO) -> Usuario:
        hash_password = bcrypt.hashpw(dto["password"].encode('utf-8'), bcrypt.gensalt())
        
        id = str(uuid7())
        
        return cls(
            id=id,
            nome=dto["nome"],
            email=dto.get("email"),
            password_hash=hash_password.decode('utf-8'),
            telefone=dto["telefone"],
            tipo=ETipoUsuario.CLIENTE
        )
        
    def tipo_usuario(self) -> ETipoUsuario:
        return self.tipo
    
    
    