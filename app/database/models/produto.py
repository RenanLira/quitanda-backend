

from sqlalchemy.orm import Mapped, mapped_column

from . import Base
from app.domain.produtos.produto import TipoUnidade



class ProdutoModel(Base):
    __tablename__ = "produtos"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    descricao: Mapped[str] = mapped_column(nullable=False)
    tipo_unidade: Mapped[TipoUnidade] = mapped_column("unidade_medida", nullable=False)
    imagem_url: Mapped[str] = mapped_column(nullable=True)