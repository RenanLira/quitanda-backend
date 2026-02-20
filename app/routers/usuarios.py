


from typing import Annotated
from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel, Field

from app.dependencies import get_current_user, get_usuario_repository
from app.domain.usuarios.dto.criar_usuario import CriarUsuarioDTO
from app.domain.usuarios.interfaces.usurario_repository import UsuarioRepository
from app.domain.usuarios.usuario import Usuario




class UsuariosRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, prefix="/usuarios", tags=["usuarios"], **kwargs)
        
        self.registrar_rotas()
    
    def registrar_rotas(self):
        
        @self.get("/")
        def listar_usuarios():
            return {"message": "Listar usuários"}
        
        @self.get("/me")
        async def obter_usuario_atual(
            current_user: Annotated[Usuario, Depends(get_current_user)]
        ):
            return current_user.model_dump(exclude={"password_hash"})
        
        
        @self.post("/")
        async def criar_usuario(
            body: Annotated[CriarUsuarioDTO, Body()],
            usuario_repository: Annotated[UsuarioRepository, Depends(get_usuario_repository)]
        ):
            usuario = Usuario.criar(body)
            
            await usuario_repository.save(usuario)
            
            
            
            return usuario.model_dump(exclude={"password_hash"})