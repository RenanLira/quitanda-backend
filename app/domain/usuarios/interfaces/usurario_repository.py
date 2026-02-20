from abc import ABC, abstractmethod

from pydantic import BaseModel
from app.domain.usuarios.usuario import Usuario


class EmailOrTelefoneAlreadyExistsResponse(BaseModel):
    email_exists: bool
    telefone_exists: bool

class UsuarioRepository(ABC):
    
    @abstractmethod
    async def save(self, usuario: Usuario) -> None:
        pass
    
    @abstractmethod
    async def find_by_id(self, id: str) -> Usuario | None:
        pass
    
    @abstractmethod
    async def find_by(self, by: str, value: str) -> Usuario | None:
        pass
    
    @abstractmethod
    async def usuario_existe(self, email: str | None, telefone: str) -> EmailOrTelefoneAlreadyExistsResponse:
        pass
    