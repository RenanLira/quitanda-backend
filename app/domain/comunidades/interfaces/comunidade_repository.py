


from abc import ABC, abstractmethod

from app.domain.comunidades.comunidade import Comunidade

class ComunidadeRepository(ABC):
    
    @abstractmethod
    async def save(self, comunidade: Comunidade) -> None: ...

    @abstractmethod
    async def find_by_id(self, comunidade_id: str) -> Comunidade | None: ...


    