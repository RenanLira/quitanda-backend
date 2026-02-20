from app.domain.usuarios.interfaces.usurario_repository import UsuarioRepository
from app.domain.usuarios.usuario import Usuario
from app.domain.usuarios.dto.criar_usuario import CriarUsuarioDTO

class UsuarioService:
    def __init__(self, usuario_repository: UsuarioRepository) -> None:
        self.usuario_repository = usuario_repository


    async def criar_usuario(self, dto: CriarUsuarioDTO) -> Usuario:
        usuario = Usuario.criar(dto)
        
        # salvar no banco de dados
        await self.usuario_repository.save(usuario)
        
        return usuario