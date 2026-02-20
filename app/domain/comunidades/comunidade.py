


from enum import Enum
from typing import List
from pydantic import BaseModel, Field
from slugify import slugify

from app.domain.vendedores.vendedor import Vendedor

class TipoComunidade(str, Enum):
    FEIRA = "feira"
    MERCADO = "mercado"
    BAIRRO = "bairro"
    CONDOMINIO = "condominio"
    OUTRO = "outro"

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
    produtores: List[Vendedor] = []
    
    @classmethod
    def criar(cls, id: str, nome: str, descricao_curta: str, tipo: TipoComunidade, descricao_longa: str | None = None, cor_tema: str = "#059669", imagem_url: str | None = None) -> Comunidade:
        nome_slug = slugify(nome)
        
        return cls(
            id=id,
            nome=nome,
            nome_slug=nome_slug,
            descricao_curta=descricao_curta,
            descricao_longa=descricao_longa,
            tipo=tipo,
            cor_tema=cor_tema,
            imagem_url=imagem_url
        )
    