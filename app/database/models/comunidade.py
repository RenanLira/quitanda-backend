


from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from app.database.models.produto import ProdutoModel
from app.database.models.usuario import UsuarioModel
from app.domain.comunidades.comunidade import TipoComunidade
from app.domain.vendedores.horario_funcionamento import DiaSemana
from app.domain.vendedores.produto_vendedor import StatusProduto
from . import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class HorarioFuncionamentoModel(Base):
    __tablename__ = "horarios_funcionamento"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    vendedor_id: Mapped[str] = mapped_column(ForeignKey("vendedores.id"))
    vendedor: Mapped[VendedorModel] = relationship(back_populates="horarios_funcionamento", single_parent=True)
    
    dia_semana: Mapped[DiaSemana] = mapped_column(nullable=False)
    hora_inicio: Mapped[str] = mapped_column(nullable=False)
    hora_fim: Mapped[str] = mapped_column(nullable=False)
    todo_tempo: Mapped[bool] = mapped_column(nullable=False, default=False)


class ProdutoVendedorModel(Base):
    __tablename__ = "produtos_vendedores"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    vendedor_id: Mapped[str] = mapped_column(ForeignKey("vendedores.id"))
    vendedor: Mapped[VendedorModel] = relationship(back_populates="produtos")
    
    produto_id: Mapped[str] = mapped_column(ForeignKey(ProdutoModel.id), nullable=False)
    produto: Mapped[ProdutoModel] = relationship()
    
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    estoque: Mapped[int] = mapped_column(nullable=False, default=1)
    status: Mapped[StatusProduto] = mapped_column(nullable=False, default=StatusProduto.DISPONIVEL)
    ativo: Mapped[bool] = mapped_column(nullable=False, default=True)

    

class VendedorModel(Base):
    __tablename__ = "vendedores"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    usuario_id: Mapped[str] = mapped_column(ForeignKey(UsuarioModel.id), index=True)
    usuario: Mapped[UsuarioModel] = relationship()
    horarios_funcionamento: Mapped[list["HorarioFuncionamentoModel"]] = relationship(back_populates="vendedor")
    comunidade_id: Mapped[str | None] = mapped_column(ForeignKey("comunidades.id"), nullable=True, index=True)
    comunidade: Mapped[ComunidadeModel] = relationship(back_populates="vendedores")
    nome_fantasia: Mapped[str] = mapped_column(nullable=False)
    nome_fantasia_slug: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    descricao: Mapped[str] = mapped_column(nullable=True)
    chave_pix: Mapped[str] = mapped_column(nullable=False)
    
    produtos: Mapped[list[ProdutoVendedorModel]] = relationship(back_populates="vendedor")
    


class ComunidadeModel(Base):
    __tablename__ = "comunidades"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    nome_slug: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    descricao_curta: Mapped[str] = mapped_column()
    descricao_longa: Mapped[str] = mapped_column(nullable=True)
    cor_tema: Mapped[str] = mapped_column(nullable=False, default="#059669")
    tipo: Mapped[TipoComunidade] = mapped_column(nullable=False)
    imagem_url: Mapped[str] = mapped_column(nullable=True)
    ativo: Mapped[bool] = mapped_column(nullable=False, default=False)
    
    vendedores: Mapped[list[VendedorModel]] = relationship(back_populates="comunidade")