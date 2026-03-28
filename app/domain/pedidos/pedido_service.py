from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid7

from app.domain.auth.auth_errors import UsuarioSemPermissaoError
from app.domain.error import DomainError
from app.domain.pedidos.dto.criar_pedido_dto import CriarPedidosDTO
from app.domain.pedidos.interfaces.pedido_repository import PedidoRepository
from app.domain.pedidos.pedido import Pedido, PedidoItem, StatusPedido
from app.domain.pedidos.pedido_errors import (
    PedidoComunidadeInvalidaError,
    PedidoItensInvalidosError,
    PedidoNotFoundError,
    PedidoProdutoVendedorInvalidoError,
    PedidoStatusInvalidoError,
)
from app.domain.usuarios.services.usuario_service import UsuarioService
from app.domain.usuarios.usuario import ETipoUsuario, Usuario
from app.domain.vendedores.interfaces.vendedor_repository import VendedorRepository
from app.domain.vendedores.produto_vendedor import StatusProduto


class PedidoService:
    def __init__(
        self,
        repository: PedidoRepository,
        usuario_service: UsuarioService,
        vendedor_repository: VendedorRepository,
    ) -> None:
        self.repository = repository
        self.usuario_service = usuario_service
        self.vendedor_repository = vendedor_repository

    async def criar_pedidos(self, cliente_id: str, dto: CriarPedidosDTO) -> list[Pedido]:
        cliente = await self.usuario_service.get_usuario_por_id(cliente_id)
        if not cliente.ativo:
            raise DomainError("Usuario inativo nao pode criar pedidos", code=400)

        itens_dto = dto.get("itens", [])
        if not itens_dto:
            raise PedidoItensInvalidosError()

        quantidade_por_produto_vendedor: dict[str, int] = {}
        for item in itens_dto:
            produto_vendedor_id = item["produto_vendedor_id"]
            quantidade = item["quantidade"]
            if quantidade <= 0:
                raise PedidoItensInvalidosError("Quantidade de item deve ser maior que zero")
            quantidade_por_produto_vendedor[produto_vendedor_id] = (
                quantidade_por_produto_vendedor.get(produto_vendedor_id, 0) + quantidade
            )

        produto_vendedor_ids = list(quantidade_por_produto_vendedor.keys())
        infos = await self.repository.get_produtos_vendedores_info(produto_vendedor_ids)

        if len(infos) != len(produto_vendedor_ids):
            raise PedidoProdutoVendedorInvalidoError("Um ou mais produto_vendedor_id sao invalidos")

        comunidades = {info.comunidade_id for info in infos}
        if len(comunidades) > 1:
            raise PedidoComunidadeInvalidaError()

        infos_por_id = {info.produto_vendedor_id: info for info in infos}
        itens_por_vendedor: dict[str, list[PedidoItem]] = {}

        for produto_vendedor_id, quantidade in quantidade_por_produto_vendedor.items():
            info = infos_por_id[produto_vendedor_id]

            if not info.ativo or info.status_produto != StatusProduto.DISPONIVEL.value:
                raise PedidoProdutoVendedorInvalidoError(
                    f"Produto_vendedor {produto_vendedor_id} esta indisponivel"
                )

            if quantidade > info.estoque:
                raise PedidoProdutoVendedorInvalidoError(
                    f"Estoque insuficiente para produto_vendedor {produto_vendedor_id}"
                )

            item = PedidoItem(
                id=str(uuid7()),
                pedido_id="",
                produto_vendedor_id=produto_vendedor_id,
                quantidade=quantidade,
                preco_unitario=Decimal(info.preco),
                valor_total_item=Decimal(info.preco) * Decimal(quantidade),
            )
            itens_por_vendedor.setdefault(info.vendedor_id, []).append(item)

        pedidos: list[Pedido] = []
        comunidade_id = comunidades.pop() if comunidades else None

        for vendedor_id, itens in itens_por_vendedor.items():
            agora = datetime.now(timezone.utc)
            pedido = Pedido(
                id=str(uuid7()),
                cliente_id=cliente.id,
                vendedor_id=vendedor_id,
                comunidade_id=comunidade_id,
                status=StatusPedido.PENDENTE,
                motivo_recusa=None,
                valor_total=Decimal("0"),
                itens=[],
                criado_em=agora,
                atualizado_em=agora,
            )
            itens_com_pedido = [
                PedidoItem(
                    id=item.id,
                    pedido_id=pedido.id,
                    produto_vendedor_id=item.produto_vendedor_id,
                    quantidade=item.quantidade,
                    preco_unitario=item.preco_unitario,
                    valor_total_item=item.valor_total_item,
                )
                for item in itens
            ]
            pedido.itens = itens_com_pedido
            pedido.valor_total = sum((item.valor_total_item for item in itens_com_pedido), Decimal("0"))
            pedidos.append(pedido)

        # TODO: atacado - redistribuicao inteligente por estoque entre vendedores da comunidade.
        await self.repository.save_many(pedidos)
        return pedidos

    async def listar_pedidos_cliente(self, cliente_id: str) -> list[Pedido]:
        return await self.repository.find_by_cliente_id(cliente_id)

    async def listar_pedidos_vendedor(self, vendedor_usuario_id: str) -> list[Pedido]:
        vendedor = await self.vendedor_repository.find_read_by_usuario_id(vendedor_usuario_id)
        if not vendedor:
            raise DomainError("Vendedor nao encontrado", code=404)
        return await self.repository.find_by_vendedor_id(vendedor.id)

    async def listar_todos(self) -> list[Pedido]:
        return await self.repository.find_all()

    async def obter_pedido_por_id(self, pedido_id: str, current_user: Usuario) -> Pedido:
        pedido = await self.repository.find_by_id(pedido_id)
        if not pedido:
            raise PedidoNotFoundError()

        tipo = current_user.tipo
        if tipo == ETipoUsuario.ADMIN:
            return pedido

        if tipo == ETipoUsuario.CLIENTE and pedido.cliente_id == current_user.id:
            return pedido

        if tipo == ETipoUsuario.VENDEDOR:
            vendedor = await self.vendedor_repository.find_read_by_usuario_id(current_user.id)
            if vendedor and pedido.vendedor_id == vendedor.id:
                return pedido

        raise UsuarioSemPermissaoError()

    async def aprovar_pedido(self, pedido_id: str, vendedor_usuario_id: str) -> Pedido:
        pedido = await self._obter_pedido_do_vendedor(pedido_id, vendedor_usuario_id)
        if pedido.status != StatusPedido.PENDENTE:
            raise PedidoStatusInvalidoError("Apenas pedidos pendentes podem ser aprovados")

        pedido.aprovar()
        await self.repository.update(pedido)
        return pedido

    async def recusar_pedido(
        self,
        pedido_id: str,
        vendedor_usuario_id: str,
        motivo: str,
    ) -> Pedido:
        if not motivo or not motivo.strip():
            raise PedidoStatusInvalidoError("Motivo da recusa e obrigatorio")

        pedido = await self._obter_pedido_do_vendedor(pedido_id, vendedor_usuario_id)
        if pedido.status != StatusPedido.PENDENTE:
            raise PedidoStatusInvalidoError("Apenas pedidos pendentes podem ser recusados")

        pedido.recusar(motivo.strip())
        await self.repository.update(pedido)
        return pedido

    async def _obter_pedido_do_vendedor(self, pedido_id: str, vendedor_usuario_id: str) -> Pedido:
        pedido = await self.repository.find_by_id(pedido_id)
        if not pedido:
            raise PedidoNotFoundError()

        vendedor = await self.vendedor_repository.find_read_by_usuario_id(vendedor_usuario_id)
        if not vendedor or vendedor.id != pedido.vendedor_id:
            raise UsuarioSemPermissaoError()

        return pedido
