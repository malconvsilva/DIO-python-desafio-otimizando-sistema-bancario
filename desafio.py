import textwrap

OPTIONS = [
    dict(opt="d", desc="Depositar"),
    dict(opt="s", desc="Sacar"),
    dict(opt="e", desc="Extrato"),
    dict(opt="nc", desc="Nova conta"),
    dict(opt="lc", desc="Listar contas"),
    dict(opt="nu", desc="Novo usuário"),
    dict(opt="q", desc="Sair"),
]
def option_menu(option, message, width=18):
    return '{message:{fill}{align}{width}}[{option}]'.format(
        option=option.lower(),
        message=message.capitalize(),
        fill=' ',
        align='<',
        width=width - len(option) - 2,
    )
def menu():
    title = "================ MENU ================"
    menu = title
    for option in OPTIONS:
        menu += "\n"
        menu += option_menu(option['opt'], option['desc'], len(title))
    menu += "\n"
    # menu += '{message:{fill}{align}{width}}'.format(message="",fill='=',align='<',width=len(title))
    # menu += "\n"
    menu += "Qual opção desejada => "
    return input(textwrap.dedent(menu)).lower()

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n*** Depósito realizado com sucesso! ***")
    else:
        print("\n!!! Operação falhou! O valor informado é inválido. !!!")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n!!! Operação falhou! Você não tem saldo suficiente. !!!")

    elif excedeu_limite:
        print("\n!!! Operação falhou! O valor do saque excede o limite. !!!")

    elif excedeu_saques:
        print("\n!!! Operação falhou! Número máximo de saques excedido. !!!")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n*** Saque realizado com sucesso! ***")

    else:
        print("\n!!! Operação falhou! O valor informado é inválido. !!!")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    cpf = input("CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n!!! Já existe usuário com esse CPF! !!!")
        return

    nome = input("Nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("*** Usuário criado! ***")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n*** Conta criada! ***")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n!!! Usuário não encontrado! !!!")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    max_n_conta = 0
    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = max_n_conta + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
                max_n_conta += 1

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
