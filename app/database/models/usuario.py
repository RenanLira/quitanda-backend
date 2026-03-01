
from datetime import datetime, timezone

from sqlalchemy import ForeignKey

from app.domain.auth.auth_service import TokenType

from . import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.usuarios.usuario import ETipoUsuario

class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id: Mapped[str] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=True, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    telefone: Mapped[str] = mapped_column(nullable=False, index=True)
    tipo: Mapped[ETipoUsuario] = mapped_column(nullable=False, default=ETipoUsuario.CLIENTE)
    ativo: Mapped[bool] = mapped_column(nullable=False, default=True)
    
    tokens: Mapped[list["TokenModel"]] = relationship(back_populates="usuario")

class TokenModel(Base):
    __tablename__ = "tokens"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey(UsuarioModel.id))
    usuario: Mapped[UsuarioModel] = relationship(back_populates="tokens")
    token_type: Mapped[TokenType] = mapped_column(nullable=False)
    expires_at: Mapped[datetime] = mapped_column(nullable=False, default=timezone.utc)