from app.domain.vendedores.produto_vendedor import ProdutoVendedorComProdutoInfo
from app.domain.vendedores.read_models import HorarioFuncionamentoReadInfo, VendedorReadInfo
from app.http.schemas.vendedores import (
    HorarioFuncionamentoResponse,
    ProdutoComunidadeResponse,
    ProdutoVendedorResponse,
    VendedorComProdutosResponse,
)


def map_produto_info_to_response(item: ProdutoVendedorComProdutoInfo) -> ProdutoVendedorResponse:
    return ProdutoVendedorResponse(
        produto_vendedor_id=item.produto_vendedor_id,
        vendedor_id=item.vendedor_id,
        produto_id=item.produto_id,
        produto_nome=item.produto_nome,
        produto_descricao=item.produto_descricao,
        tipo_unidade=item.tipo_unidade,
        preco=item.preco,
        estoque=item.estoque,
        status=item.status,
    )


def map_horario_to_response(item: HorarioFuncionamentoReadInfo) -> HorarioFuncionamentoResponse:
    return HorarioFuncionamentoResponse(
        id=item.id,
        vendedor_id=item.vendedor_id,
        dia_semana=item.dia_semana.value,
        hora_inicio=item.hora_inicio,
        hora_fim=item.hora_fim,
        todo_tempo=item.todo_tempo,
    )


def map_vendedor_com_produtos(
    vendedor: VendedorReadInfo,
    itens: list[ProdutoVendedorComProdutoInfo],
    horarios: list[HorarioFuncionamentoReadInfo],
) -> VendedorComProdutosResponse:
    return VendedorComProdutosResponse(
        id=vendedor.id,
        nome_fantasia=vendedor.nome_fantasia,
        nome_fantasia_slug=vendedor.nome_fantasia_slug,
        descricao=vendedor.descricao,
        comunidade_id=vendedor.comunidade_id,
        horarios_funcionamento=[map_horario_to_response(horario) for horario in horarios],
        produtos_vendedores=[map_produto_info_to_response(item) for item in itens],
    )


def map_catalogo_comunidade(
    itens: list[ProdutoVendedorComProdutoInfo],
) -> list[ProdutoComunidadeResponse]:
    agrupados: dict[str, ProdutoComunidadeResponse] = {}

    for item in itens:
        produto = agrupados.get(item.produto_id)
        if not produto:
            produto = ProdutoComunidadeResponse(
                produto_id=item.produto_id,
                nome=item.produto_nome,
                descricao=item.produto_descricao,
                tipo_unidade=item.tipo_unidade,
                produtos_vendedores=[],
            )
            agrupados[item.produto_id] = produto

        produto.produtos_vendedores.append(map_produto_info_to_response(item))

    return list(agrupados.values())
