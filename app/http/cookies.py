from fastapi import Cookie
from pydantic import BaseModel


class Cookies(BaseModel):
    refresh_token: str | None = Cookie(default=None, alias="refresh_token")