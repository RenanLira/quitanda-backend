

from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="O token de acesso JWT")
    refresh_token: str = Field(..., description="O token de atualização JWT")
    token_type: str = Field(..., description="O tipo do token, geralmente 'bearer'")