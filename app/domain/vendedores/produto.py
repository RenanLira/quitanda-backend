from pydantic import BaseModel
from enum import Enum
from decimal import Decimal

class EStatusProduto(Enum):
    DISPONIVEL = "disponivel"
    INDISPONIVEL = "indisponivel"
    ESGOTADO = "esgotado"

class ETipoUnidade(Enum):
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
    vendedor_id: str
    categoria_id: str
    status: EStatusProduto
    nome: str
    descricao: str | None
    preco: Decimal
    unidade: ETipoUnidade
    imagem_url: str | None
    
    @classmethod
    def criar(cls, id: str, vendedor_id: str, categoria_id: str, status: EStatusProduto, nome: str, descricao: str | None, preco: Decimal, unidade: ETipoUnidade, imagem_url: str | None) -> Produto:
        return cls(
            id=id,
            vendedor_id=vendedor_id,
            categoria_id=categoria_id,
            status=status,
            nome=nome,
            descricao=descricao,
            preco=preco,
            unidade=unidade,
            imagem_url=imagem_url
        )
        
    
    def disponibilizar(self) -> None:
        self.status = EStatusProduto.DISPONIVEL
    
    def esgotar(self) -> None:
        self.status = EStatusProduto.ESGOTADO

    def indisponibilizar(self) -> None:
        self.status = EStatusProduto.INDISPONIVEL
    
    