from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from decimal import Decimal
from uuid import uuid7

import bcrypt
from sqlalchemy import text

from app.database import sessionmanager
from app.database.models.comunidade import ComunidadeModel, ProdutoVendedorModel, VendedorModel
from app.database.models.endereco import EnderecoModel
from app.database.models.pedido import PedidoItemModel, PedidoModel
from app.database.models.produto import ProdutoModel
from app.database.models.usuario import TokenModel, UsuarioModel
from app.domain.auth.enums.token_type import TokenType
from app.domain.comunidades.types.tipo_comunidade import TipoComunidade
from app.domain.pedidos.pedido import StatusPedido
from app.domain.produtos.produto import TipoUnidade
from app.domain.usuarios.usuario import ETipoUsuario
from app.domain.vendedores.produto_vendedor import StatusProduto


TABLES_IN_RESET_ORDER = [
    "pedido_itens",
    "pedidos",
    "horarios_funcionamento",
    "produtos_vendedores",
    "vendedores",
    "enderecos",
    "tokens",
    "produtos",
    "comunidades",
    "usuarios",
]


def _hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


async def seed_database(reset: bool = True) -> None:
    async with sessionmanager.session() as session:
        if reset:
            await session.execute(text(f"TRUNCATE TABLE {', '.join(TABLES_IN_RESET_ORDER)} CASCADE"))

        now = datetime.now()
        password_hash = _hash_password("123456")

        # Usuarios
        admin_id = str(uuid7())
        cliente_1_id = str(uuid7())
        cliente_2_id = str(uuid7())
        vendedor_user_1_id = str(uuid7())
        vendedor_user_2_id = str(uuid7())
        vendedor_user_3_id = str(uuid7())

        usuarios = [
            UsuarioModel(
                id=admin_id,
                nome="Admin Quitanda",
                email="admin@quitanda.local",
                password_hash=password_hash,
                telefone="11900000001",
                tipo=ETipoUsuario.ADMIN,
                ativo=True,
            ),
            UsuarioModel(
                id=cliente_1_id,
                nome="Cliente Ativo 1",
                email="cliente1@quitanda.local",
                password_hash=password_hash,
                telefone="11900000002",
                tipo=ETipoUsuario.CLIENTE,
                ativo=True,
            ),
            UsuarioModel(
                id=cliente_2_id,
                nome="Cliente Ativo 2",
                email="cliente2@quitanda.local",
                password_hash=password_hash,
                telefone="11900000003",
                tipo=ETipoUsuario.CLIENTE,
                ativo=True,
            ),
            UsuarioModel(
                id=vendedor_user_1_id,
                nome="Usuario Vendedor 1",
                email="vendedor1@quitanda.local",
                password_hash=password_hash,
                telefone="11900000004",
                tipo=ETipoUsuario.VENDEDOR,
                ativo=True,
            ),
            UsuarioModel(
                id=vendedor_user_2_id,
                nome="Usuario Vendedor 2",
                email="vendedor2@quitanda.local",
                password_hash=password_hash,
                telefone="11900000005",
                tipo=ETipoUsuario.VENDEDOR,
                ativo=True,
            ),
            UsuarioModel(
                id=vendedor_user_3_id,
                nome="Usuario Vendedor Inativo",
                email="vendedor3@quitanda.local",
                password_hash=password_hash,
                telefone="11900000006",
                tipo=ETipoUsuario.VENDEDOR,
                ativo=False,
            ),
        ]

        session.add_all(usuarios)
        await session.flush()

        # Comunidades
        comunidade_ativa_id = str(uuid7())
        comunidade_inativa_id = str(uuid7())

        comunidades = [
            ComunidadeModel(
                id=comunidade_ativa_id,
                nome="Comunidade Feira Centro",
                nome_slug="comunidade-feira-centro",
                descricao_curta="Feira com produtores locais",
                descricao_longa="Comunidade principal para testes de endpoints",
                cor_tema="#059669",
                tipo=TipoComunidade.FEIRA,
                imagem_url=None,
                ativo=True,
            ),
            ComunidadeModel(
                id=comunidade_inativa_id,
                nome="Comunidade Mercado Bairro",
                nome_slug="comunidade-mercado-bairro",
                descricao_curta="Mercado de bairro",
                descricao_longa="Comunidade secundaria inativa",
                cor_tema="#0ea5e9",
                tipo=TipoComunidade.MERCADO,
                imagem_url=None,
                ativo=False,
            ),
        ]

        session.add_all(comunidades)
        await session.flush()

        # Enderecos
        enderecos = [
            EnderecoModel(
                id=str(uuid7()),
                usuario_id=admin_id,
                comunidade_id=None,
                latitude=-23.55052,
                longitude=-46.633308,
                cep="01001-000",
                cidade="Sao Paulo",
                rua="Rua Administrador",
                numero="100",
                bairro="Centro",
                estado="SP",
            ),
            EnderecoModel(
                id=str(uuid7()),
                usuario_id=cliente_1_id,
                comunidade_id=None,
                latitude=-23.551,
                longitude=-46.632,
                cep="01002-000",
                cidade="Sao Paulo",
                rua="Rua Cliente 1",
                numero="101",
                bairro="Centro",
                estado="SP",
            ),
            EnderecoModel(
                id=str(uuid7()),
                usuario_id=cliente_2_id,
                comunidade_id=None,
                latitude=-23.552,
                longitude=-46.631,
                cep="01003-000",
                cidade="Sao Paulo",
                rua="Rua Cliente 2",
                numero="102",
                bairro="Centro",
                estado="SP",
            ),
            EnderecoModel(
                id=str(uuid7()),
                usuario_id=vendedor_user_1_id,
                comunidade_id=None,
                latitude=-23.553,
                longitude=-46.630,
                cep="01004-000",
                cidade="Sao Paulo",
                rua="Rua Vendedor 1",
                numero="103",
                bairro="Centro",
                estado="SP",
            ),
            EnderecoModel(
                id=str(uuid7()),
                usuario_id=vendedor_user_2_id,
                comunidade_id=None,
                latitude=-23.554,
                longitude=-46.629,
                cep="01005-000",
                cidade="Sao Paulo",
                rua="Rua Vendedor 2",
                numero="104",
                bairro="Centro",
                estado="SP",
            ),
            EnderecoModel(
                id=str(uuid7()),
                usuario_id=vendedor_user_3_id,
                comunidade_id=None,
                latitude=-23.555,
                longitude=-46.628,
                cep="01006-000",
                cidade="Sao Paulo",
                rua="Rua Vendedor 3",
                numero="105",
                bairro="Centro",
                estado="SP",
            ),
            EnderecoModel(
                id=str(uuid7()),
                usuario_id=None,
                comunidade_id=comunidade_ativa_id,
                latitude=-23.549,
                longitude=-46.634,
                cep="01007-000",
                cidade="Sao Paulo",
                rua="Praca da Feira",
                numero="200",
                bairro="Centro",
                estado="SP",
            ),
            EnderecoModel(
                id=str(uuid7()),
                usuario_id=None,
                comunidade_id=comunidade_inativa_id,
                latitude=-23.548,
                longitude=-46.635,
                cep="01008-000",
                cidade="Sao Paulo",
                rua="Rua Mercado",
                numero="201",
                bairro="Centro",
                estado="SP",
            ),
        ]

        session.add_all(enderecos)
        await session.flush()

        # Vendedores
        vendedor_1_id = str(uuid7())
        vendedor_2_id = str(uuid7())
        vendedor_3_id = str(uuid7())

        vendedores = [
            VendedorModel(
                id=vendedor_1_id,
                usuario_id=vendedor_user_1_id,
                comunidade_id=comunidade_ativa_id,
                nome_fantasia="Horta do Joao",
                nome_fantasia_slug="horta-do-joao",
                descricao="Verduras e frutas frescas",
                chave_pix="11111111111",
            ),
            VendedorModel(
                id=vendedor_2_id,
                usuario_id=vendedor_user_2_id,
                comunidade_id=comunidade_ativa_id,
                nome_fantasia="Sacolao da Maria",
                nome_fantasia_slug="sacolao-da-maria",
                descricao="Produtos selecionados",
                chave_pix="22222222222",
            ),
            VendedorModel(
                id=vendedor_3_id,
                usuario_id=vendedor_user_3_id,
                comunidade_id=comunidade_ativa_id,
                nome_fantasia="Banca Inativa",
                nome_fantasia_slug="banca-inativa",
                descricao="Nao deve aparecer nas listagens de ativos",
                chave_pix="33333333333",
            ),
        ]

        session.add_all(vendedores)
        await session.flush()

        # Produtos base
        produto_banana_id = str(uuid7())
        produto_maca_id = str(uuid7())
        produto_leite_id = str(uuid7())
        produto_arroz_id = str(uuid7())

        produtos = [
            ProdutoModel(
                id=produto_banana_id,
                nome="Banana Nanica",
                descricao="Banana doce por kg",
                tipo_unidade=TipoUnidade.KG,
                imagem_url=None,
            ),
            ProdutoModel(
                id=produto_maca_id,
                nome="Maca Gala",
                descricao="Maca selecionada",
                tipo_unidade=TipoUnidade.KG,
                imagem_url=None,
            ),
            ProdutoModel(
                id=produto_leite_id,
                nome="Leite Integral",
                descricao="Leite integral 1L",
                tipo_unidade=TipoUnidade.LITRO,
                imagem_url=None,
            ),
            ProdutoModel(
                id=produto_arroz_id,
                nome="Arroz Tipo 1",
                descricao="Arroz pacote 5kg",
                tipo_unidade=TipoUnidade.PACOTE,
                imagem_url=None,
            ),
        ]

        session.add_all(produtos)
        await session.flush()

        # Produtos por vendedor
        pv_1_id = str(uuid7())
        pv_2_id = str(uuid7())
        pv_3_id = str(uuid7())
        pv_4_id = str(uuid7())
        pv_5_id = str(uuid7())
        pv_6_id = str(uuid7())
        pv_7_id = str(uuid7())

        produtos_vendedores = [
            ProdutoVendedorModel(
                id=pv_1_id,
                vendedor_id=vendedor_1_id,
                produto_id=produto_banana_id,
                preco=Decimal("7.90"),
                estoque=40,
                status=StatusProduto.DISPONIVEL,
                ativo=True,
            ),
            ProdutoVendedorModel(
                id=pv_2_id,
                vendedor_id=vendedor_1_id,
                produto_id=produto_maca_id,
                preco=Decimal("12.50"),
                estoque=0,
                status=StatusProduto.ESGOTADO,
                ativo=True,
            ),
            ProdutoVendedorModel(
                id=pv_3_id,
                vendedor_id=vendedor_1_id,
                produto_id=produto_leite_id,
                preco=Decimal("5.99"),
                estoque=20,
                status=StatusProduto.INDISPONIVEL,
                ativo=True,
            ),
            ProdutoVendedorModel(
                id=pv_4_id,
                vendedor_id=vendedor_2_id,
                produto_id=produto_banana_id,
                preco=Decimal("8.20"),
                estoque=12,
                status=StatusProduto.DISPONIVEL,
                ativo=True,
            ),
            ProdutoVendedorModel(
                id=pv_5_id,
                vendedor_id=vendedor_2_id,
                produto_id=produto_arroz_id,
                preco=Decimal("28.90"),
                estoque=0,
                status=StatusProduto.ESGOTADO,
                ativo=True,
            ),
            ProdutoVendedorModel(
                id=pv_6_id,
                vendedor_id=vendedor_2_id,
                produto_id=produto_maca_id,
                preco=Decimal("13.50"),
                estoque=14,
                status=StatusProduto.INDISPONIVEL,
                ativo=True,
            ),
            ProdutoVendedorModel(
                id=pv_7_id,
                vendedor_id=vendedor_3_id,
                produto_id=produto_banana_id,
                preco=Decimal("6.90"),
                estoque=8,
                status=StatusProduto.DISPONIVEL,
                ativo=True,
            ),
        ]

        session.add_all(produtos_vendedores)
        await session.flush()

        # Pedidos
        pedido_1_id = str(uuid7())
        pedido_2_id = str(uuid7())

        pedidos = [
            PedidoModel(
                id=pedido_1_id,
                cliente_id=cliente_1_id,
                vendedor_id=vendedor_1_id,
                comunidade_id=comunidade_ativa_id,
                status=StatusPedido.PENDENTE,
                motivo_recusa=None,
                valor_total=Decimal("15.80"),
                criado_em=now,
                atualizado_em=now,
                aprovado_em=None,
                recusado_em=None,
            ),
            PedidoModel(
                id=pedido_2_id,
                cliente_id=cliente_2_id,
                vendedor_id=vendedor_2_id,
                comunidade_id=comunidade_ativa_id,
                status=StatusPedido.RECUSADO,
                motivo_recusa="Sem estoque no momento",
                valor_total=Decimal("28.90"),
                criado_em=now - timedelta(hours=2),
                atualizado_em=now - timedelta(hours=1, minutes=30),
                aprovado_em=None,
                recusado_em=now - timedelta(hours=1, minutes=30),
            ),
        ]

        session.add_all(pedidos)
        await session.flush()

        pedido_itens = [
            PedidoItemModel(
                id=str(uuid7()),
                pedido_id=pedido_1_id,
                produto_vendedor_id=pv_1_id,
                quantidade=2,
                preco_unitario=Decimal("7.90"),
                valor_total_item=Decimal("15.80"),
            ),
            PedidoItemModel(
                id=str(uuid7()),
                pedido_id=pedido_2_id,
                produto_vendedor_id=pv_5_id,
                quantidade=1,
                preco_unitario=Decimal("28.90"),
                valor_total_item=Decimal("28.90"),
            ),
        ]

        session.add_all(pedido_itens)
        await session.flush()

        # Token de exemplo para inspeção de dados
        token_demo = TokenModel(
            id=str(uuid7()),
            user_id=admin_id,
            token_type=TokenType.ACCESS,
            expires_at=now + timedelta(hours=1),
        )
        session.add(token_demo)

        await session.commit()

    print("Seed concluido com sucesso.")
    print("Usuarios de teste (senha para todos: 123456):")
    print("- admin@quitanda.local (ADMIN)")
    print("- cliente1@quitanda.local (CLIENTE)")
    print("- cliente2@quitanda.local (CLIENTE)")
    print("- vendedor1@quitanda.local (VENDEDOR ativo)")
    print("- vendedor2@quitanda.local (VENDEDOR ativo)")
    print("- vendedor3@quitanda.local (VENDEDOR inativo)")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Seed do banco para testes de endpoints")
    parser.add_argument(
        "--no-reset",
        action="store_true",
        help="Nao limpa as tabelas antes de inserir dados",
    )
    args = parser.parse_args()

    await seed_database(reset=not args.no_reset)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
