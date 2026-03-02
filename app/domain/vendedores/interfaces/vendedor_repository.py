

from abc import ABC, abstractmethod

from app.domain.vendedores.vendedor import Vendedor


class VendedorRepository(ABC):

    @abstractmethod
    async def save(self, vendedor: Vendedor) -> None: ...

    @abstractmethod
    async def find_by_id(self, vendedor_id: str) -> Vendedor | None: ...

    @abstractmethod
    async def get_vendedores_por_comunidade(self, comunidade_id: str) -> list[Vendedor]: ...