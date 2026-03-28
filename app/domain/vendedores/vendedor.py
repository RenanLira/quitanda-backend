from pydantic import BaseModel

class Vendedor(BaseModel):
    id: str
    usuario_id: str
    comunidade_id: str
    nome_fantasia: str
    nome_fantasia_slug: str
    descricao: str | None
    chave_pix: str