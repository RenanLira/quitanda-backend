from typing import Annotated, TypedDict

from pydantic import Field


class CriarPedidoItemDTO(TypedDict):
    produto_vendedor_id: Annotated[str, Field(..., description="ID do produto_vendedor")]
    quantidade: Annotated[int, Field(..., gt=0, description="Quantidade solicitada")]


class CriarPedidosDTO(TypedDict):
    itens: Annotated[list[CriarPedidoItemDTO], Field(..., min_length=1, description="Itens do checkout")]
