from typing import Annotated

from fastapi import APIRouter, Body, Depends

from app.dependencies import get_comunidade_service, get_current_user, get_endereco_service, get_vendedor_service
from app.domain.auth.decorators.authorization import require_roles
from app.domain.comunidades.comunidade_service import ComunidadeService
from app.domain.comunidades.dto.criar_comunidade_dto import CriarComunidadeDTO
from app.domain.enderecos.dto.criar_endereco_dto import CriarEnderecoDTO
from app.domain.enderecos.endereco_service import EnderecoService
from app.domain.usuarios.usuario import ETipoUsuario, Usuario
from app.domain.vendedores.vendedor_service import VendedorService
from app.http.mappers.enderecos import map_endereco
from app.http.mappers.comunidades import map_comunidade_resumo


class ComunidadesRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, prefix="/comunidades", tags=["comunidades"], **kwargs)
        self.registrar_rotas()

    def registrar_rotas(self):
        @self.post("/")
        @require_roles([ETipoUsuario.ADMIN])
        async def criar_comunidade(
            body: Annotated[CriarComunidadeDTO, Body()],
            current_user: Annotated[Usuario, Depends(get_current_user)],
            comunidade_service: Annotated[ComunidadeService, Depends(get_comunidade_service)],
        ):
            comunidade = await comunidade_service.criar_comunidade(body)
            return map_comunidade_resumo(comunidade).model_dump(mode="json")

        @self.get("/{comunidade_id}")
        async def obter_comunidade_por_id(
            comunidade_id: str,
            comunidade_service: Annotated[ComunidadeService, Depends(get_comunidade_service)],
        ):
            comunidade = await comunidade_service.get_comunidade_por_id(comunidade_id)
            return map_comunidade_resumo(comunidade).model_dump(mode="json")

        @self.get("/{comunidade_id}/vendedores")
        async def listar_vendedores_da_comunidade(
            comunidade_id: str,
            comunidade_service: Annotated[ComunidadeService, Depends(get_comunidade_service)],
            vendedor_service: Annotated[VendedorService, Depends(get_vendedor_service)],
        ):
            await comunidade_service.get_comunidade_por_id(comunidade_id)
            vendedores = await vendedor_service.get_vendedores_ativos_com_produtos_por_comunidade(comunidade_id)
            return [vendedor.model_dump(mode="json") for vendedor in vendedores]

        @self.get("/{comunidade_id}/produtos")
        async def listar_produtos_da_comunidade(
            comunidade_id: str,
            comunidade_service: Annotated[ComunidadeService, Depends(get_comunidade_service)],
            vendedor_service: Annotated[VendedorService, Depends(get_vendedor_service)],
        ):
            await comunidade_service.get_comunidade_por_id(comunidade_id)
            produtos = await vendedor_service.get_catalogo_produtos_por_comunidade(comunidade_id)
            return [produto.model_dump(mode="json") for produto in produtos]

        @self.get("/{comunidade_id}/endereco")
        async def obter_endereco_comunidade(
            comunidade_id: str,
            endereco_service: Annotated[EnderecoService, Depends(get_endereco_service)],
        ):
            endereco = await endereco_service.get_por_comunidade(comunidade_id)
            return map_endereco(endereco).model_dump(mode="json")

        @self.put("/{comunidade_id}/endereco")
        @require_roles([ETipoUsuario.ADMIN])
        async def atualizar_endereco_comunidade(
            comunidade_id: str,
            body: Annotated[CriarEnderecoDTO, Body()],
            current_user: Annotated[Usuario, Depends(get_current_user)],
            comunidade_service: Annotated[ComunidadeService, Depends(get_comunidade_service)],
            endereco_service: Annotated[EnderecoService, Depends(get_endereco_service)],
        ):
            await comunidade_service.get_comunidade_por_id(comunidade_id)
            endereco = await endereco_service.criar_ou_atualizar_para_comunidade(comunidade_id, body)
            return map_endereco(endereco).model_dump(mode="json")
