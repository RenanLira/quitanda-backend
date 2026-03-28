from pydantic import BaseModel


class ProdutoResponse(BaseModel):
    id: str
    nome: str
    descricao: str
    tipo_unidade: str
