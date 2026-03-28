from app.domain.enderecos.endereco import Endereco
from app.http.schemas.enderecos import EnderecoResponse


def map_endereco(endereco: Endereco) -> EnderecoResponse:
    return EnderecoResponse(
        id=endereco.id,
        usuario_id=endereco.usuario_id,
        comunidade_id=endereco.comunidade_id,
        latitude=endereco.latitude,
        longitude=endereco.longitude,
        cep=endereco.cep,
        cidade=endereco.cidade,
        rua=endereco.rua,
        numero=endereco.numero,
        bairro=endereco.bairro,
        estado=endereco.estado,
    )
