

from typing import Annotated, TypedDict

from pydantic import Field

from app.domain.produtos.produto import TipoUnidade


class CriarProdutoDTO(TypedDict): 
    nome: Annotated[str, Field(..., min_length=1, max_length=255)]
    descricao: Annotated[str, Field(..., min_length=1, max_length=255)]
    tipo_unidade: Annotated[TipoUnidade, Field(...)]