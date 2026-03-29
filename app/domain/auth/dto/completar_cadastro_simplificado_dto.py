from typing import Annotated, TypedDict

from pydantic import EmailStr, Field


class CompletarCadastroSimplificadoDTO(TypedDict):
    nome: Annotated[str, Field(..., min_length=2, description="Nome completo do cliente")]
    telefone: Annotated[str, Field(..., description="Telefone usado no pedido sem login")]
    email: Annotated[EmailStr, Field(..., description="Email para concluir o cadastro")]
    password: Annotated[str, Field(..., min_length=6, description="Senha para acesso")]
