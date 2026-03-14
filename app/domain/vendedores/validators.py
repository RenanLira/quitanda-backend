from app.database.repositories.produto import get_produto_repository


async def produto_existe(produto_id: str) -> str:
    repository = await get_produto_repository()

    produto = await repository.find_by_id(produto_id)

    if not produto:
        raise ValueError(f"Produto com id {produto_id} não existe")
    
    return produto_id