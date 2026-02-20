

class VendedorService():
    def __init__(self, repository):
        self.repository = repository

    def criar_vendedor(self, nome, email):
        # Lógica para criar um novo vendedor
        vendedor = {
            'nome': nome,
            'email': email
        }
        return self.repository.save(vendedor)

    def obter_vendedor(self, vendedor_id):
        # Lógica para obter um vendedor pelo ID
        return self.repository.get_by_id(vendedor_id)

    def atualizar_vendedor(self, vendedor_id, nome=None, email=None):
        # Lógica para atualizar as informações de um vendedor
        vendedor = self.repository.get_by_id(vendedor_id)
        if not vendedor:
            return None
        if nome:
            vendedor['nome'] = nome
        if email:
            vendedor['email'] = email
        return self.repository.update(vendedor_id, vendedor)

    def deletar_vendedor(self, vendedor_id):
        # Lógica para deletar um vendedor
        return self.repository.delete(vendedor_id)