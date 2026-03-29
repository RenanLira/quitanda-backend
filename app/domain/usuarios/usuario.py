from enum import Enum

from pydantic import BaseModel, EmailStr, Field


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
    cadastro_completo: bool = Field(default=True)




