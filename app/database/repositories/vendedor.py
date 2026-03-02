
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database.models.comunidade import VendedorModel
from app.domain.vendedores.interfaces.vendedor_repository import VendedorRepository
from app.domain.vendedores.vendedor import Vendedor
from sqlalchemy.ext.asyncio import AsyncSession

class VendedorRepositoryImpl(VendedorRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, vendedor: Vendedor) -> None:
        
        vendedor_model = VendedorModel(
            usuario_id=vendedor.usuario.id,
            comunidade_id=vendedor.comunidade.id,
            **vendedor.model_dump(exclude={'usuario', 'comunidade'})
        )        
        self.session.add(vendedor_model)

        await self.session.commit()
    
    async def find_by_id(self, vendedor_id: str) -> Vendedor | None:

        vendedor_model = await self.session.get(VendedorModel, vendedor_id)
        
        return Vendedor.model_validate(vendedor_model) if vendedor_model else None


    async def get_vendedores_por_comunidade(self, comunidade_id: str) -> list[Vendedor]:

        result = await self.session.execute(
            select(VendedorModel)
            .where(VendedorModel.comunidade_id == comunidade_id)
            .options(
                joinedload(VendedorModel.usuario),
            )
        )


        return [Vendedor.model_validate(vendedor_model) for vendedor_model in result.scalars()]