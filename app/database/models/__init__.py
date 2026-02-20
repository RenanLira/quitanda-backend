
from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .usuario import UsuarioModel
from .comunidade import VendedorModel, HorarioFuncionamentoModel, ComunidadeModel, ProdutoVendedorModel
from .produto import ProdutoModel