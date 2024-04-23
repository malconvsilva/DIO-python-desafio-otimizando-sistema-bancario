import re
import textwrap

OPCOES_MENU = [
    dict(opt="d", desc="Depositar"),
    dict(opt="s", desc="Sacar"),
    dict(opt="e", desc="Extrato"),
    dict(opt="a", desc="Nova conta"),
    dict(opt="lc", desc="Listar contas"),
    dict(opt="lu", desc="Listar usuarios"),
    dict(opt="u", desc="Novo usuário"),
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


def valida_data(data: str):

    if not re.match(r'\d{2}-\d{2}-\d{4}', data):
        return False

    return True

# (logradouro, nro - bairro - cidade/sigla estado)
def valida_endereco(endereco: str):

    if not re.match(r'(.*),\s{0,1}(\d+)\s{0,1}-\s{0,1}(.*)\s{0,1}-\s{0,1}(.*)\\(\w{1,3})', endereco):
        return False

    return True

def valida_cpf(cpf: str):
    # Verifica a formatação do CPF
    if not re.match(r'\d{11}', cpf):
        return False

    numeros = [int(digito) for digito in cpf if digito.isdigit()]

    if len(numeros) != 11 or len(set(numeros)) == 1:
        return False

    soma_produtos = sum(a * b for a, b in zip(numeros[0:9], range(10, 1, -1)))
    digito_esperado = (soma_produtos * 10 % 11) % 10
    if numeros[9] != digito_esperado:
        return False

    soma_produtos = sum(a * b for a, b in zip(numeros[0:10], range(11, 1, -1)))
    digito_esperado = (soma_produtos * 10 % 11) % 10
    if numeros[10] != digito_esperado:
        return False

    return True


def menu():
    title = "================ MENU ================"
    menu = title
    for option in OPCOES_MENU:
        menu += "\n"
        menu += option_menu(option['opt'], option['desc'], len(title))
    menu += "\n"
    # menu += '{message:{fill}{align}{width}}'.format(message="",fill='=',align='<',width=len(title))
    # menu += "\n"
    menu += "Qual opção desejada => "
    return input(textwrap.dedent(menu)).lower()


def saque(*, saldo, valor_saque, historico, limite, numero_saques, limite_saques):
    if valor_saque > saldo:
        print("\n!!! Você não tem saldo suficiente. !!!")

    elif valor_saque > limite:
        print("\n!!! O valor do saque excede o limite. !!!")

    elif numero_saques >= limite_saques:
        print("\n!!! Número máximo de saques excedido. !!!")

    elif valor_saque > 0:
        saldo -= valor_saque
        historico += f"Saque:\t\tR$ {valor_saque:.2f}\n"
        numero_saques += 1
        print("\n*** Saque realizado com sucesso! ***")

    else:
        print("\n!!! O valor informado é inválido. !!!")

    return saldo, historico


def deposito(saldo, valor_deposito, historico, /):
    if valor_deposito > 0:
        saldo += valor_deposito
        historico += f"Depósito:\tR$ {valor_deposito:.2f}\n"
        print("\n*** Depósito realizado com sucesso! ***")
    else:
        print("\n!!! O valor informado é inválido. !!!")

    return saldo, historico


def extrato(saldo, /, *, historico):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not historico else historico)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def listar_usuarios(usuarios):
    for usuario in usuarios:
        linha = f"""\
            CPF:\t{usuario['cpf']}
            Nome completo:\t{usuario['nome']}
            Data de nascimento:\t\t{usuario['data_nascimento']}
            Endereço:\t{usuario['endereco']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("CPF do usuário: ")

    if not valida_cpf(cpf):
        print("\n!!! CPF Invalido! !!!")
        return

    usuario = usuario_existe(cpf, usuarios)

    if usuario:
        print("\n*** Conta criada! ***")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n!!! Usuário não encontrado! !!!")


def criar_usuario(usuarios):
    cpf = input("CPF (somente número): ")
    if not valida_cpf(cpf):
        print("\n!!! CPF Invalido! !!!")
        return

    usuario = usuario_existe(cpf, usuarios)

    if usuario:
        print("\n!!! Já existe usuário com esse CPF! !!!")
        return

    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")

    if not valida_data(data_nascimento):
        print("\n!!! Data Invalida! !!!")
        return

    endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("*** Usuário criado! ***")


def usuario_existe(cpf, usuarios):
    res = None
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            res = usuario
            break
    return res


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    historico = ""
    numero_saques = 0
    usuarios = []
    contas = []
    max_n_conta = 0
    while True:
        opcao = menu()

        if opcao == "d":
            valor_deposito = float(input("Valor do depósito: "))

            saldo, historico = deposito(saldo, valor_deposito, historico)

        elif opcao == "s":
            valor_saque = float(input("Valor do saque: "))

            saldo, historico = saque(
                saldo=saldo,
                valor_saque=valor_saque,
                historico=historico,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            extrato(saldo, historico=historico)

        elif opcao == "u":
            criar_usuario(usuarios)

        elif opcao == "a":
            numero_conta = max_n_conta + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
                max_n_conta += 1

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "lu":
            listar_usuarios(usuarios)

        elif opcao == "q":
            break

        else:
            print("Opção inválida!\nPor favor selecione novamente a opção desejada.")


main()
