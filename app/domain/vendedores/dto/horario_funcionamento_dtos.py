

from typing import TypedDict

from app.domain.vendedores.horario_funcionamento import DiaSemana


class CriarHorarioFuncionamentoDTO(TypedDict):
    dia_semana: DiaSemana
    hora_inicio: str
    hora_fim: str
    todo_tempo: bool


class AtualizarHorarioFuncionamentoDTO(TypedDict):
    dia_semana: DiaSemana
    hora_inicio: str
    hora_fim: str
    todo_tempo: bool