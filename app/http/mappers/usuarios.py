from app.domain.usuarios.usuario import Usuario
from app.http.schemas.usuarios import UsuarioPublicResponse


def map_usuario_publico(usuario: Usuario) -> UsuarioPublicResponse:
    return UsuarioPublicResponse(
        id=usuario.id,
        nome=usuario.nome,
        email=usuario.email,
        telefone=usuario.telefone,
        tipo=usuario.tipo.value,
        ativo=usuario.ativo,
        cadastro_completo=usuario.cadastro_completo,
    )
