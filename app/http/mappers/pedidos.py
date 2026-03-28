from app.domain.pedidos.pedido import Pedido, PedidoItem
from app.http.schemas.pedidos import PedidoItemResponse, PedidoResponse


def map_pedido_item(item: PedidoItem) -> PedidoItemResponse:
    return PedidoItemResponse(
        id=item.id,
        pedido_id=item.pedido_id,
        produto_vendedor_id=item.produto_vendedor_id,
        quantidade=item.quantidade,
        preco_unitario=item.preco_unitario,
        valor_total_item=item.valor_total_item,
    )


def map_pedido(pedido: Pedido) -> PedidoResponse:
    return PedidoResponse(
        id=pedido.id,
        cliente_id=pedido.cliente_id,
        vendedor_id=pedido.vendedor_id,
        comunidade_id=pedido.comunidade_id,
        status=pedido.status.value,
        motivo_recusa=pedido.motivo_recusa,
        valor_total=pedido.valor_total,
        itens=[map_pedido_item(item) for item in pedido.itens],
        criado_em=pedido.criado_em,
        atualizado_em=pedido.atualizado_em,
        aprovado_em=pedido.aprovado_em,
        recusado_em=pedido.recusado_em,
    )
