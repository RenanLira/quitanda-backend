

from enum import Enum


class TipoComunidade(str, Enum):
    FEIRA = "feira"
    MERCADO = "mercado"
    BAIRRO = "bairro"
    CONDOMINIO = "condominio"
    OUTRO = "outro"