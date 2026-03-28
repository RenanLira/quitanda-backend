

from functools import wraps
import inspect

from app.domain.auth.auth_errors import UsuarioSemPermissaoError
from app.domain.error import DomainError
from app.domain.usuarios.usuario import ETipoUsuario, Usuario


def require_roles(allowed_roles: list[ETipoUsuario]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user: Usuario | None = None
            
            for arg in kwargs.values():
                if isinstance(arg, Usuario):
                    current_user = arg
                    break
                
            if not current_user:
                raise UsuarioSemPermissaoError("Usuário não autenticado")
            
            if current_user.tipo not in allowed_roles:
                raise UsuarioSemPermissaoError("Usuário não tem permissão para acessar este recurso")

            
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
            
        return wrapper
    return decorator