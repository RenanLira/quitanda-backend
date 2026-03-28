from pydantic import BaseModel
from enum import Enum
from decimal import Decimal

from app.domain.produtos.produto import Produto



class StatusProduto(Enum):
    DISPONIVEL = "disponivel"
    INDISPONIVEL = "indisponivel"
    ESGOTADO = "esgotado"


class ProdutoVendedor(BaseModel):
    id: str
    vendedor_id: str
    produto_id: str
    produto: Produto | None = None
    preco: Decimal
    estoque: int
    status: StatusProduto
    
    
    def disponibilizar(self) -> None:
        self.status = StatusProduto.DISPONIVEL
    
    def esgotar(self) -> None:
        self.status = StatusProduto.ESGOTADO

    def indisponibilizar(self) -> None:
        self.status = StatusProduto.INDISPONIVEL


class ProdutoVendedorComProdutoInfo(BaseModel):
    produto_vendedor_id: str
    vendedor_id: str
    produto_id: str
    produto_nome: str
    produto_descricao: str
    tipo_unidade: str
    preco: Decimal
    estoque: int
    status: str
    
    