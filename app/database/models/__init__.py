
from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .usuario import UsuarioModel
from .vendedor import VendedorModel, HorarioFuncionamentoModel, ComunidadeModel