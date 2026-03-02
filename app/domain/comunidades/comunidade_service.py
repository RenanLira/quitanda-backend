


from app.domain.comunidades.comunidade import Comunidade
from app.domain.comunidades.comunidade_errors import ComunidadeNotFoundError
from app.domain.comunidades.dto.criar_comunidade_dto import CriarComunidadeDTO
from app.domain.comunidades.interfaces.comunidade_repository import ComunidadeRepository


class ComunidadeService:
    def __init__(self, repository: ComunidadeRepository) -> None:
        self.repository = repository


    async def get_comunidade_por_id(self, comunidade_id: str) -> Comunidade:

        comunidade = await self.repository.find_by_id(comunidade_id)
        if not comunidade:
            raise ComunidadeNotFoundError()

        return comunidade

    async def criar_comunidade(self, criar_comunidade_dto: CriarComunidadeDTO) -> Comunidade:
        comunidade = Comunidade.criar(criar_comunidade_dto)
        
        await self.repository.save(comunidade)
        
        return comunidade
