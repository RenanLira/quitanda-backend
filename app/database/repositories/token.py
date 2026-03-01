

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.usuario import TokenModel
from app.domain.auth.auth_service import TokenType
from app.domain.auth.interfaces.token_repository import TokenRepository

class TokenRepositoryImpl(TokenRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        
        
    async def create_token(self, user_id: str, token: str, expires_at: datetime, type: TokenType):
    
        token_model = TokenModel(
            id=token,
            user_id=user_id,
            expires_at=expires_at,
            token_type=type
        )
        self.session.add(token_model)
        await self.session.commit()
        
        
    async def exists(self, token: str, user_id: str, token_type: TokenType) -> bool:
        
        results = await self.session.execute(
            select(TokenModel).where(
                TokenModel.id == token,
                TokenModel.user_id == user_id,
                TokenModel.token_type == token_type)
        )
        
        return bool(results.scalars().first())
        
        
    async def delete_token(self, token: str):
        
        await self.session.delete(TokenModel(id=token))
        
        