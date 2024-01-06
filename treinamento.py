from abc import ABC, abstractmethod


class Conta(ABC):
    def __init__(self, agencia, conta, saldo=0):
        self.agencia = agencia
        self.conta = conta
        self.saldo = saldo

    @abstractmethod
    def sacar(self, valor):
        pass

    def depositar(self, valor):
        self.saldo += valor
        self.detalhe(f'DEPOSITO CONCLUIDO {valor:.2f} R$')

    def detalhe(self, msg=''):
        print(f'O seu saldo é de {self.saldo:.2f} R$ {msg}')

    def __repr__(self):
        class_name = type(self).__name__
        attr = f'Agencia: {self.agencia!r} Conta: {self.conta!r}'\
            f' Saldo: {self.saldo!r}'
        return f'{class_name} ({attr})'


class ContaPoupanca(Conta):
    def sacar(self, valor):

        if valor <= self.saldo:
            self.saldo -= valor
            self.detalhe(f'SAQUE FEITO NO VALOR {valor:.2f} R$')
            return self.saldo

        print('Nao foi possivel realizar o saque!')
        self.detalhe('SAQUE NEGADO!!')


class ContaCorrente(Conta):
    def __init__(self, agencia, conta, saldo=0, limite=0):
        super().__init__(agencia, conta, saldo)
        self.limite = limite

    def sacar(self, valor):
        valor_pos_saque = self.saldo - valor
        limite_maximo = -self.limite

        if valor_pos_saque >= limite_maximo:
            self.saldo -= valor
            self.detalhe(f'SAQUE FEITO NO VALOR DE {valor:.2f} R$')
            return self.saldo

        print('Nao foi possivel realizar o saque!')
        print(f'Seu limite maximo é de {-self.limite:.2f} R$')
        self.detalhe('SAQUE NEGADO!!!')


class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    @property
    def nome(self):
        return self._nome

    @property
    def idade(self):
        return self._idade

    @nome.setter
    def nome(self, valor):
        self._nome = valor

    @idade.setter
    def idade(self, valor):
        self._idade = valor

    def __repr__(self):
        class_name = type(self).__name__
        attr = f'Nome: {self.nome!r} Idade: {self.idade!r}'
        return f'{class_name} ({attr})'


class Cliente(Pessoa):
    def __init__(self, nome, idade):
        super().__init__(nome, idade)
        self.conta = Conta | None


class Banco:
    def __init__(
            self,
            agencias: list[int] | None = None,
            clientes: list[Pessoa] | None = None,
            contas: list[Conta] | None = None,
    ):
        self.agencias = agencias or []
        self.clientes = clientes or []
        self.contas = contas or []

    def _checar_agencias(self, conta):
        if conta.agencia in self.agencias:
            return True
        return False

    def _checar_clientes(self, cliente):
        if cliente in self.clientes:
            return True
        return False

    def _checar_contas(self, conta):
        if conta in self.contas:
            return True
        return False

    def _checar_se_conta_e_do_cliente(self, cliente, conta):
        if conta is cliente.conta:
            return True
        return False

    def autenticar(self, cliente: Pessoa, conta: Conta):
        return self._checar_agencias(conta), \
               self._checar_clientes(cliente), \
               self._checar_contas(conta), \
               self._checar_se_conta_e_do_cliente(cliente, conta)

    def __repr__(self):
        class_name = type(self).__name__
        attr = f'Agencias: {self.agencias!r} Clientes: {self.clientes!r}'\
            f'Contas: {self.contas!r}'
        return f'{class_name} ({attr})'


# Adicionado padrao facade para deixar mais simples a usabilidade
# do codigo
class BancoFacade:
    def __init__(self):
        self.banco = Banco()

    def cadastrar_cliente(self, nome, idade):
        cliente = Cliente(nome, idade)
        return cliente

    def criar_conta_corrente(self, agencia, numero, saldo, limite=0):
        conta = ContaCorrente(agencia, numero, saldo, limite)
        return conta

    def criar_conta_poupanca(self, agencia, numero, saldo):
        conta = ContaPoupanca(agencia, numero, saldo)
        return conta

    def associar_conta(self, cliente: Cliente, conta):
        cliente.conta = conta

    def adicionar_clientes(self, clientes):
        return self.banco.clientes.extend(clientes)

    def adicionar_agencias(self, agencias):
        return self.banco.agencias.extend(agencias)

    def adicionar_contas(self, contas):
        return self.banco.contas.extend(contas)

    def autenticar(self, cliente: Pessoa, conta: Conta):
        if self.banco.autenticar(cliente, conta):
            if cliente.conta == conta:
                print(f'{cliente} autenticado com sucesso!')
                return True
        print(
            f'Nao foi possivel autenticar o cliente {cliente}\n'
            'Pois a conta informada nao pertence a ele!'
            )
        return False


# MAIN
if __name__ == '__main__':
    f_facade = BancoFacade()

    # Cria clientes
    cliente1 = f_facade.cadastrar_cliente('Joao', 40)
    cliente2 = f_facade.cadastrar_cliente('Fernanda', 35)
    cliente3 = f_facade.cadastrar_cliente('Eduarda', 22)

    # Cria contas
    conta1 = f_facade.criar_conta_corrente(151, 266, 500, 1000)
    conta2 = f_facade.criar_conta_corrente(111, 296, 300, 200)
    conta3 = f_facade.criar_conta_poupanca(101, 200, 700)

    # Associa conta com cliente
    f_facade.associar_conta(cliente1, conta1)
    f_facade.associar_conta(cliente2, conta2)
    f_facade.associar_conta(cliente3, conta3)

    # Adiciona clientes, agencias e contas a classe Banco
    # (instanciada internamente na classe de fachada)
    f_facade.adicionar_clientes([cliente1, cliente2, cliente3])
    f_facade.adicionar_agencias([151, 111, 101])
    f_facade.adicionar_contas([conta1, conta2, conta3])

    # Autentica cliente1
    if f_facade.autenticar(cliente1, conta1):
        cliente1.conta.depositar(600)
        cliente1.conta.sacar(2100)
        cliente1.conta.sacar(50)
        print()
    # Autentica cliente2
    if f_facade.autenticar(cliente2, conta2):
        cliente2.conta.depositar(600)
        cliente2.conta.sacar(50)
        cliente2.conta.sacar(1000)
        cliente2.conta.sacar(50)
        cliente2.conta.sacar(50)
        print()
    # Autentica cliente3
    if f_facade.autenticar(cliente3, conta3):
        cliente3.conta.depositar(600)
        cliente3.conta.sacar(50)
        cliente3.conta.sacar(1000)
        cliente3.conta.sacar(50)
        cliente3.conta.sacar(50)
        print()
