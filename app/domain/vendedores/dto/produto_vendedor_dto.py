

from typing import TypedDict


class CriarProdutoVendedorDTO(TypedDict):
    produto_id: str
    preco: float
    estoque: int
