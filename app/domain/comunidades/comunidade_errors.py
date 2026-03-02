
from app.domain.error import NotFoundError


class ComunidadeNotFoundError(NotFoundError):
    def __init__(self, message="Comunidade não encontrada", code=404):
        self.message = message
        self.code = code
        super().__init__(self.message, self.code)