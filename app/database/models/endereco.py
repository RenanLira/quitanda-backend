

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

if TYPE_CHECKING:
    from app.database.models.comunidade import ComunidadeModel
    from app.database.models.usuario import UsuarioModel


class EnderecoModel(Base):
    __tablename__ = "enderecos"

    id: Mapped[str] = mapped_column(primary_key=True)
    usuario_id: Mapped[str] = mapped_column(ForeignKey("usuarios.id"), nullable=True, index=True)
    comunidade_id: Mapped[str] = mapped_column(ForeignKey("comunidades.id"), nullable=True, index=True)

    latitude: Mapped[float] = mapped_column(nullable=True)
    longitude: Mapped[float] = mapped_column(nullable=True)

    cep: Mapped[str] = mapped_column()
    cidade: Mapped[str] = mapped_column()
    rua: Mapped[str] = mapped_column()
    numero: Mapped[str] = mapped_column()
    bairro: Mapped[str] = mapped_column()
    estado: Mapped[str] = mapped_column()

    usuario: Mapped["UsuarioModel"] = relationship(back_populates="endereco")
    comunidade: Mapped["ComunidadeModel"] = relationship(back_populates="endereco")
