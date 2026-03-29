

from pydantic import BaseModel

from app.http.schemas.usuarios import UsuarioPublicResponse


class TokenAuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class CompletarCadastroResponse(BaseModel):
    message: str = "Cadastro completo com sucesso"
    usuario: UsuarioPublicResponse