from app.http.schemas.comunidades import ComunidadeResumoResponse


def map_comunidade_resumo(comunidade) -> ComunidadeResumoResponse:
    return ComunidadeResumoResponse(
        id=comunidade.id,
        nome=comunidade.nome,
        nome_slug=comunidade.nome_slug,
        descricao_curta=comunidade.descricao_curta,
        descricao_longa=comunidade.descricao_longa,
        cor_tema=comunidade.cor_tema,
        tipo=comunidade.tipo.value,
        imagem_url=comunidade.imagem_url,
        ativo=comunidade.ativo,
    )
