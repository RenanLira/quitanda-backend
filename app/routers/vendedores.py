

from typing import Annotated
from fastapi import APIRouter, Body, Depends

from app.dependencies import get_current_user, get_vendedor_service
from app.domain.auth.decorators.authorization import require_roles
from app.domain.usuarios.usuario import ETipoUsuario, Usuario
from app.domain.vendedores.dto.horario_funcionamento_dtos import (
    AtualizarHorarioFuncionamentoDTO,
    CriarHorarioFuncionamentoDTO,
)
from app.domain.vendedores.dto.produto_vendedor_dto import CriarProdutoVendedorDTO
from app.domain.vendedores.dto.vendedores_dto import CriarVendedorDTO
from app.domain.vendedores.read_models import HorarioFuncionamentoReadInfo
from app.domain.vendedores.vendedor_service import VendedorService


class VendedoresRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "/vendedores"
        self.tags = ["vendedores"]
        self.registrar_rotas()
        
    def registrar_rotas(self):
        
        @self.get("/")
        def listar_vendedores():
            return {"message": "Listar vendedores"}
        
        @self.post("/", description="Cria um novo vendedor associado a um usuário existente")
        @require_roles([ETipoUsuario.ADMIN])
        async def criar_vendedor(
            body: Annotated[CriarVendedorDTO, Body()],
            current_user: Annotated[Usuario, Depends(get_current_user)],
            vendedor_service: Annotated[VendedorService, Depends(get_vendedor_service)]
        ):
            
            vendedor = await vendedor_service.criar_vendedor(body)

            return vendedor.model_dump(mode="json")

        @self.get("/me/produtos", description="Lista produtos_vendedores do vendedor autenticado")
        @require_roles([ETipoUsuario.VENDEDOR])
        async def listar_meus_produtos_vendedor(
            current_user: Annotated[Usuario, Depends(get_current_user)],
            vendedor_service: Annotated[VendedorService, Depends(get_vendedor_service)],
        ):
            vendedor = await vendedor_service.get_meus_produtos_vendedor(current_user.id)
            return vendedor.model_dump(mode="json")

        @self.get("/{vendedor_id}/produtos", description="Lista produtos_vendedores de um vendedor")
        async def listar_produtos_vendedor_por_id(
            vendedor_id: str,
            vendedor_service: Annotated[VendedorService, Depends(get_vendedor_service)],
        ):
            vendedor = await vendedor_service.get_produtos_vendedor_por_id(vendedor_id)
            return vendedor.model_dump(mode="json")

        @self.post("/produtos", description="Cadastra um produto para o vendedor autenticado")
        @require_roles([ETipoUsuario.VENDEDOR])
        async def cadastrar_produto_vendedor(
            body: Annotated[CriarProdutoVendedorDTO, Body()],
            current_user: Annotated[Usuario, Depends(get_current_user)],
            vendedor_service: Annotated[VendedorService, Depends(get_vendedor_service)]
        ):
            await vendedor_service.cadastrar_produto_vendedor(current_user.id, body)
            return {"message": "Produto cadastrado para vendedor"}

        @self.post("/me/horarios", description="Registra horario de funcionamento do vendedor autenticado")
        @require_roles([ETipoUsuario.VENDEDOR])
        async def registrar_horario_funcionamento(
            body: Annotated[CriarHorarioFuncionamentoDTO, Body()],
            current_user: Annotated[Usuario, Depends(get_current_user)],
            vendedor_service: Annotated[VendedorService, Depends(get_vendedor_service)],
        ) -> HorarioFuncionamentoReadInfo:
            horario = await vendedor_service.registrar_horario_funcionamento(current_user.id, body)
            return horario

        @self.put("/me/horarios/{horario_id}", description="Atualiza um horario de funcionamento do vendedor autenticado")
        @require_roles([ETipoUsuario.VENDEDOR])
        async def atualizar_horario_funcionamento(
            horario_id: str,
            body: Annotated[AtualizarHorarioFuncionamentoDTO, Body()],
            current_user: Annotated[Usuario, Depends(get_current_user)],
            vendedor_service: Annotated[VendedorService, Depends(get_vendedor_service)],
        ):
            horario = await vendedor_service.atualizar_horario_funcionamento(current_user.id, horario_id, body)
            return horario.model_dump(mode="json")