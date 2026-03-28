

from abc import ABC, abstractmethod

from app.domain.vendedores.horario_funcionamento import HorarioFuncionamento
from app.domain.vendedores.produto_vendedor import ProdutoVendedor, ProdutoVendedorComProdutoInfo
from app.domain.vendedores.read_models import HorarioFuncionamentoReadInfo, VendedorReadInfo
from app.domain.vendedores.vendedor import Vendedor


class VendedorRepository(ABC):

    @abstractmethod
    async def save(self, vendedor: Vendedor) -> None: ...

    @abstractmethod
    async def find_read_by_id_ativo(self, vendedor_id: str) -> VendedorReadInfo | None: ...

    @abstractmethod
    async def find_read_by_usuario_id(self, usuario_id: str) -> VendedorReadInfo | None: ...

    @abstractmethod
    async def get_vendedores_ativos_por_comunidade(self, comunidade_id: str) -> list[VendedorReadInfo]: ...

    @abstractmethod
    async def get_produtos_vendedor_ordenado(
        self,
        vendedor_id: str,
    ) -> list[ProdutoVendedorComProdutoInfo]: ...

    @abstractmethod
    async def get_produtos_vendedores_por_comunidade(
        self,
        comunidade_id: str,
    ) -> list[ProdutoVendedorComProdutoInfo]: ...

    @abstractmethod
    async def add_produto_vendedor(self, produto_vendedor: ProdutoVendedor) -> None: ...

    @abstractmethod
    async def add_horario_funcionamento(self, horario: HorarioFuncionamento) -> None: ...

    @abstractmethod
    async def update_horario_funcionamento(self, horario: HorarioFuncionamento) -> None: ...

    @abstractmethod
    async def find_horario_by_id_vendedor(
        self,
        horario_id: str,
        vendedor_id: str,
    ) -> HorarioFuncionamento | None: ...

    @abstractmethod
    async def list_horarios_vendedor(self, vendedor_id: str) -> list[HorarioFuncionamentoReadInfo]: ...