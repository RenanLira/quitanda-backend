


from app.domain.comunidades.comunidade import Comunidade
from app.domain.comunidades.comunidade_errors import ComunidadeNotFoundError
from app.domain.comunidades.dto.criar_comunidade_dto import CriarComunidadeDTO
from app.domain.comunidades.interfaces.comunidade_repository import ComunidadeRepository
from app.domain.enderecos.endereco_service import EnderecoService
from slugify import slugify
from uuid import uuid7


class ComunidadeService:
    def __init__(self, repository: ComunidadeRepository, endereco_service: EnderecoService) -> None:
        self.repository = repository
        self.endereco_service = endereco_service


    async def get_comunidade_por_id(self, comunidade_id: str) -> Comunidade:
        comunidade = await self.repository.find_by_id(comunidade_id)
        if not comunidade:
            raise ComunidadeNotFoundError()
        return comunidade

    async def criar_comunidade(self, criar_comunidade_dto: CriarComunidadeDTO) -> Comunidade:
        comunidade = Comunidade(
            id=str(uuid7()),
            nome=criar_comunidade_dto["nome"],
            nome_slug=slugify(criar_comunidade_dto["nome"]),
            descricao_curta=criar_comunidade_dto["descricao_curta"],
            descricao_longa=criar_comunidade_dto["descricao_longa"],
            tipo=criar_comunidade_dto["tipo"],
            cor_tema=criar_comunidade_dto["cor_tema"],
            imagem_url=criar_comunidade_dto["imagem_url"],
        )
        
        await self.repository.save(comunidade)
        await self.endereco_service.criar_ou_atualizar_para_comunidade(
            comunidade.id,
            criar_comunidade_dto["endereco"],
        )
        
        return comunidade
