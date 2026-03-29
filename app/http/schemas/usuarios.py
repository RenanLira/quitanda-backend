from pydantic import BaseModel, EmailStr


class UsuarioPublicResponse(BaseModel):
    id: str
    nome: str
    email: EmailStr | None
    telefone: str
    tipo: str
    ativo: bool
    cadastro_completo: bool
