


from typing import Annotated
from fastapi import APIRouter, Body, Depends

from app.dependencies import get_current_user, get_endereco_service, get_usuario_service
from app.domain.auth.decorators.authorization import require_roles
from app.domain.enderecos.dto.criar_endereco_dto import CriarEnderecoDTO
from app.domain.enderecos.endereco_service import EnderecoService
from app.domain.usuarios.dto.criar_usuario import CriarUsuarioDTO
from app.domain.usuarios.services.usuario_service import UsuarioService
from app.domain.usuarios.usuario import ETipoUsuario, Usuario
from app.http.mappers.enderecos import map_endereco
from app.http.mappers.usuarios import map_usuario_publico




class UsuariosRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, prefix="/usuarios", tags=["usuarios"], **kwargs)
        
        self.registrar_rotas()
    
    def registrar_rotas(self):
        
        @self.get("/me")
        async def obter_usuario_atual(
            current_user: Annotated[Usuario, Depends(get_current_user)]
        ):
            return map_usuario_publico(current_user).model_dump(mode="json")

        @self.get("/me/endereco")
        async def obter_endereco_usuario_atual(
            current_user: Annotated[Usuario, Depends(get_current_user)],
            endereco_service: Annotated[EnderecoService, Depends(get_endereco_service)],
        ):
            endereco = await endereco_service.get_por_usuario(current_user.id)
            return map_endereco(endereco).model_dump(mode="json")

        @self.put("/me/endereco")
        async def atualizar_endereco_usuario_atual(
            body: Annotated[CriarEnderecoDTO, Body()],
            current_user: Annotated[Usuario, Depends(get_current_user)],
            endereco_service: Annotated[EnderecoService, Depends(get_endereco_service)],
        ):
            endereco = await endereco_service.criar_ou_atualizar_para_usuario(current_user.id, body)
            return map_endereco(endereco).model_dump(mode="json")

        @self.get("/{usuario_id}/endereco")
        @require_roles([ETipoUsuario.ADMIN])
        async def obter_endereco_usuario_por_id(
            usuario_id: str,
            current_user: Annotated[Usuario, Depends(get_current_user)],
            usuario_service: Annotated[UsuarioService, Depends(get_usuario_service)],
            endereco_service: Annotated[EnderecoService, Depends(get_endereco_service)],
        ):
            await usuario_service.get_usuario_por_id(usuario_id)
            endereco = await endereco_service.get_por_usuario(usuario_id)
            return map_endereco(endereco).model_dump(mode="json")

        @self.put("/{usuario_id}/endereco")
        @require_roles([ETipoUsuario.ADMIN])
        async def atualizar_endereco_usuario_por_id(
            usuario_id: str,
            body: Annotated[CriarEnderecoDTO, Body()],
            current_user: Annotated[Usuario, Depends(get_current_user)],
            usuario_service: Annotated[UsuarioService, Depends(get_usuario_service)],
            endereco_service: Annotated[EnderecoService, Depends(get_endereco_service)],
        ):
            await usuario_service.get_usuario_por_id(usuario_id)
            endereco = await endereco_service.criar_ou_atualizar_para_usuario(usuario_id, body)
            return map_endereco(endereco).model_dump(mode="json")
        
        @self.get("/{usuario_id}")
        @require_roles([ETipoUsuario.ADMIN])
        async def obter_usuario_por_id(
            usuario_id: str,
            current_user: Annotated[Usuario, Depends(get_current_user)],
            usuario_service: Annotated[UsuarioService, Depends(get_usuario_service)],
        ):
            usuario = await usuario_service.get_usuario_por_id(usuario_id)
            return map_usuario_publico(usuario).model_dump(mode="json")
        
        
        @self.post("/")
        @require_roles([ETipoUsuario.ADMIN])
        async def criar_usuario(
            body: Annotated[CriarUsuarioDTO, Body()],
            current_user: Annotated[Usuario, Depends(get_current_user)],
            usuario_service: Annotated[UsuarioService, Depends(get_usuario_service)]
        ):
            
            usuario = await usuario_service.criar_usuario(body)
            
            return map_usuario_publico(usuario).model_dump(mode="json")