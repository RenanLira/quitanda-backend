from abc import ABC, abstractmethod

from app.domain.pedidos.pedido import Pedido, ProdutoVendedorPedidoInfo


class PedidoRepository(ABC):
    @abstractmethod
    async def save_many(self, pedidos: list[Pedido]) -> None: ...

    @abstractmethod
    async def find_by_id(self, pedido_id: str) -> Pedido | None: ...

    @abstractmethod
    async def find_by_cliente_id(self, cliente_id: str) -> list[Pedido]: ...

    @abstractmethod
    async def find_by_vendedor_id(self, vendedor_id: str) -> list[Pedido]: ...

    @abstractmethod
    async def find_all(self) -> list[Pedido]: ...

    @abstractmethod
    async def update(self, pedido: Pedido) -> None: ...

    @abstractmethod
    async def get_produtos_vendedores_info(
        self,
        produto_vendedor_ids: list[str],
    ) -> list[ProdutoVendedorPedidoInfo]: ...
