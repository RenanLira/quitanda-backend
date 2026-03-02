

from typing import Annotated, NotRequired, Optional, TypedDict

from pydantic import Field


class CriarVendedorDTO(TypedDict):
    usuario_id: Annotated[str, Field(description="ID do usuário associado ao vendedor", examples=["123e4567-e89b-12d3-a456-426614174000"])]
    comunidade_id: Annotated[str, Field(description="ID da comunidade associada ao vendedor", examples=["123e4567-e89b-12d3-a456-426614174000"])]
    nome_fantasia: Annotated[str, Field(description="Nome fantasia do vendedor", examples=["Quitanda do Zé"])]
    descricao: Annotated[NotRequired[Optional[str]], Field(description="Descrição do vendedor", examples=["Vendemos frutas frescas e legumes de qualidade."])]
    chave_pix: Annotated[str, Field(description="Chave pix do vendedor", examples=["12345678901234567890"])]