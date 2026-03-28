import bcrypt
from fastapi.exceptions import RequestValidationError
from uuid import uuid7

from app.domain.usuarios.interfaces.usurario_repository import UsuarioRepository
from app.domain.usuarios.usuario import ETipoUsuario, Usuario
from app.domain.usuarios.dto.criar_usuario import CriarUsuarioDTO
from app.domain.usuarios.usuario_errors import UsuarioNotFoundError
from app.domain.usuarios.usuario_errors import UsuarioTipoInvalidoError

class UsuarioService:
    def __init__(self, usuario_repository: UsuarioRepository) -> None:
        self.usuario_repository = usuario_repository


    async def get_usuario_por_id(self, usuario_id: str) -> Usuario:

        usuario = await self.usuario_repository.find_by_id(usuario_id)
        if not usuario:
            raise UsuarioNotFoundError()

        return usuario
    
    async def mudar_tipo_usuario(self, usuario_id: str, novo_tipo: ETipoUsuario) -> Usuario:
        usuario = await self.get_usuario_por_id(usuario_id)
        self._validar_transicao_tipo(usuario.tipo, novo_tipo)
        usuario.tipo = novo_tipo

        await self.usuario_repository.save(usuario)
        
        return usuario


    async def criar_usuario(self, dto: CriarUsuarioDTO) -> Usuario:
        existing_user = await self.usuario_repository.usuario_existe(dto.get("email"), dto["telefone"])

        if existing_user.telefone_exists:
            raise RequestValidationError(errors=[{
                "loc": ["body", "telefone"],
                "msg": "Telefone já cadastrado",
                "type": "value_error",
            }])

        if existing_user.email_exists:
            raise RequestValidationError(errors=[{
                "loc": ["body", "email"],
                "msg": "Email já cadastrado",
                "type": "value_error",
            }])

        hash_password = bcrypt.hashpw(dto["password"].encode("utf-8"), bcrypt.gensalt())
        usuario = Usuario(
            id=str(uuid7()),
            nome=dto["nome"],
            email=dto.get("email"),
            password_hash=hash_password.decode("utf-8"),
            telefone=dto["telefone"],
            tipo=ETipoUsuario.CLIENTE,
            ativo=True,
        )

        await self.usuario_repository.save(usuario)
        
        return usuario

    def _validar_transicao_tipo(self, tipo_atual: ETipoUsuario, novo_tipo: ETipoUsuario) -> None:
        match (tipo_atual, novo_tipo):
            case (ETipoUsuario.CLIENTE, ETipoUsuario.VENDEDOR):
                return
            case (ETipoUsuario.VENDEDOR, ETipoUsuario.CLIENTE):
                return
            case (ETipoUsuario.ADMIN, _):
                raise UsuarioTipoInvalidoError("Não é permitido mudar o tipo de um usuário ADMIN")
            case (_, ETipoUsuario.ADMIN):
                raise UsuarioTipoInvalidoError("Não é permitido mudar para o tipo ADMIN")
            case _:
                raise UsuarioTipoInvalidoError(
                    f"Mudança de tipo de usuário de {tipo_atual} para {novo_tipo} não é permitida"
                )