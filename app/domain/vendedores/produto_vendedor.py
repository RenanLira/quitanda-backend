from typing import Annotated
from uuid import uuid7

from pydantic import AfterValidator, BaseModel
from enum import Enum
from decimal import Decimal

from app.domain.vendedores.validators import produto_existe



class StatusProduto(Enum):
    DISPONIVEL = "disponivel"
    INDISPONIVEL = "indisponivel"
    ESGOTADO = "esgotado"


class ProdutoVendedor(BaseModel):
    id: str
    vendedor_id: str
    produto_id: Annotated[str, AfterValidator(produto_existe)]
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
    
    