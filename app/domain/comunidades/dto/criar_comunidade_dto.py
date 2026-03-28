


from typing import Annotated, TypedDict

from pydantic import Field

from app.domain.comunidades.types.tipo_comunidade import TipoComunidade
from app.domain.enderecos.dto.criar_endereco_dto import CriarEnderecoDTO



class CriarComunidadeDTO(TypedDict):

    nome: Annotated[str, Field(..., description="Nome da comunidade, deve ser único")]
    descricao_curta: Annotated[str, Field(..., description="Descrição curta da comunidade, usada em listagens")]
    descricao_longa: Annotated[str | None, Field(None, description="Descrição longa da comunidade, usada na página da comunidade")]
    tipo: Annotated[TipoComunidade, Field(..., description="Tipo da comunidade, deve ser um dos: feira, mercado, bairro, condominio, outro")]
    cor_tema: Annotated[str, Field("#059669", description="Cor tema da comunidade, em formato hexadecimal, ex: #059669")]
    imagem_url: Annotated[str | None, Field(None, description="URL da imagem da comunidade, usada na página da comunidade")]
    endereco: Annotated[CriarEnderecoDTO, Field(..., description="Endereço da comunidade")]