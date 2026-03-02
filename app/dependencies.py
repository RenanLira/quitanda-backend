
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db_session
from app.database.repositories.comunidade import ComunidadeRepositoryImpl
from app.database.repositories.token import TokenRepositoryImpl
from app.database.repositories.usuario import UsuarioRepositoryImpl
from app.database.repositories.vendedor import VendedorRepositoryImpl
from app.domain.auth.auth_service import AuthService
from app.domain.comunidades.comunidade_service import ComunidadeService
from app.domain.comunidades.interfaces.comunidade_repository import ComunidadeRepository
from app.domain.usuarios.interfaces.usurario_repository import UsuarioRepository
from app.domain.usuarios.services.usuario_service import UsuarioService
from app.domain.vendedores.interfaces.vendedor_repository import VendedorRepository
from app.domain.vendedores.vendedor_service import VendedorService
from app.settings import Settings, get_settings
from sqlalchemy.ext.asyncio import AsyncSession

def get_usuario_repository(session: Annotated[AsyncSession, Depends(get_db_session)]):
    
    return UsuarioRepositoryImpl(session=session)


def get_token_repository(session: Annotated[AsyncSession, Depends(get_db_session)]):

    return TokenRepositoryImpl(session=session)

def get_usuario_service(
    usuario_repository: Annotated[UsuarioRepository, Depends(get_usuario_repository)]
):
    return UsuarioService(usuario_repository=usuario_repository)

def get_auth_service(
    settings: Annotated[Settings, Depends(get_settings)],
    usuario_repository: Annotated[UsuarioRepository, Depends(get_usuario_repository)],
    token_repository: Annotated[TokenRepositoryImpl, Depends(get_token_repository)]
):
    return AuthService(settings=settings, usuario_repository=usuario_repository, token_repository=token_repository)

async def get_comunidade_repository(session: Annotated[AsyncSession, Depends(get_db_session)]):
    return ComunidadeRepositoryImpl(session=session)

async def get_comunidade_service(
        repository: Annotated[ComunidadeRepository, Depends(get_comunidade_repository)],
):
    return ComunidadeService(repository=repository)

async def get_vendedor_repository(session: Annotated[AsyncSession, Depends(get_db_session)]):
    return VendedorRepositoryImpl(session=session)

async def get_vendedor_service(
        repository: Annotated[VendedorRepository, Depends(get_vendedor_repository)],
        comunidade_service: Annotated[ComunidadeService, Depends(get_comunidade_service)],
        usuario_service: Annotated[UsuarioService, Depends(get_usuario_service)]
):
    return VendedorService(repository=repository, comunidade_service=comunidade_service, usuario_service=usuario_service)


async def get_current_user(
    token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/auth/signin", refreshUrl="/auth/refresh"))],
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):

    return await auth_service.get_current_user(token)