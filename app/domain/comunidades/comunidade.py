


from enum import Enum
from typing import List
from uuid import uuid7
from pydantic import BaseModel, Field
from slugify import slugify

from app.domain.comunidades.dto.criar_comunidade_dto import CriarComunidadeDTO
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
    
    @classmethod
    def criar(cls, criar_comunidade_dto: CriarComunidadeDTO) -> Comunidade:
        
        id = str(uuid7())
        nome_slug = slugify(criar_comunidade_dto["nome"])
        
        return cls(
            id=id,
            nome=criar_comunidade_dto["nome"],
            nome_slug=nome_slug,
            descricao_curta=criar_comunidade_dto["descricao_curta"],
            descricao_longa=criar_comunidade_dto["descricao_longa"],
            tipo=criar_comunidade_dto["tipo"],
            cor_tema=criar_comunidade_dto["cor_tema"],
            imagem_url=criar_comunidade_dto["imagem_url"]
        )
    