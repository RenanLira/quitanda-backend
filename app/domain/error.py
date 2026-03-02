

class DomainError(Exception):
    """Classe base para erros de domínio."""
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code
        super().__init__(self.message)

class NotFoundError(DomainError):
    """Erro para recursos não encontrados."""
    def __init__(self, message: str = "Recurso não encontrado", code: int = 404):
        super().__init__(message, code)
