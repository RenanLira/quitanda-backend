
from sqlalchemy import case, exists, select

from app.database.models.comunidade import HorarioFuncionamentoModel, ProdutoVendedorModel, VendedorModel
from app.database.models.produto import ProdutoModel
from app.database.models.usuario import UsuarioModel
from app.domain.vendedores.horario_funcionamento import HorarioFuncionamento
from app.domain.vendedores.interfaces.vendedor_repository import VendedorRepository
from app.domain.vendedores.produto_vendedor import ProdutoVendedor, ProdutoVendedorComProdutoInfo, StatusProduto
from app.domain.vendedores.read_models import HorarioFuncionamentoReadInfo, VendedorReadInfo
from app.domain.vendedores.vendedor import Vendedor
from sqlalchemy.ext.asyncio import AsyncSession

class VendedorRepositoryImpl(VendedorRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, vendedor: Vendedor) -> None:
        vendedor_model = VendedorModel(**vendedor.model_dump())
        self.session.add(vendedor_model)

        await self.session.commit()
    
    async def find_read_by_id_ativo(self, vendedor_id: str) -> VendedorReadInfo | None:
        vendedor_tem_horario = exists(
            select(HorarioFuncionamentoModel.id).where(HorarioFuncionamentoModel.vendedor_id == VendedorModel.id)
        )
        result = await self.session.execute(
            select(VendedorModel)
            .join(UsuarioModel, UsuarioModel.id == VendedorModel.usuario_id)
            .where(VendedorModel.id == vendedor_id)
            .where(UsuarioModel.ativo.is_(True))
            .where(vendedor_tem_horario)
        )
        vendedor_model = result.scalars().first()
        if not vendedor_model:
            return None

        return VendedorReadInfo(
            id=vendedor_model.id,
            usuario_id=vendedor_model.usuario_id,
            comunidade_id=vendedor_model.comunidade_id,
            nome_fantasia=vendedor_model.nome_fantasia,
            nome_fantasia_slug=vendedor_model.nome_fantasia_slug,
            descricao=vendedor_model.descricao,
            horarios_funcionamento=await self.list_horarios_vendedor(vendedor_model.id),
        )

    async def find_read_by_usuario_id(self, usuario_id: str) -> VendedorReadInfo | None:
        result = await self.session.execute(
            select(VendedorModel)
            .where(VendedorModel.usuario_id == usuario_id)
        )
        vendedor_model = result.scalars().first()
        if not vendedor_model:
            return None

        return VendedorReadInfo(
            id=vendedor_model.id,
            usuario_id=vendedor_model.usuario_id,
            comunidade_id=vendedor_model.comunidade_id,
            nome_fantasia=vendedor_model.nome_fantasia,
            nome_fantasia_slug=vendedor_model.nome_fantasia_slug,
            descricao=vendedor_model.descricao,
            horarios_funcionamento=await self.list_horarios_vendedor(vendedor_model.id),
        )


    async def get_vendedores_ativos_por_comunidade(self, comunidade_id: str) -> list[VendedorReadInfo]:
        vendedor_tem_horario = exists(
            select(HorarioFuncionamentoModel.id).where(HorarioFuncionamentoModel.vendedor_id == VendedorModel.id)
        )
        result = await self.session.execute(
            select(VendedorModel)
            .join(UsuarioModel, UsuarioModel.id == VendedorModel.usuario_id)
            .where(VendedorModel.comunidade_id == comunidade_id)
            .where(UsuarioModel.ativo.is_(True))
            .where(vendedor_tem_horario)
        )
        vendedores = result.scalars().all()
        return [
            VendedorReadInfo(
                id=vendedor_model.id,
                usuario_id=vendedor_model.usuario_id,
                comunidade_id=vendedor_model.comunidade_id,
                nome_fantasia=vendedor_model.nome_fantasia,
                nome_fantasia_slug=vendedor_model.nome_fantasia_slug,
                descricao=vendedor_model.descricao,
                horarios_funcionamento=await self.list_horarios_vendedor(vendedor_model.id),
            )
            for vendedor_model in vendedores
        ]

    async def get_produtos_vendedor_ordenado(
        self,
        vendedor_id: str,
    ) -> list[ProdutoVendedorComProdutoInfo]:
        result = await self.session.execute(
            select(
                ProdutoVendedorModel.id,
                ProdutoVendedorModel.vendedor_id,
                ProdutoVendedorModel.produto_id,
                ProdutoModel.nome,
                ProdutoModel.descricao,
                ProdutoModel.tipo_unidade,
                ProdutoVendedorModel.preco,
                ProdutoVendedorModel.estoque,
                ProdutoVendedorModel.status,
            )
            .join(ProdutoModel, ProdutoModel.id == ProdutoVendedorModel.produto_id)
            .where(ProdutoVendedorModel.vendedor_id == vendedor_id)
            .where(ProdutoVendedorModel.ativo.is_(True))
            .where(ProdutoVendedorModel.status.in_([StatusProduto.DISPONIVEL, StatusProduto.ESGOTADO]))
            .order_by(
                case(
                    (ProdutoVendedorModel.status == StatusProduto.DISPONIVEL, 0),
                    (ProdutoVendedorModel.status == StatusProduto.ESGOTADO, 1),
                    else_=2,
                ),
            )
        )

        return [
            ProdutoVendedorComProdutoInfo(
                produto_vendedor_id=produto_vendedor_id,
                vendedor_id=vendedor_id,
                produto_id=produto_id,
                produto_nome=produto_nome,
                produto_descricao=produto_descricao,
                tipo_unidade=tipo_unidade.value,
                preco=preco,
                estoque=estoque,
                status=status.value,
            )
            for (
                produto_vendedor_id,
                vendedor_id,
                produto_id,
                produto_nome,
                produto_descricao,
                tipo_unidade,
                preco,
                estoque,
                status,
            ) in result.all()
        ]

    async def get_produtos_vendedores_por_comunidade(
        self,
        comunidade_id: str,
    ) -> list[ProdutoVendedorComProdutoInfo]:
        vendedor_tem_horario = exists(
            select(HorarioFuncionamentoModel.id).where(HorarioFuncionamentoModel.vendedor_id == VendedorModel.id)
        )
        result = await self.session.execute(
            select(
                ProdutoVendedorModel.id,
                ProdutoVendedorModel.vendedor_id,
                ProdutoVendedorModel.produto_id,
                ProdutoModel.nome,
                ProdutoModel.descricao,
                ProdutoModel.tipo_unidade,
                ProdutoVendedorModel.preco,
                ProdutoVendedorModel.estoque,
                ProdutoVendedorModel.status,
            )
            .join(VendedorModel, VendedorModel.id == ProdutoVendedorModel.vendedor_id)
            .join(UsuarioModel, UsuarioModel.id == VendedorModel.usuario_id)
            .join(ProdutoModel, ProdutoModel.id == ProdutoVendedorModel.produto_id)
            .where(VendedorModel.comunidade_id == comunidade_id)
            .where(UsuarioModel.ativo.is_(True))
            .where(vendedor_tem_horario)
            .where(ProdutoVendedorModel.ativo.is_(True))
            .where(ProdutoVendedorModel.status.in_([StatusProduto.DISPONIVEL, StatusProduto.ESGOTADO]))
            .order_by(
                ProdutoModel.nome,
                case(
                    (ProdutoVendedorModel.status == StatusProduto.DISPONIVEL, 0),
                    (ProdutoVendedorModel.status == StatusProduto.ESGOTADO, 1),
                    else_=2,
                ),
            )
        )

        return [
            ProdutoVendedorComProdutoInfo(
                produto_vendedor_id=produto_vendedor_id,
                vendedor_id=vendedor_id,
                produto_id=produto_id,
                produto_nome=produto_nome,
                produto_descricao=produto_descricao,
                tipo_unidade=tipo_unidade.value,
                preco=preco,
                estoque=estoque,
                status=status.value,
            )
            for (
                produto_vendedor_id,
                vendedor_id,
                produto_id,
                produto_nome,
                produto_descricao,
                tipo_unidade,
                preco,
                estoque,
                status,
            ) in result.all()
        ]

    async def add_produto_vendedor(self, produto_vendedor: ProdutoVendedor) -> None:
        self.session.add(ProdutoVendedorModel(**produto_vendedor.model_dump()))
        await self.session.commit()

    async def add_horario_funcionamento(self, horario: HorarioFuncionamento) -> None:
        self.session.add(HorarioFuncionamentoModel(**horario.model_dump()))
        await self.session.commit()

    async def update_horario_funcionamento(self, horario: HorarioFuncionamento) -> None:
        horario_model = await self.session.get(HorarioFuncionamentoModel, horario.id)
        if not horario_model:
            return

        horario_model.dia_semana = horario.dia_semana
        horario_model.hora_inicio = horario.hora_inicio
        horario_model.hora_fim = horario.hora_fim
        horario_model.todo_tempo = horario.todo_tempo

        await self.session.commit()

    async def find_horario_by_id_vendedor(
        self,
        horario_id: str,
        vendedor_id: str,
    ) -> HorarioFuncionamento | None:
        result = await self.session.execute(
            select(HorarioFuncionamentoModel)
            .where(HorarioFuncionamentoModel.id == horario_id)
            .where(HorarioFuncionamentoModel.vendedor_id == vendedor_id)
        )
        horario_model = result.scalars().first()
        if not horario_model:
            return None

        return HorarioFuncionamento.model_validate(horario_model, from_attributes=True)

    async def list_horarios_vendedor(self, vendedor_id: str) -> list[HorarioFuncionamentoReadInfo]:
        result = await self.session.execute(
            select(HorarioFuncionamentoModel)
            .where(HorarioFuncionamentoModel.vendedor_id == vendedor_id)
            .order_by(HorarioFuncionamentoModel.dia_semana, HorarioFuncionamentoModel.hora_inicio)
        )
        horarios_model = result.scalars().all()
        return [
            HorarioFuncionamentoReadInfo.model_validate(horario_model, from_attributes=True)
            for horario_model in horarios_model
        ]