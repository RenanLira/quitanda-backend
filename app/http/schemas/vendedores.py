from decimal import Decimal

from pydantic import BaseModel


class HorarioFuncionamentoResponse(BaseModel):
    id: str
    vendedor_id: str
    dia_semana: int
    hora_inicio: str
    hora_fim: str
    todo_tempo: bool


class ProdutoVendedorResponse(BaseModel):
    produto_vendedor_id: str
    vendedor_id: str
    produto_id: str
    produto_nome: str
    produto_descricao: str
    tipo_unidade: str
    preco: Decimal
    estoque: int
    status: str


class VendedorComProdutosResponse(BaseModel):
    id: str
    nome_fantasia: str
    nome_fantasia_slug: str
    descricao: str | None
    comunidade_id: str | None
    horarios_funcionamento: list[HorarioFuncionamentoResponse]
    produtos_vendedores: list[ProdutoVendedorResponse]


class ProdutoComunidadeResponse(BaseModel):
    produto_id: str
    nome: str
    descricao: str
    tipo_unidade: str
    produtos_vendedores: list[ProdutoVendedorResponse]
