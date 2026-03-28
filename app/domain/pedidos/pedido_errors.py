from app.domain.error import DomainError, NotFoundError


class PedidoNotFoundError(NotFoundError):
    def __init__(self, message: str = "Pedido nao encontrado", code: int = 404):
        super().__init__(message, code)


class PedidoItensInvalidosError(DomainError):
    def __init__(self, message: str = "Pedido deve possuir ao menos um item", code: int = 400):
        super().__init__(message, code)


class PedidoComunidadeInvalidaError(DomainError):
    def __init__(
        self,
        message: str = "Nao e permitido misturar produtos de comunidades diferentes no mesmo checkout",
        code: int = 400,
    ):
        super().__init__(message, code)


class PedidoProdutoVendedorInvalidoError(DomainError):
    def __init__(
        self,
        message: str = "Produto de vendedor invalido ou indisponivel para pedido",
        code: int = 400,
    ):
        super().__init__(message, code)


class PedidoStatusInvalidoError(DomainError):
    def __init__(self, message: str = "Transicao de status de pedido invalida", code: int = 400):
        super().__init__(message, code)
