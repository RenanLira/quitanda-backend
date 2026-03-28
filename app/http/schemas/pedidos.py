from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class PedidoItemResponse(BaseModel):
    id: str
    pedido_id: str
    produto_vendedor_id: str
    quantidade: int
    preco_unitario: Decimal
    valor_total_item: Decimal


class PedidoResponse(BaseModel):
    id: str
    cliente_id: str
    vendedor_id: str
    comunidade_id: str | None
    status: str
    motivo_recusa: str | None
    valor_total: Decimal
    itens: list[PedidoItemResponse]
    criado_em: datetime
    atualizado_em: datetime
    aprovado_em: datetime | None
    recusado_em: datetime | None
