

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models import Base, usuario, comunidade


class EnderecoModel(Base):
    __tablename__ = "enderecos"

    id: Mapped[str] = mapped_column(primary_key=True)
    usuario_id: Mapped[str] = mapped_column(ForeignKey(usuario.UsuarioModel.id), nullable=True, index=True)
    comunidade_id: Mapped[str] = mapped_column(ForeignKey(comunidade.ComunidadeModel.id), nullable=True, index=True)

    latitude: Mapped[float] = mapped_column(nullable=True)
    longitude: Mapped[float] = mapped_column(nullable=True)

    cep: Mapped[str] = mapped_column()
    cidade: Mapped[str] = mapped_column()
    rua: Mapped[str] = mapped_column()
    numero: Mapped[str] = mapped_column()
    bairro: Mapped[str] = mapped_column()
    estado: Mapped[str] = mapped_column()
