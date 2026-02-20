

from app.domain.produtos.dto.criar_produto_dto import CriarProdutoDTO
from app.domain.produtos.interfaces.produto_repository import ProdutoRepository
from app.domain.produtos.produto import Produto


class ProdutoService:
    def __init__(self, produto_repository: ProdutoRepository):
        self.produto_repository = produto_repository
        
        
    async def criar_produto(self, produto_dto: CriarProdutoDTO) -> Produto:
        
        produto = Produto.criar(**produto_dto)
        
        await self.produto_repository.save(produto)
        
        return produto
        