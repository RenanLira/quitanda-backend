from typing import Annotated, TypedDict

from pydantic import Field


class CriarEnderecoDTO(TypedDict):
    cep: Annotated[str, Field(..., description="CEP", examples=["01001-000"])]
    cidade: Annotated[str, Field(..., description="Cidade", examples=["Sao Paulo"])]
    rua: Annotated[str, Field(..., description="Rua", examples=["Rua das Flores"])]
    numero: Annotated[str, Field(..., description="Numero", examples=["123"])]
    bairro: Annotated[str, Field(..., description="Bairro", examples=["Centro"])]
    estado: Annotated[str, Field(..., description="Estado", examples=["SP"])]
    latitude: Annotated[float, Field(..., description="Latitude", examples=[-23.55052])]
    longitude: Annotated[float, Field(..., description="Longitude", examples=[-46.633308])]
