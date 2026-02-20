


from enum import Enum
from uuid import uuid7

from pydantic import BaseModel


class TipoUnidade(Enum):
    KG = "kg"
    UNIDADE = "unidade"
    LITRO = "litro"
    PACOTE = "pacote"
    CAIXA = "caixa"
    MACO = "maco"
    FARDO = "fardo"
    BANDEJA = "bandeja"

class Produto(BaseModel):
    id: str
    nome: str
    descricao: str
    tipo_unidade: TipoUnidade
    
    @classmethod
    def criar(cls, nome: str, descricao: str, tipo_unidade: TipoUnidade) -> "Produto":
        
        uuid = str(uuid7())    
        
        return cls(
            id=uuid,
            nome=nome,
            descricao=descricao,
            tipo_unidade=tipo_unidade
        )