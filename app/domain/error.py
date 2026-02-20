

class DomainError(Exception):
    """Classe base para erros de domínio."""
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code
        super().__init__(self.message)