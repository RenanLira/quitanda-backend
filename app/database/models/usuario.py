

from . import Base
from sqlalchemy.orm import Mapped, mapped_column

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