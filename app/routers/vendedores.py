

from typing import Annotated
from fastapi import APIRouter, Body
from pydantic import BaseModel

from app.domain.vendedores.dto.vendedores_dto import CriarVendedorDTO


class VendedoresRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "/vendedores"
        self.tags = ["vendedores"]
        self.registrar_rotas()
        
    def registrar_rotas(self):
        
        @self.get("/")
        def listar_vendedores():
            return {"message": "Listar vendedores"}
        
        @self.post("/", description="Cria um novo vendedor associado a um usuário existente")
        def criar_vendedor(
            body: Annotated[CriarVendedorDTO, Body()]
        ):
            return {"message": "Criar vendedor"}