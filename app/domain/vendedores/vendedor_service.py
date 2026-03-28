

from app.domain.comunidades.comunidade_service import ComunidadeService
from app.domain.vendedores.dto.horario_funcionamento_dtos import (
    AtualizarHorarioFuncionamentoDTO,
    CriarHorarioFuncionamentoDTO,
)
from app.domain.enderecos.endereco_errors import EnderecoNotFoundError
from app.domain.enderecos.endereco_service import EnderecoService
from app.domain.error import DomainError
from app.domain.usuarios.services.usuario_service import UsuarioService
from app.domain.usuarios.usuario import ETipoUsuario
from app.domain.vendedores.horario_funcionamento import HorarioFuncionamento
from app.domain.vendedores.read_models import HorarioFuncionamentoReadInfo
from decimal import Decimal
from datetime import datetime
from slugify import slugify
from uuid import uuid7

from app.domain.produtos.produto_service import ProdutoService
from app.domain.vendedores.dto.produto_vendedor_dto import CriarProdutoVendedorDTO
from app.domain.vendedores.dto.vendedores_dto import CriarVendedorDTO
from app.domain.vendedores.interfaces.vendedor_repository import VendedorRepository
from app.domain.vendedores.produto_vendedor import ProdutoVendedor, StatusProduto
from app.domain.vendedores.read_models import VendedorReadInfo
from app.domain.vendedores.vendedor import Vendedor
from app.http.mappers.vendedores import map_catalogo_comunidade, map_vendedor_com_produtos
from app.http.schemas.vendedores import ProdutoComunidadeResponse, VendedorComProdutosResponse


