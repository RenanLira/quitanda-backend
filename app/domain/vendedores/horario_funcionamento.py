
from enum import Enum

from pydantic import BaseModel, Field


class DiaSemana(int, Enum):
    DOMINGO = 0
    SEGUNDA = 1
    TERCA = 2
    QUARTA = 3
    QUINTA = 4
    SEXTA = 5
    SABADO = 6


class HorarioFuncionamento(BaseModel):
    id: str
    vendedor_id: str
    dia_semana: DiaSemana
    hora_inicio: str
    hora_fim: str
    todo_tempo: bool = Field(default=False)




