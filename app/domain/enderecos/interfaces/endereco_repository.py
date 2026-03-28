from abc import ABC, abstractmethod

from app.domain.enderecos.endereco import Endereco


class EnderecoRepository(ABC):
    @abstractmethod
    async def save(self, endereco: Endereco) -> None: ...

    @abstractmethod
    async def update(self, endereco: Endereco) -> None: ...

    @abstractmethod
    async def find_by_usuario_id(self, usuario_id: str) -> Endereco | None: ...

    @abstractmethod
    async def find_by_comunidade_id(self, comunidade_id: str) -> Endereco | None: ...
