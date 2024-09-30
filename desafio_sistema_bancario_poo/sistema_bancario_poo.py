import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import re

class Cliente:
    """
    Classe que representa um cliente do banco, contendo seu endereço e contas associadas.
    """
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        """
        Executa uma transação (depósito ou saque) em uma conta específica.
        """
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """
        Adiciona uma nova conta ao cliente.
        """
        self.contas.append(conta)


class PessoaFisica(Cliente):
    """
    Classe que representa um cliente Pessoa Física, herdando da classe Cliente.
    """
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    """
    Classe que representa uma conta bancária genérica.
    """
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        """
        Cria uma nova conta associada a um cliente.
        """
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        """
        Realiza um saque da conta, se o valor for válido e o saldo permitir.
        """
        if valor > self.saldo:
            print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
            return False
        if valor <= 0:
            print("\n@@@ Operação falhou! Valor inválido. @@@")
            return False

        self._saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor):
        """
        Realiza um depósito na conta, se o valor for válido.
        """
        if valor <= 0:
            print("\n@@@ Operação falhou! Valor inválido. @@@")
            return False

        self._saldo += valor
        print("\n=== Depósito realizado com sucesso! ===")
        return True


class ContaCorrente(Conta):
    """
    Classe que representa uma Conta Corrente, herdando da classe Conta, com limite de saque e número máximo de saques por dia.
    """
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        """
        Realiza o saque, verificando se o limite e o número de saques diários não foram excedidos.
        """
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        if valor > self._limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
            return False

        if numero_saques >= self._limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
            return False

        return super().sacar(valor)

    def __str__(self):
        """
        Retorna uma representação textual da conta corrente.
        """
        return f"Agência: {self.agencia}\nC/C: {self.numero}\nTitular: {self.cliente.nome}"


class Historico:
    """
    Classe que armazena o histórico de transações de uma conta.
    """
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        """
        Adiciona uma transação ao histórico, com o tipo, valor e data.
        """
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })


class Transacao(ABC):
    """
    Classe abstrata que define o contrato para diferentes tipos de transações.
    """
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    """
    Classe que representa a operação de saque.
    """
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        """
        Registra a operação de saque na conta.
        """
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    """
    Classe que representa a operação de depósito.
    """
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        """
        Registra a operação de depósito na conta.
        """
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


def validar_cpf(cpf):
    """
    Verifica se o CPF contém exatamente 11 dígitos numéricos.
    """
    return re.fullmatch(r'\d{11}', cpf)


def menu():
    """
    Exibe o menu de opções do sistema bancário.
    """
    menu_text = """\n
    ================ MENU ================
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova conta
    [lc] Listar contas
    [nu] Novo usuário
    [q] Sair
    => """
    return input(textwrap.dedent(menu_text))


def escolher_conta(cliente):
    """
    Permite que o cliente escolha uma de suas contas, caso tenha mais de uma.
    """
    if not cliente.contas:
        print("\n@@@ Cliente não possui contas! @@@")
        return None

    print("\nSelecione uma das contas:")
    for i, conta in enumerate(cliente.contas, 1):
        print(f"[{i}] Conta {conta.numero} - Agência {conta.agencia}")

    indice = int(input("Escolha o número da conta: "))
    try:
        return cliente.contas[indice - 1]
    except (IndexError, ValueError):
        print("\n@@@ Escolha inválida! @@@")
        return None


def filtrar_cliente(cpf, clientes):
    """
    Busca um cliente na lista de clientes pelo CPF.
    """
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def depositar(clientes):
    """
    Realiza um depósito em uma conta de um cliente existente.
    """
    cpf = input("Informe o CPF do cliente: ")
    if not validar_cpf(cpf):
        print("\n@@@ CPF inválido! @@@")
        return

    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    conta = escolher_conta(cliente)
    if not conta:
        return

    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    """
    Realiza um saque em uma conta de um cliente existente.
    """
    cpf = input("Informe o CPF do cliente: ")
    if not validar_cpf(cpf):
        print("\n@@@ CPF inválido! @@@")
        return

    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    conta = escolher_conta(cliente)
    if not conta:
        return

    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    """
    Exibe o extrato de uma conta de um cliente existente.
    """
    cpf = input("Informe o CPF do cliente: ")
    if not validar_cpf(cpf):
        print("\n@@@ CPF inválido! @@@")
        return

    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = escolher_conta(cliente)
    if not conta:
        return

    print("\n=============== EXTRATO ===============")
    transacoes = conta.historico.transacoes

    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            print(f"\n{transacao['tipo']} - R$ {transacao['valor']:.2f} - {transacao['data']}")

    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("========================================")


def criar_nova_conta(numero_conta, clientes):
    """
    Cria uma nova conta corrente para um cliente existente.
    """
    cpf = input("Informe o CPF do cliente: ")
    if not validar_cpf(cpf):
        print("\n@@@ CPF inválido! @@@")
        return

    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    numero_conta += 1
    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    cliente.adicionar_conta(conta)

    print("\n=== Conta criada com sucesso! ===")
    print(conta)


def criar_novo_usuario(clientes):
    """
    Cria um novo cliente com os dados fornecidos.
    """
    cpf = input("Informe o CPF (somente números): ")
    if not validar_cpf(cpf):
        print("\n@@@ CPF inválido! @@@")
        return

    if filtrar_cliente(cpf, clientes):
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço: ")

    cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def listar_contas(clientes):
    """
    Lista todas as contas associadas a um cliente.
    """
    cpf = input("Informe o CPF do cliente: ")
    if not validar_cpf(cpf):
        print("\n@@@ CPF inválido! @@@")
        return

    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    if not cliente.contas:
        print("\n@@@ Cliente não possui contas! @@@")
    else:
        print("\n=== Contas do Cliente ===")
        for conta in cliente.contas:
            print(conta)


def main():
    """
    Função principal que controla o fluxo do sistema bancário.
    """
    clientes = []
    numero_conta = 0

    while True:
        opcao = menu()

        if opcao == 'd':
            depositar(clientes)

        elif opcao == 's':
            sacar(clientes)

        elif opcao == 'e':
            exibir_extrato(clientes)

        elif opcao == 'nc':
            criar_nova_conta(numero_conta, clientes)

        elif opcao == 'lc':
            listar_contas(clientes)

        elif opcao == 'nu':
            criar_novo_usuario(clientes)

        elif opcao == 'q':
            break

        else:
            print("\n@@@ Operação inválida! Por favor, selecione novamente. @@@")


if __name__ == "__main__":
    main()
