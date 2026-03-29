import bcrypt
from fastapi.exceptions import RequestValidationError
from uuid import uuid7
from app.domain.error import DomainError

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
        nome = self._normalizar_nome(dto["nome"])
        telefone = self._normalizar_telefone(dto["telefone"])
        existing_user = await self.usuario_repository.usuario_existe(dto.get("email"), telefone)

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
            nome=nome,
            email=dto.get("email"),
            password_hash=hash_password.decode("utf-8"),
            telefone=telefone,
            tipo=ETipoUsuario.CLIENTE,
            ativo=True,
            cadastro_completo=True,
        )

        await self.usuario_repository.save(usuario)
        
        return usuario

    async def obter_ou_criar_cadastro_simplificado(self, nome: str, telefone: str) -> Usuario:
        nome_normalizado = self._normalizar_nome(nome)
        telefone_normalizado = self._normalizar_telefone(telefone)

        usuario = await self.usuario_repository.find_by("telefone", telefone_normalizado)
        if usuario:
            if usuario.tipo != ETipoUsuario.CLIENTE:
                raise DomainError("Telefone vinculado a um usuario que nao e cliente", code=400)
            if not usuario.ativo:
                raise DomainError("Usuario inativo nao pode criar pedidos", code=400)

            if not usuario.cadastro_completo and usuario.nome != nome_normalizado:
                usuario.nome = nome_normalizado
                await self.usuario_repository.update(usuario)

            return usuario

        senha_temporaria = bcrypt.hashpw(str(uuid7()).encode("utf-8"), bcrypt.gensalt())
        novo_usuario = Usuario(
            id=str(uuid7()),
            nome=nome_normalizado,
            email=None,
            password_hash=senha_temporaria.decode("utf-8"),
            telefone=telefone_normalizado,
            tipo=ETipoUsuario.CLIENTE,
            ativo=True,
            cadastro_completo=False,
        )
        await self.usuario_repository.save(novo_usuario)
        return novo_usuario

    def _normalizar_nome(self, nome: str) -> str:
        nome_normalizado = nome.strip()
        if not nome_normalizado:
            raise RequestValidationError(errors=[{
                "loc": ["body", "nome"],
                "msg": "Nome e obrigatorio",
                "type": "value_error",
            }])
        return nome_normalizado

    def _normalizar_telefone(self, telefone: str) -> str:
        telefone_normalizado = "".join(char for char in telefone if char.isdigit())
        if not telefone_normalizado:
            raise RequestValidationError(errors=[{
                "loc": ["body", "telefone"],
                "msg": "Telefone invalido",
                "type": "value_error",
            }])
        return telefone_normalizado

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