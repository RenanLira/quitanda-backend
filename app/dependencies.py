
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db_session
from app.database.repositories.usuario import UsuarioRepositoryImpl
from app.domain.auth.auth_service import AuthService
from app.domain.usuarios.interfaces.usurario_repository import UsuarioRepository
from app.domain.usuarios.services.usuario_service import UsuarioService
from app.settings import Settings, get_settings
from sqlalchemy.ext.asyncio import AsyncSession

def get_usuario_repository(session: Annotated[AsyncSession, Depends(get_db_session)]):
    
    return UsuarioRepositoryImpl(session=session)

def get_usuario_service(
    usuario_repository: Annotated[UsuarioRepository, Depends(get_usuario_repository)]
):
    return UsuarioService(usuario_repository=usuario_repository)

def get_auth_service(
    settings: Annotated[Settings, Depends(get_settings)],
    usuario_repository: Annotated[UsuarioRepository, Depends(get_usuario_repository)]
):
    return AuthService(settings=settings, usuario_repository=usuario_repository)

async def get_current_user(
    token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/auth/signin", refreshUrl="/auth/refresh"))],
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):

    return await auth_service.get_current_user(token)