


from app.domain.error import NotFoundError


class UsuarioNotFoundError(NotFoundError):
    def __init__(self, message="Usuário não encontrado", code=404):
        self.message = message
        self.code = code
        super().__init__(self.message, self.code)