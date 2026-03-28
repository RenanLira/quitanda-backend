


from enum import Enum
from typing import List
from pydantic import BaseModel, Field
from app.domain.comunidades.types.tipo_comunidade import TipoComunidade



class Comunidade(BaseModel):
    id: str
    nome: str
    nome_slug: str = Field(..., description="Versão do nome formatada para URLs, sem espaços e caracteres especiais")
    descricao_longa: str | None
    descricao_curta: str
    cor_tema: str = Field(default="#059669")
    tipo: TipoComunidade
    imagem_url: str | None
    ativo: bool = Field(default=False)
    