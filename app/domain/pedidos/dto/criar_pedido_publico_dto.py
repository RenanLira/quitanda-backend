from typing import Annotated, TypedDict

from pydantic import Field

from app.domain.pedidos.dto.criar_pedido_dto import CriarPedidoItemDTO


class CriarPedidoPublicoDTO(TypedDict):
    nome: Annotated[str, Field(..., min_length=2, description="Nome do cliente")]
    telefone: Annotated[str, Field(..., description="Telefone do cliente")]
    itens: Annotated[list[CriarPedidoItemDTO], Field(..., min_length=1, description="Itens do checkout")]
