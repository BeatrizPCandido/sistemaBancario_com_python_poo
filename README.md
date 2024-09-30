# sistemaBancario_com_python_poo
 **Criando um Sistema Bancário com Python com Programação Orientado a Obijeto**

 O projeto consiste em um sistema bancário simples, onde clientes podem criar contas, realizar depósitos, saques e consultar extratos. Ele é desenvolvido em Python e utiliza conceitos de Programação Orientada a Objetos, como herança, abstração e polimorfismo. O código é modular e segue boas práticas para garantir extensibilidade e fácil manutenção.

**Classes Principais:**

**Cliente:** Representa um cliente bancário, que pode ser uma pessoa física. Cada cliente pode ter múltiplas contas associadas.

**PessoaFisica (Cliente):** Herda de Cliente e adiciona atributos específicos de pessoas físicas, como nome, data_nascimento e cpf.

**Conta:** Representa uma conta bancária genérica com funcionalidades como depósito, saque e histórico de transações. Ela também mantém os atributos da conta, como o saldo, número e agência.

**ContaCorrente (Conta):** Herda de Conta e adiciona regras específicas, como limites de saque e quantidade de saques permitidos por dia.

**Historico:** Armazena todas as transações realizadas em uma conta, incluindo saques e depósitos, com a data e hora em que foram feitos.

**Transacao:** Classe abstrata que serve como base para as transações bancárias (saque e depósito). Cada transação deve ser registrada no histórico da conta.

**Saque e Deposito:** Implementam a classe Transacao, lidando com a lógica de registrar saques e depósitos.

**Fluxo do Programa:**

**Cadastro de Cliente:** O sistema permite cadastrar clientes com CPF único e endereço.

**Criação de Conta:** Após o cadastro, o cliente pode criar uma conta corrente, que vem com um limite de saque pré-definido e um número máximo de saques diários.

**Operações Bancárias:** O cliente pode realizar depósitos e saques em sua conta, com as devidas validações de saldo e limites. Todas as transações são registradas no histórico.

**Extrato Bancário:** O cliente pode solicitar o extrato de sua conta, que exibirá todas as transações realizadas e o saldo atual.

**Exemplos de Uso:**

**Criar Cliente e Conta:**

Após inserir o CPF e demais informações, um cliente pode ser criado e uma conta corrente associada a ele.

**Depositar:**
O cliente pode realizar depósitos em sua conta, inserindo o valor desejado.

**Sacar:**
Saques são permitidos até o limite definido, e o número de saques diários é monitorado.

**Extrato:**
Exibe todas as transações do cliente junto com o saldo atual.

**Melhorias Futuras:**
Adicionar uma interface gráfica (GUI) usando uma biblioteca como tkinter.
Permitir múltiplas contas por cliente, com a escolha explícita de contas durante as transações.
Implementar transferências entre contas e gerenciamentos mais complexos de finanças, como contas de poupança.
