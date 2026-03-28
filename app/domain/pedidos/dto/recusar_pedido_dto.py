from typing import Annotated, TypedDict

from pydantic import Field


class RecusarPedidoDTO(TypedDict):
    motivo: Annotated[str, Field(..., min_length=3, description="Motivo da recusa")]
