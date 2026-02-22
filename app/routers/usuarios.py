


from typing import Annotated
from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel, Field

from app.dependencies import get_current_user, get_usuario_repository, get_usuario_service
from app.domain.auth.decorators.authorization import require_roles
from app.domain.usuarios.dto.criar_usuario import CriarUsuarioDTO
from app.domain.usuarios.interfaces.usurario_repository import UsuarioRepository
from app.domain.usuarios.services.usuario_service import UsuarioService
from app.domain.usuarios.usuario import ETipoUsuario, Usuario




class UsuariosRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, prefix="/usuarios", tags=["usuarios"], **kwargs)
        
        self.registrar_rotas()
    
    def registrar_rotas(self):
        
        @self.get("/me")
        async def obter_usuario_atual(
            current_user: Annotated[Usuario, Depends(get_current_user)]
        ):
            return current_user.model_dump(exclude={"password_hash"})
        
        @self.get("/{usuario_id}")
        @require_roles([ETipoUsuario.ADMIN])
        async def obter_usuario_por_id(
            usuario_id: str,
            usuario_repository: Annotated[UsuarioRepository, Depends(get_usuario_repository)]
        ):
            usuario = await usuario_repository.find_by_id(usuario_id)
            
            if not usuario:
                return {"message": "Usuário não encontrado"}, 404
            
            return usuario.model_dump(exclude={"password_hash"})
        
        
        @self.post("/")
        @require_roles([ETipoUsuario.ADMIN])
        async def criar_usuario(
            body: Annotated[CriarUsuarioDTO, Body()],
            usuario_service: Annotated[UsuarioService, Depends(get_usuario_service)]
        ):
            
            usuario = await usuario_service.criar_usuario(body)
            
            return usuario.model_dump(exclude={"password_hash"})