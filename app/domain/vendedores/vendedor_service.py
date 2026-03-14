

from app.domain.comunidades.comunidade_errors import ComunidadeNotFoundError
from app.domain.comunidades.comunidade_service import ComunidadeService
from app.domain.error import DomainError
from app.domain.usuarios.services.usuario_service import UsuarioService
from app.domain.usuarios.usuario import ETipoUsuario
from app.domain.vendedores.dto.produto_vendedor_dto import CriarProdutoVendedorDTO
from app.domain.vendedores.dto.vendedores_dto import CriarVendedorDTO
from app.domain.vendedores.interfaces.vendedor_repository import VendedorRepository
from app.domain.vendedores.vendedor import Vendedor


class VendedorService():
    def __init__(self, 
        repository: VendedorRepository,
        comunidade_service: ComunidadeService,
        usuario_service: UsuarioService
    ) -> None:
        self.repository = repository
        self.comunidade_service = comunidade_service
        self.usuario_service = usuario_service

    async def criar_vendedor(self, vendedorDTO: CriarVendedorDTO) -> None:
        
        comunidade = await self.comunidade_service.get_comunidade_por_id(vendedorDTO['comunidade_id'])
        usuario = await self.usuario_service.get_usuario_por_id(vendedorDTO['usuario_id'])

        if usuario.tipo_usuario != ETipoUsuario.CLIENTE:
            raise DomainError("O usuário deve ser do tipo CLIENTE para se tornar um vendedor")

        vendedor = Vendedor.criar(
            usuario=usuario,
            comunidade=comunidade,
            nome_fantasia=vendedorDTO['nome_fantasia'],
            descricao=vendedorDTO.get('descricao'),
            chave_pix=vendedorDTO['chave_pix']
        )

        await self.repository.save(vendedor)

    async def cadastrar_produto_vendedor(self, vendedor_id: str, produto_vendedor_dto: CriarProdutoVendedorDTO):
        ...
        # vendedor = await self.repository.find_by_id(vendedor_id)

        # if not vendedor:
        #     raise DomainError("Vendedor não encontrado")
        

        # await self.repository.save(vendedor)

        # return produto_vendedor

    async def get_vendedores_por_comunidade(self, comunidade_id: str) -> list[Vendedor]:
        return await self.repository.get_vendedores_por_comunidade(comunidade_id)
