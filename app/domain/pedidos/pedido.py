
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class StatusPedido(str, Enum):
    PENDENTE = "pendente"
    APROVADO = "aprovado"
    RECUSADO = "recusado"
    ENTREGUE = "entregue"


class ProdutoVendedorPedidoInfo(BaseModel):
    produto_vendedor_id: str
    vendedor_id: str
    comunidade_id: str | None
    preco: Decimal
    estoque: int
    ativo: bool
    status_produto: str


class PedidoItem(BaseModel):
    id: str
    pedido_id: str
    produto_vendedor_id: str
    quantidade: int
    preco_unitario: Decimal
    valor_total_item: Decimal


class Pedido(BaseModel):
    id: str
    cliente_id: str
    vendedor_id: str
    comunidade_id: str | None
    status: StatusPedido = Field(default=StatusPedido.PENDENTE)
    motivo_recusa: str | None = None
    valor_total: Decimal
    itens: list[PedidoItem] = Field(default_factory=list)
    criado_em: datetime
    atualizado_em: datetime
    aprovado_em: datetime | None = None
    recusado_em: datetime | None = None

    def aprovar(self) -> None:
        agora = datetime.now(timezone.utc)
        self.status = StatusPedido.APROVADO
        self.aprovado_em = agora
        self.atualizado_em = agora

    def recusar(self, motivo: str) -> None:
        agora = datetime.now(timezone.utc)
        self.status = StatusPedido.RECUSADO
        self.motivo_recusa = motivo
        self.recusado_em = agora
        self.atualizado_em = agora