
from enum import Enum
from pydantic import BaseModel, Field

class StatusPedido(str, Enum):
    PENDENTE = "pendente"
    APROVADO = "aprovado"
    RECUSADO = "recusado"
    ENTREGUE = "entregue"


class Pedido(BaseModel):
    id: str
    cliente_id: str
    vendedor_id: str
    produto_id: str
    quantidade: int
    valor_total: float
    status: StatusPedido = Field(default=StatusPedido.PENDENTE)