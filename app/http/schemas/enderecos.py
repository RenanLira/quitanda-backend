from pydantic import BaseModel


class EnderecoResponse(BaseModel):
    id: str
    usuario_id: str | None
    comunidade_id: str | None
    latitude: float
    longitude: float
    cep: str
    cidade: str
    rua: str
    numero: str
    bairro: str
    estado: str
