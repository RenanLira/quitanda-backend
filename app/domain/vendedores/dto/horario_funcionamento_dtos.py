

from typing import TypedDict

from app.domain.vendedores.horario_funcionamento import DiaSemana


class CriarHorarioFuncionamentoDTO(TypedDict):
    vendedor_id: str
    dia_semana: DiaSemana
    hora_inicio: str
    hora_fim: str
    todo_tempo: bool