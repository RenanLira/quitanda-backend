


from abc import ABC, abstractmethod
from datetime import datetime

from app.domain.auth.enums.token_type import TokenType


class TokenRepository(ABC):
    
    @abstractmethod
    async def create_token(self, user_id: str, token: str, expires_at: datetime, type: TokenType): ...
    
    @abstractmethod
    async def exists(self, token: str, user_id: str, token_type: TokenType) -> bool: ...
    
    @abstractmethod
    async def delete_token(self, token: str): ...
    