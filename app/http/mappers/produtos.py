from app.domain.produtos.produto import Produto
from app.http.schemas.produtos import ProdutoResponse


def map_produto(produto: Produto) -> ProdutoResponse:
    return ProdutoResponse(
        id=produto.id,
        nome=produto.nome,
        descricao=produto.descricao,
        tipo_unidade=produto.tipo_unidade.value,
    )
