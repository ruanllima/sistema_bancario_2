# Importação da biblioteca para ajuste de formatação
import textwrap

# Função para exibir o menu de opções
def exibir_menu():
    menu = """\n
    MENU
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))  # Remove espaços em branco desnecessários

# Função para realizar um depósito
def fazer_deposito(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"  # Adiciona a formatação correta
        print("\nDepósito realizado com sucesso!")
    else:
        print("\nOperação falhou! Valor inválido.")

    return saldo, extrato

# Função para realizar um saque
def fazer_saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\nOperação falhou! Saldo insuficiente.")

    elif excedeu_limite:
        print("\nOperação falhou! Valor de saque excede o limite.")

    elif excedeu_saques:
        print("\nOperação falhou! Limite máximo de saques atingido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"  # Adiciona a formatação correta
        numero_saques += 1
        print("\nSaque realizado com sucesso!")

    else:
        print("\nOperação falhou! Valor inválido.")

    return saldo, extrato

# Função para exibir o extrato da conta
def mostrar_extrato(saldo, /, *, extrato):
    print("\nEXTRATO")
    print("Nenhuma movimentação registrada." if not extrato else extrato)  # Simplificação da mensagem
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================")

# Função para criar um novo usuário
def criar_novo_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nUsuário já cadastrado com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nmr - bairro - cidade/estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("Usuário criado com sucesso!")

# Função para filtrar usuário por CPF
def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

# Função para criar uma nova conta
def criar_nova_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nConta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\nUsuário não encontrado, processo de criação de conta encerrado!")

# Função para listar as contas
def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência: {conta['agencia']}
            C/C:     {conta['numero_conta']}
            Titular: {conta['usuario']['nome']}
        """
        print("=" * 70)
        print(textwrap.dedent(linha))  # Remove espaços em branco desnecessários

# Função principal
def principal():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = exibir_menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = fazer_deposito(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato = fazer_saque(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            mostrar_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_novo_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_nova_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, selecione novamente a operação desejada.")

principal()