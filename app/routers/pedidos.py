from typing import Annotated

from fastapi import APIRouter, Body, Depends

from app.dependencies import get_current_user, get_pedido_service
from app.domain.auth.decorators.authorization import require_roles
from app.domain.pedidos.dto.criar_pedido_dto import CriarPedidosDTO
from app.domain.pedidos.dto.recusar_pedido_dto import RecusarPedidoDTO
from app.domain.pedidos.pedido_service import PedidoService
from app.domain.usuarios.usuario import ETipoUsuario, Usuario
from app.http.mappers.pedidos import map_pedido


class PedidosRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, prefix="/pedidos", tags=["pedidos"], **kwargs)
        self.registrar_rotas()

    def registrar_rotas(self):
        @self.post("/", description="Cria pedidos por vendedor a partir do checkout")
        @require_roles([ETipoUsuario.CLIENTE])
        async def criar_pedidos(
            body: Annotated[CriarPedidosDTO, Body()],
            current_user: Annotated[Usuario, Depends(get_current_user)],
            pedido_service: Annotated[PedidoService, Depends(get_pedido_service)],
        ):
            pedidos = await pedido_service.criar_pedidos(current_user.id, body)
            return [map_pedido(pedido).model_dump(mode="json") for pedido in pedidos]

        @self.get("/me", description="Lista pedidos do cliente autenticado")
        @require_roles([ETipoUsuario.CLIENTE])
        async def listar_meus_pedidos(
            current_user: Annotated[Usuario, Depends(get_current_user)],
            pedido_service: Annotated[PedidoService, Depends(get_pedido_service)],
        ):
            pedidos = await pedido_service.listar_pedidos_cliente(current_user.id)
            return [map_pedido(pedido).model_dump(mode="json") for pedido in pedidos]

        @self.get("/recebidos", description="Lista pedidos recebidos pelo vendedor autenticado")
        @require_roles([ETipoUsuario.VENDEDOR])
        async def listar_pedidos_recebidos(
            current_user: Annotated[Usuario, Depends(get_current_user)],
            pedido_service: Annotated[PedidoService, Depends(get_pedido_service)],
        ):
            pedidos = await pedido_service.listar_pedidos_vendedor(current_user.id)
            return [map_pedido(pedido).model_dump(mode="json") for pedido in pedidos]

        @self.get("/", description="Lista todos os pedidos")
        @require_roles([ETipoUsuario.ADMIN])
        async def listar_todos_pedidos(
            current_user: Annotated[Usuario, Depends(get_current_user)],
            pedido_service: Annotated[PedidoService, Depends(get_pedido_service)],
        ):
            pedidos = await pedido_service.listar_todos()
            return [map_pedido(pedido).model_dump(mode="json") for pedido in pedidos]

        @self.get("/{pedido_id}", description="Busca pedido por ID com controle de acesso")
        async def obter_pedido_por_id(
            pedido_id: str,
            current_user: Annotated[Usuario, Depends(get_current_user)],
            pedido_service: Annotated[PedidoService, Depends(get_pedido_service)],
        ):
            pedido = await pedido_service.obter_pedido_por_id(pedido_id, current_user)
            return map_pedido(pedido).model_dump(mode="json")

        @self.put("/{pedido_id}/aprovar", description="Vendedor aprova pedido pendente")
        @require_roles([ETipoUsuario.VENDEDOR])
        async def aprovar_pedido(
            pedido_id: str,
            current_user: Annotated[Usuario, Depends(get_current_user)],
            pedido_service: Annotated[PedidoService, Depends(get_pedido_service)],
        ):
            pedido = await pedido_service.aprovar_pedido(pedido_id, current_user.id)
            return map_pedido(pedido).model_dump(mode="json")

        @self.put("/{pedido_id}/recusar", description="Vendedor recusa pedido pendente")
        @require_roles([ETipoUsuario.VENDEDOR])
        async def recusar_pedido(
            pedido_id: str,
            body: Annotated[RecusarPedidoDTO, Body()],
            current_user: Annotated[Usuario, Depends(get_current_user)],
            pedido_service: Annotated[PedidoService, Depends(get_pedido_service)],
        ):
            pedido = await pedido_service.recusar_pedido(
                pedido_id=pedido_id,
                vendedor_usuario_id=current_user.id,
                motivo=body["motivo"],
            )
            return map_pedido(pedido).model_dump(mode="json")
