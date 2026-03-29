

from sqlalchemy import select
from app.database import get_db_session
from app.database.models.usuario import UsuarioModel
from app.domain.usuarios.interfaces.usurario_repository import EmailOrTelefoneAlreadyExistsResponse, UsuarioRepository
from app.domain.usuarios.usuario import Usuario
from sqlalchemy.ext.asyncio import AsyncSession

class UsuarioRepositoryImpl(UsuarioRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        
        
    async def save(self, usuario: Usuario) -> None:
        
        self.session.add(UsuarioModel(**usuario.model_dump()))
        await self.session.commit()

    async def update(self, usuario: Usuario) -> None:
        usuario_model = await self.session.get(UsuarioModel, usuario.id)
        if not usuario_model:
            return

        for key, value in usuario.model_dump().items():
            setattr(usuario_model, key, value)

        await self.session.commit()
    
    async def find_by_id(self, id: str) -> Usuario | None:
        
        query = await self.session.execute(select(UsuarioModel).where(UsuarioModel.id == id))
        
        usuario = query.scalars().first()
        
        if not usuario:
            return None
        
        return Usuario.model_validate(usuario, from_attributes=True)
    
    async def find_by(self, by: str, value: str) -> Usuario | None:
        query = await self.session.execute(select(UsuarioModel).where(getattr(UsuarioModel, by) == value))
        
        usuario = query.scalars().first()
        
        if not usuario:
            return None
        
        return Usuario.model_validate(usuario, from_attributes=True)
    
    async def usuario_existe(self, email: str | None, telefone: str) -> EmailOrTelefoneAlreadyExistsResponse:
        if email:
            query = await self.session.execute(
                select(UsuarioModel).where(
                    (UsuarioModel.email == email) | (UsuarioModel.telefone == telefone)
                )
            )
        else:
            query = await self.session.execute(
                select(UsuarioModel).where(UsuarioModel.telefone == telefone)
            )

        result = query.scalars().first()
        return EmailOrTelefoneAlreadyExistsResponse(
            email_exists=bool(result and result.email == email),
            telefone_exists=bool(result and result.telefone == telefone)
        )
    
async def get_usuario_repository(session: AsyncSession | None = None) -> UsuarioRepository:
    if session is None:
        session = await get_db_session().__anext__()

    return UsuarioRepositoryImpl(session)