


from sqlalchemy import select

from app.database.models.comunidade import ComunidadeModel
from app.domain.comunidades.comunidade import Comunidade
from app.domain.comunidades.interfaces.comunidade_repository import ComunidadeRepository
from sqlalchemy.ext.asyncio import AsyncSession

class ComunidadeRepositoryImpl(ComunidadeRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, comunidade: Comunidade) -> None:
        self.session.add(ComunidadeModel(**comunidade.model_dump()))
        await self.session.commit()

    async def find_by_id(self, comunidade_id: str) -> Comunidade | None:
        result = await self.session.execute(select(ComunidadeModel).where(ComunidadeModel.id == comunidade_id))
        comunidade_model = result.scalars().first()
        if not comunidade_model:
            return None
        return Comunidade.model_validate(comunidade_model, from_attributes=True)