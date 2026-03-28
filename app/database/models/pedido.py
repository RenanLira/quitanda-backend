from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from app.domain.pedidos.pedido import StatusPedido


class PedidoModel(Base):
    __tablename__ = "pedidos"

    id: Mapped[str] = mapped_column(primary_key=True)
    cliente_id: Mapped[str] = mapped_column(ForeignKey("usuarios.id"), nullable=False, index=True)
    vendedor_id: Mapped[str] = mapped_column(ForeignKey("vendedores.id"), nullable=False, index=True)
    comunidade_id: Mapped[str | None] = mapped_column(ForeignKey("comunidades.id"), nullable=True, index=True)
    status: Mapped[StatusPedido] = mapped_column(nullable=False, default=StatusPedido.PENDENTE, index=True)
    motivo_recusa: Mapped[str | None] = mapped_column(nullable=True)
    valor_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    atualizado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    aprovado_em: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    recusado_em: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    itens: Mapped[list[PedidoItemModel]] = relationship(
        back_populates="pedido",
        cascade="all, delete-orphan",
    )


class PedidoItemModel(Base):
    __tablename__ = "pedido_itens"

    id: Mapped[str] = mapped_column(primary_key=True)
    pedido_id: Mapped[str] = mapped_column(ForeignKey("pedidos.id"), nullable=False, index=True)
    produto_vendedor_id: Mapped[str] = mapped_column(ForeignKey("produtos_vendedores.id"), nullable=False, index=True)
    quantidade: Mapped[int] = mapped_column(nullable=False)
    preco_unitario: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    valor_total_item: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    pedido: Mapped[PedidoModel] = relationship(back_populates="itens")
