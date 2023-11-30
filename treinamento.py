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
        self.detalhe(f'SAQUE NEGADO!!!')


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
        return self._checar_agencias(conta),\
        self._checar_clientes(cliente),\
        self._checar_contas(conta), \
        self._checar_se_conta_e_do_cliente(cliente, conta)
    
    def __repr__(self):
        class_name = type(self).__name__
        attr = f'Agencias: {self.agencias!r} Clientes: {self.clientes!r}'\
            f'Contas: {self.contas!r}'
        return f'{class_name} ({attr})'


#MAIN
cliente1 = Cliente('Flauzino', 30)
cliente2 = Cliente('Maria', 72)
cliente3 = Cliente('Fernanda', 22)
contacc1 = ContaCorrente(111, 255, 0, 0)
contacc2 = ContaCorrente(221, 566, 0, 400)
contapc3 = ContaPoupanca(655, 551)
cliente1.conta = contacc1
cliente2.conta = contacc2
cliente3.conta = contapc3

banco = Banco()
banco.clientes.extend([cliente1, cliente2, cliente3])
banco.agencias.extend([111, 221, 655])
banco.contas.extend([contacc1, contacc2, contapc3])

print('~'*50)
print(f'CLIENTE 1 {cliente1}'.center(50))
print('~'*50)
if banco.autenticar(cliente1, contacc1):
    contacc1.sacar(500)
    contacc1.depositar(600)
    contacc1.sacar(500)

print('~'*50)    
print(f'CLIENTE 2 {cliente2}'.center(50))
print('~'*50)
if banco.autenticar(cliente2, contacc2):
    contacc2.depositar(1700)
    cliente2.conta.depositar(300)
    cliente2.conta.sacar(2400)

print('~'*50)
print(f'CLIENTE 3 {cliente2}'.center(50))
print('~'*50)
if banco.autenticar(cliente3, contapc3):
    cliente3.conta.depositar(1700)
    cliente3.conta.sacar(1500)