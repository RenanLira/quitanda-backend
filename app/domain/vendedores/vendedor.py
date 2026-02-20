from decimal import Decimal
from uuid import uuid7
from pydantic import BaseModel
from typing import List

from slugify import slugify

from app.domain.vendedores.horario_funcionamento import DiaSemana, HorarioFuncionamento
from .produto_vendedor import ProdutoVendedor, StatusProduto

class Vendedor(BaseModel):
    id: str
    usuario_id: str
    comunidade_id: str | None
    nome_fantasia: str
    nome_fantasia_slug: str
    descricao: str | None
    produtos: List[ProdutoVendedor] = []
    chave_pix: str
    horarios_funcionamento: List[HorarioFuncionamento] = []
    
    
    @classmethod
    def criar(cls, usuario_id: str, comunidade_id: str | None, nome_fantasia: str, descricao: str | None, chave_pix: str) -> Vendedor:
        
        id = str(uuid7())
        nome_fantasia_slug = slugify(nome_fantasia)
        
        return cls(
            id=id,
            usuario_id=usuario_id,
            comunidade_id=comunidade_id,
            nome_fantasia=nome_fantasia,
            descricao=descricao,
            chave_pix=chave_pix,
            nome_fantasia_slug=nome_fantasia_slug
        )
        
    def adicionar_produto(self, produto_id: str, preco: Decimal, estoque: int) -> ProdutoVendedor:
        produto_vendedor = ProdutoVendedor.criar(
            vendedor_id=self.id,
            produto_id=produto_id,
            preco=preco,
            estoque=estoque,
            status=StatusProduto.DISPONIVEL
        )
        
        self.produtos.append(produto_vendedor)
        return produto_vendedor
        
    def registrar_horario_funcionamento(self, dia_semana: DiaSemana, hora_inicio: str, hora_fim: str, todo_tempo: bool = False) -> HorarioFuncionamento:
        horario = HorarioFuncionamento.criar(**{
            'dia_semana': dia_semana,
            'hora_inicio': hora_inicio,
            'hora_fim': hora_fim,
            'todo_tempo': todo_tempo,
            'vendedor_id': self.id
        })
        
        self.horarios_funcionamento.append(horario)
        return horario