from app.domain.enderecos.dto.criar_endereco_dto import CriarEnderecoDTO
from app.domain.enderecos.endereco import Endereco
from app.domain.enderecos.endereco_errors import EnderecoNotFoundError
from app.domain.enderecos.interfaces.endereco_repository import EnderecoRepository
from uuid import uuid7


class EnderecoService:
    def __init__(self, repository: EnderecoRepository) -> None:
        self.repository = repository

    async def get_por_usuario(self, usuario_id: str) -> Endereco:
        endereco = await self.repository.find_by_usuario_id(usuario_id)
        if not endereco:
            raise EnderecoNotFoundError("Endereco do usuario nao encontrado")
        return endereco

    async def get_por_comunidade(self, comunidade_id: str) -> Endereco:
        endereco = await self.repository.find_by_comunidade_id(comunidade_id)
        if not endereco:
            raise EnderecoNotFoundError("Endereco da comunidade nao encontrado")
        return endereco

    async def criar_ou_atualizar_para_usuario(self, usuario_id: str, dto: CriarEnderecoDTO) -> Endereco:
        existente = await self.repository.find_by_usuario_id(usuario_id)
        if existente:
            endereco = existente.model_copy(update={
                "latitude": dto["latitude"],
                "longitude": dto["longitude"],
                "cep": dto["cep"],
                "cidade": dto["cidade"],
                "rua": dto["rua"],
                "numero": dto["numero"],
                "bairro": dto["bairro"],
                "estado": dto["estado"],
            })
            await self.repository.update(endereco)
            return endereco

        endereco = Endereco(
            id=str(uuid7()),
            usuario_id=usuario_id,
            comunidade_id=None,
            latitude=dto["latitude"],
            longitude=dto["longitude"],
            cep=dto["cep"],
            cidade=dto["cidade"],
            rua=dto["rua"],
            numero=dto["numero"],
            bairro=dto["bairro"],
            estado=dto["estado"],
        )
        await self.repository.save(endereco)
        return endereco

    async def criar_ou_atualizar_para_comunidade(self, comunidade_id: str, dto: CriarEnderecoDTO) -> Endereco:
        existente = await self.repository.find_by_comunidade_id(comunidade_id)
        if existente:
            endereco = existente.model_copy(update={
                "latitude": dto["latitude"],
                "longitude": dto["longitude"],
                "cep": dto["cep"],
                "cidade": dto["cidade"],
                "rua": dto["rua"],
                "numero": dto["numero"],
                "bairro": dto["bairro"],
                "estado": dto["estado"],
            })
            await self.repository.update(endereco)
            return endereco

        endereco = Endereco(
            id=str(uuid7()),
            usuario_id=None,
            comunidade_id=comunidade_id,
            latitude=dto["latitude"],
            longitude=dto["longitude"],
            cep=dto["cep"],
            cidade=dto["cidade"],
            rua=dto["rua"],
            numero=dto["numero"],
            bairro=dto["bairro"],
            estado=dto["estado"],
        )
        await self.repository.save(endereco)
        return endereco
