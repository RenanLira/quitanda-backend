
from abc import ABC, abstractmethod

from app.domain.produtos.produto import Produto


class ProdutoRepository(ABC):
    
    @abstractmethod
    async def save(self, produto: Produto) -> None: ...
    
    @abstractmethod
    async def find_by_id(self, id: str) -> Produto | None: ...
    
    @abstractmethod
    async def find_by(self, by: str, value: str) -> Produto | None: ...
    
    @abstractmethod
    async def delete(self, id: str) -> None: ...
    
    