from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.endereco import EnderecoModel
from app.domain.enderecos.endereco import Endereco
from app.domain.enderecos.interfaces.endereco_repository import EnderecoRepository


class EnderecoRepositoryImpl(EnderecoRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, endereco: Endereco) -> None:
        self.session.add(EnderecoModel(**endereco.model_dump()))
        await self.session.commit()

    async def update(self, endereco: Endereco) -> None:
        endereco_model = await self.session.get(EnderecoModel, endereco.id)
        if not endereco_model:
            return

        for key, value in endereco.model_dump().items():
            setattr(endereco_model, key, value)

        await self.session.commit()

    async def find_by_usuario_id(self, usuario_id: str) -> Endereco | None:
        result = await self.session.execute(
            select(EnderecoModel).where(EnderecoModel.usuario_id == usuario_id)
        )
        endereco_model = result.scalars().first()
        return Endereco.model_validate(endereco_model, from_attributes=True) if endereco_model else None

    async def find_by_comunidade_id(self, comunidade_id: str) -> Endereco | None:
        result = await self.session.execute(
            select(EnderecoModel).where(EnderecoModel.comunidade_id == comunidade_id)
        )
        endereco_model = result.scalars().first()
        return Endereco.model_validate(endereco_model, from_attributes=True) if endereco_model else None
