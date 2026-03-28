from typing import Annotated

from fastapi import APIRouter, Body, Depends

from app.dependencies import get_produto_service
from app.dependencies import get_current_user
from app.domain.auth.decorators.authorization import require_roles
from app.domain.produtos.dto.criar_produto_dto import CriarProdutoDTO
from app.domain.produtos.produto_service import ProdutoService
from app.domain.usuarios.usuario import ETipoUsuario, Usuario
from app.http.mappers.produtos import map_produto


class ProdutosRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, prefix="/produtos", tags=["produtos"], **kwargs)
        self.registrar_rotas()

    def registrar_rotas(self):
        @self.post("/", description="Cria um novo produto base")
        @require_roles([ETipoUsuario.ADMIN])
        async def criar_produto(
            body: Annotated[CriarProdutoDTO, Body()],
            current_user: Annotated[Usuario, Depends(get_current_user)],
            produto_service: Annotated[ProdutoService, Depends(get_produto_service)],
        ):
            produto = await produto_service.criar_produto(body)
            return map_produto(produto).model_dump(mode="json")
