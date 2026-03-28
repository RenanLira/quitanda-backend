from pydantic import BaseModel, Field

from app.domain.vendedores.horario_funcionamento import DiaSemana


class HorarioFuncionamentoReadInfo(BaseModel):
    id: str
    vendedor_id: str
    dia_semana: DiaSemana
    hora_inicio: str
    hora_fim: str
    todo_tempo: bool


class VendedorReadInfo(BaseModel):
    id: str
    usuario_id: str
    comunidade_id: str | None
    nome_fantasia: str
    nome_fantasia_slug: str
    descricao: str | None
    horarios_funcionamento: list[HorarioFuncionamentoReadInfo] = Field(default_factory=list)
