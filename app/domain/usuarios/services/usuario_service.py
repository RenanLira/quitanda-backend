from app.domain.usuarios.interfaces.usurario_repository import UsuarioRepository
from app.domain.usuarios.usuario import Usuario
from app.domain.usuarios.dto.criar_usuario import CriarUsuarioDTO
from app.domain.usuarios.usuario_errors import UsuarioNotFoundError

class UsuarioService:
    def __init__(self, usuario_repository: UsuarioRepository) -> None:
        self.usuario_repository = usuario_repository


    async def get_usuario_por_id(self, usuario_id: str) -> Usuario:

        usuario = await self.usuario_repository.find_by_id(usuario_id)
        if not usuario:
            raise UsuarioNotFoundError()

        return usuario


    async def criar_usuario(self, dto: CriarUsuarioDTO) -> Usuario:
        usuario = Usuario.criar(dto)
        
        # salvar no banco de dados
        await self.usuario_repository.save(usuario)
        
        return usuario