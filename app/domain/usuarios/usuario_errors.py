


from app.domain.error import NotFoundError
from app.domain.error import DomainError


class UsuarioNotFoundError(NotFoundError):
    def __init__(self, message="Usuário não encontrado", code=404):
        self.message = message
        self.code = code
        super().__init__(self.message, self.code)


class UsuarioTipoInvalidoError(DomainError):
    def __init__(self, message="Mudança de tipo de usuário não permitida", code=400):
        self.message = message
        self.code = code
        super().__init__(self.message, self.code)