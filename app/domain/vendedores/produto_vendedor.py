from uuid import uuid7

from pydantic import BaseModel
from enum import Enum
from decimal import Decimal

class StatusProduto(Enum):
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

class ProdutoVendedor(BaseModel):
    id: str
    vendedor_id: str
    produto_id: str
    preco: Decimal
    estoque: int
    status: StatusProduto
    
    @classmethod
    def criar(cls,vendedor_id: str, produto_id: str, preco: Decimal, estoque: int, status: StatusProduto) -> ProdutoVendedor:
        return cls(
            id=str(uuid7()),
            vendedor_id=vendedor_id,
            produto_id=produto_id,
            status=status,
            preco=preco,
            estoque=estoque,
        )
        
    
    def disponibilizar(self) -> None:
        self.status = StatusProduto.DISPONIVEL
    
    def esgotar(self) -> None:
        self.status = StatusProduto.ESGOTADO

    def indisponibilizar(self) -> None:
        self.status = StatusProduto.INDISPONIVEL
    
    