class VendedorService():
    def __init__(self, 
        repository: VendedorRepository,
        comunidade_service: ComunidadeService,
        usuario_service: UsuarioService,
        endereco_service: EnderecoService,
        produto_service: ProdutoService,
    ) -> None:
        self.repository = repository
        self.comunidade_service = comunidade_service
        self.usuario_service = usuario_service
        self.endereco_service = endereco_service
        self.produto_service = produto_service

    async def criar_vendedor(self, vendedorDTO: CriarVendedorDTO) -> VendedorReadInfo:
        await self.comunidade_service.get_comunidade_por_id(vendedorDTO['comunidade_id'])
        usuario = await self.usuario_service.get_usuario_por_id(vendedorDTO['usuario_id'])

        await self.usuario_service.mudar_tipo_usuario(usuario.id, ETipoUsuario.VENDEDOR)
        
        try:
            await self.endereco_service.get_por_usuario(usuario.id)
        except EnderecoNotFoundError:
            raise DomainError("O usuario deve ter endereco cadastrado para se tornar um vendedor")

        vendedor = Vendedor(
            id=str(uuid7()),
            usuario_id=usuario.id,
            comunidade_id=vendedorDTO['comunidade_id'],
            nome_fantasia=vendedorDTO['nome_fantasia'],
            nome_fantasia_slug=slugify(vendedorDTO['nome_fantasia']),
            descricao=vendedorDTO.get('descricao'),
            chave_pix=vendedorDTO['chave_pix'],
        )

        await self.repository.save(vendedor)

        vendedor_criado = await self.repository.find_read_by_usuario_id(usuario.id)
        if not vendedor_criado:
            raise DomainError("Falha ao carregar vendedor criado", code=500)

        return vendedor_criado

    async def cadastrar_produto_vendedor(self, usuario_id: str, produto_vendedor_dto: CriarProdutoVendedorDTO) -> None:
        vendedor = await self.repository.find_read_by_usuario_id(usuario_id)

        if not vendedor:
            raise DomainError("Vendedor não encontrado")

        await self.produto_service.get_produto_por_id(produto_vendedor_dto["produto_id"])

        produto_vendedor = ProdutoVendedor(
            id=str(uuid7()),
            vendedor_id=vendedor.id,
            produto_id=produto_vendedor_dto["produto_id"],
            preco=Decimal(str(produto_vendedor_dto["preco"])),
            estoque=produto_vendedor_dto["estoque"],
            status=StatusProduto.DISPONIVEL,
        )

        await self.repository.add_produto_vendedor(produto_vendedor)

    async def registrar_horario_funcionamento(
        self,
        usuario_id: str,
        horario_dto: CriarHorarioFuncionamentoDTO,
    ) -> HorarioFuncionamentoReadInfo:
        vendedor = await self.repository.find_read_by_usuario_id(usuario_id)
        if not vendedor:
            raise DomainError("Vendedor nao encontrado", code=404)

        self._validar_intervalo_horario(
            hora_inicio=horario_dto["hora_inicio"],
            hora_fim=horario_dto["hora_fim"],
            todo_tempo=horario_dto["todo_tempo"],
        )

        horario = HorarioFuncionamento(
            id=str(uuid7()),
            vendedor_id=vendedor.id,
            dia_semana=horario_dto["dia_semana"],
            hora_inicio=horario_dto["hora_inicio"],
            hora_fim=horario_dto["hora_fim"],
            todo_tempo=horario_dto["todo_tempo"],
        )
        await self.repository.add_horario_funcionamento(horario)

        horario_criado = await self.repository.find_horario_by_id_vendedor(horario.id, vendedor.id)
        if not horario_criado:
            raise DomainError("Falha ao carregar horario cadastrado", code=500)

        return HorarioFuncionamentoReadInfo.model_validate(horario_criado)

    async def atualizar_horario_funcionamento(
        self,
        usuario_id: str,
        horario_id: str,
        horario_dto: AtualizarHorarioFuncionamentoDTO,
    ) -> HorarioFuncionamentoReadInfo:
        vendedor = await self.repository.find_read_by_usuario_id(usuario_id)
        if not vendedor:
            raise DomainError("Vendedor nao encontrado", code=404)

        horario = await self.repository.find_horario_by_id_vendedor(horario_id, vendedor.id)
        if not horario:
            raise DomainError("Horario de funcionamento nao encontrado", code=404)

        self._validar_intervalo_horario(
            hora_inicio=horario_dto["hora_inicio"],
            hora_fim=horario_dto["hora_fim"],
            todo_tempo=horario_dto["todo_tempo"],
        )

        horario_atualizado = horario.model_copy(
            update={
                "dia_semana": horario_dto["dia_semana"],
                "hora_inicio": horario_dto["hora_inicio"],
                "hora_fim": horario_dto["hora_fim"],
                "todo_tempo": horario_dto["todo_tempo"],
            }
        )

        await self.repository.update_horario_funcionamento(horario_atualizado)
        return HorarioFuncionamentoReadInfo.model_validate(horario_atualizado)

    async def get_vendedores_ativos_com_produtos_por_comunidade(
        self,
        comunidade_id: str,
    ) -> list[VendedorComProdutosResponse]:
        vendedores = await self.repository.get_vendedores_ativos_por_comunidade(comunidade_id)
        vendedores_payload: list[VendedorComProdutosResponse] = []

        for vendedor in vendedores:
            produtos = await self.repository.get_produtos_vendedor_ordenado(vendedor.id)
            horarios = await self.repository.list_horarios_vendedor(vendedor.id)
            vendedores_payload.append(map_vendedor_com_produtos(vendedor, produtos, horarios))

        return vendedores_payload

    async def get_catalogo_produtos_por_comunidade(
        self,
        comunidade_id: str,
    ) -> list[ProdutoComunidadeResponse]:
        produtos_vendedores = await self.repository.get_produtos_vendedores_por_comunidade(comunidade_id)
        return map_catalogo_comunidade(produtos_vendedores)

    async def get_produtos_vendedor_por_id(self, vendedor_id: str) -> VendedorComProdutosResponse:
        vendedor = await self.repository.find_read_by_id_ativo(vendedor_id)
        if not vendedor:
            raise DomainError("Vendedor nao encontrado", code=404)

        produtos = await self.repository.get_produtos_vendedor_ordenado(vendedor.id)
        horarios = await self.repository.list_horarios_vendedor(vendedor.id)
        return map_vendedor_com_produtos(vendedor, produtos, horarios)

    async def get_meus_produtos_vendedor(self, usuario_id: str) -> VendedorComProdutosResponse:
        vendedor = await self.repository.find_read_by_usuario_id(usuario_id)
        if not vendedor:
            raise DomainError("Vendedor nao encontrado", code=404)

        produtos = await self.repository.get_produtos_vendedor_ordenado(vendedor.id)
        horarios = await self.repository.list_horarios_vendedor(vendedor.id)
        return map_vendedor_com_produtos(vendedor, produtos, horarios)

    def _validar_intervalo_horario(self, hora_inicio: str, hora_fim: str, todo_tempo: bool) -> None:
        if todo_tempo:
            return

        try:
            inicio = datetime.strptime(hora_inicio, "%H:%M")
            fim = datetime.strptime(hora_fim, "%H:%M")
        except ValueError:
            raise DomainError("Formato de hora invalido. Use HH:MM", code=400)

        if inicio >= fim:
            raise DomainError("hora_inicio deve ser menor que hora_fim", code=400)
