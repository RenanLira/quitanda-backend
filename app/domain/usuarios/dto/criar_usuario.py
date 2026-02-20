from typing import Annotated, NotRequired, TypedDict
from pydantic import EmailStr

from pydantic import Field



class CriarUsuarioDTO(TypedDict,):
    nome: Annotated[str, Field(description="Nome do usuário", examples=["Renan Lira"])]
    email: Annotated[NotRequired[EmailStr], Field(description="Email do usuário", examples=["renan.lira@exemplo.com"])]
    password: Annotated[str, Field(description="Senha do usuário", examples=["123456"])]
    telefone: Annotated[str, Field(description="Telefone do usuário", examples=["(11) 99999-9999"])]
    
    
    