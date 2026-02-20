

from app.domain.error import DomainError


class TokenNotFoundError(DomainError):
    def __init__(self, message="Token não encontrado", code=401):
        self.message = message
        self.code = code
        super().__init__(self.message, self.code)
        
        
class InvalidTokenError(DomainError):
    def __init__(self, message="Token inválido ou expirado", code=401):
        self.message = message
        self.code = code
        super().__init__(self.message, self.code)
        
        
class CredenciaisInvalidasError(DomainError):
    def __init__(self, message="Credenciais inválidas", code=401):
        self.message = message
        self.code = code
        super().__init__(self.message, self.code)