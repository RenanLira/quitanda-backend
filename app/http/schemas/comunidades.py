from pydantic import BaseModel


class ComunidadeResumoResponse(BaseModel):
    id: str
    nome: str
    nome_slug: str
    descricao_curta: str
    descricao_longa: str | None
    cor_tema: str
    tipo: str
    imagem_url: str | None
    ativo: bool
