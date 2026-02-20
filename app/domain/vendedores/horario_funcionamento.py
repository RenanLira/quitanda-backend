

from enum import Enum
from uuid import uuid7
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
    
    @classmethod
    def criar(cls, vendedor_id: str, dia_semana: DiaSemana, hora_inicio: str, hora_fim: str, todo_tempo: bool = False) -> HorarioFuncionamento:
        
        id = str(uuid7())
        
        return cls(
            id=id,
            vendedor_id=vendedor_id,
            dia_semana=dia_semana,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim,
            todo_tempo=todo_tempo
        )
    
    
    