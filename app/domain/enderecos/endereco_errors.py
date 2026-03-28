from app.domain.error import NotFoundError


class EnderecoNotFoundError(NotFoundError):
    def __init__(self, message="Endereco nao encontrado", code=404):
        self.message = message
        self.code = code
        super().__init__(self.message, self.code)
