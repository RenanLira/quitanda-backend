


from enum import Enum

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