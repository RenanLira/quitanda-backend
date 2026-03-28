from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.comunidade import ProdutoVendedorModel, VendedorModel
from app.database.models.pedido import PedidoItemModel, PedidoModel
from app.domain.pedidos.interfaces.pedido_repository import PedidoRepository
from app.domain.pedidos.pedido import Pedido, ProdutoVendedorPedidoInfo


class PedidoRepositoryImpl(PedidoRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_many(self, pedidos: list[Pedido]) -> None:
        for pedido in pedidos:
            pedido_model = PedidoModel(**pedido.model_dump(exclude={"itens"}, mode="python"))
            pedido_model.itens = [
                PedidoItemModel(**item.model_dump(mode="python")) for item in pedido.itens
            ]
            self.session.add(pedido_model)

        await self.session.commit()

    async def find_by_id(self, pedido_id: str) -> Pedido | None:
        result = await self.session.execute(
            select(PedidoModel)
            .where(PedidoModel.id == pedido_id)
            .options(joinedload(PedidoModel.itens))
        )
        pedido_model = result.unique().scalars().first()
        if not pedido_model:
            return None
        return Pedido.model_validate(pedido_model, from_attributes=True)

    async def find_by_cliente_id(self, cliente_id: str) -> list[Pedido]:
        result = await self.session.execute(
            select(PedidoModel)
            .where(PedidoModel.cliente_id == cliente_id)
            .options(joinedload(PedidoModel.itens))
        )
        return self._to_domain_list(result.unique().scalars().all())

    async def find_by_vendedor_id(self, vendedor_id: str) -> list[Pedido]:
        result = await self.session.execute(
            select(PedidoModel)
            .where(PedidoModel.vendedor_id == vendedor_id)
            .options(joinedload(PedidoModel.itens))
        )
        return self._to_domain_list(result.unique().scalars().all())

    async def find_all(self) -> list[Pedido]:
        result = await self.session.execute(select(PedidoModel).options(joinedload(PedidoModel.itens)))
        return self._to_domain_list(result.unique().scalars().all())

    async def update(self, pedido: Pedido) -> None:
        pedido_model = await self.session.get(PedidoModel, pedido.id)
        if not pedido_model:
            return

        pedido_model.status = pedido.status
        pedido_model.motivo_recusa = pedido.motivo_recusa
        pedido_model.valor_total = pedido.valor_total
        pedido_model.atualizado_em = pedido.atualizado_em
        pedido_model.aprovado_em = pedido.aprovado_em
        pedido_model.recusado_em = pedido.recusado_em

        await self.session.commit()

    async def get_produtos_vendedores_info(
        self,
        produto_vendedor_ids: list[str],
    ) -> list[ProdutoVendedorPedidoInfo]:
        if not produto_vendedor_ids:
            return []

        result = await self.session.execute(
            select(
                ProdutoVendedorModel.id,
                ProdutoVendedorModel.vendedor_id,
                VendedorModel.comunidade_id,
                ProdutoVendedorModel.preco,
                ProdutoVendedorModel.estoque,
                ProdutoVendedorModel.ativo,
                ProdutoVendedorModel.status,
            )
            .join(VendedorModel, VendedorModel.id == ProdutoVendedorModel.vendedor_id)
            .where(ProdutoVendedorModel.id.in_(produto_vendedor_ids))
        )

        return [
            ProdutoVendedorPedidoInfo(
                produto_vendedor_id=produto_vendedor_id,
                vendedor_id=vendedor_id,
                comunidade_id=comunidade_id,
                preco=preco,
                estoque=estoque,
                ativo=ativo,
                status_produto=status.value,
            )
            for (
                produto_vendedor_id,
                vendedor_id,
                comunidade_id,
                preco,
                estoque,
                ativo,
                status,
            ) in result.all()
        ]

    def _to_domain_list(self, models: Iterable[PedidoModel]) -> list[Pedido]:
        return [Pedido.model_validate(model, from_attributes=True) for model in models]
