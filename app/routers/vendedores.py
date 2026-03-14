

from typing import Annotated
from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel

from app.dependencies import get_current_user, get_vendedor_service
from app.domain.auth.decorators.authorization import require_roles
from app.domain.usuarios.usuario import ETipoUsuario
from app.domain.vendedores.dto.produto_vendedor_dto import CriarProdutoVendedorDTO
from app.domain.vendedores.dto.vendedores_dto import CriarVendedorDTO
from app.domain.vendedores.vendedor_service import VendedorService


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
        @require_roles([ETipoUsuario.ADMIN])
        async def criar_vendedor(
            body: Annotated[CriarVendedorDTO, Body()],
            current_user: Annotated[str, Depends(get_current_user)],
            vendedor_service: Annotated[VendedorService, Depends(get_vendedor_service)]
        ):
            
            vendedor = await vendedor_service.criar_vendedor(body)

            return vendedor

        @self.post("/produtos", description="Cadastra um produto para o vendedor autenticado")
        @require_roles([ETipoUsuario.VENDEDOR])
        async def cadastrar_produto_vendedor(
            body: Annotated[CriarProdutoVendedorDTO, Body()],
            current_user: Annotated[str, Depends(get_current_user)],
            vendedor_service: Annotated[VendedorService, Depends(get_vendedor_service)]
        ):
            return {"message": "Cadastrar produto para vendedor"}