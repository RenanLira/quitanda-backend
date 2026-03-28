

from app.domain.produtos.dto.criar_produto_dto import CriarProdutoDTO
from app.domain.produtos.interfaces.produto_repository import ProdutoRepository
from app.domain.produtos.produto import Produto
from app.domain.error import DomainError
from uuid import uuid7


class ProdutoService:
    def __init__(self, produto_repository: ProdutoRepository):
        self.produto_repository = produto_repository
        
        
    async def criar_produto(self, produto_dto: CriarProdutoDTO) -> Produto:
        produto = Produto(
            id=str(uuid7()),
            nome=produto_dto["nome"],
            descricao=produto_dto["descricao"],
            tipo_unidade=produto_dto["tipo_unidade"],
        )
        
        await self.produto_repository.save(produto)
        
        return produto

    async def get_produto_por_id(self, produto_id: str) -> Produto:
        produto = await self.produto_repository.find_by_id(produto_id)
        if not produto:
            raise DomainError("Produto nao encontrado", code=404)
        return produto
        