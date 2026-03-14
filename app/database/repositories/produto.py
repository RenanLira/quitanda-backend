
from sqlalchemy import select

from app.database import get_db_session
from app.database.models.produto import ProdutoModel
from app.domain.produtos.interfaces.produto_repository import ProdutoRepository

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.produtos.produto import Produto

class ProdutoRepositoryImpl(ProdutoRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
        
    async def save(self, produto: Produto) -> None:
        self.session.add(produto)
        await self.session.commit()
        
        
    async def find_by(self, by: str, value: str) -> Produto | None:
        result = await self.session.execute(select(ProdutoModel).where(getattr(ProdutoModel, by) == value))
        
        produto_model = result.scalars().first()
        
        if not produto_model:
            return None
        
        return Produto.model_validate(produto_model, from_attributes=True)
        
        
    async def find_by_id(self, id: str) -> Produto | None:
        result = await self.session.execute(select(ProdutoModel).where(ProdutoModel.id == id))
        
        produto_model = result.scalars().first()
        
        if not produto_model:
            return None
        
        return Produto.model_validate(produto_model, from_attributes=True)
    
    async def delete(self, id: str) -> None:
        produto = await self.find_by_id(id)
        
        if not produto:
            return
        
        await self.session.delete(produto)
        await self.session.commit()
        

async def get_produto_repository(session: AsyncSession | None = None) -> ProdutoRepository:
    if session is None:
        session = await get_db_session().__anext__()

    return ProdutoRepositoryImpl(session)