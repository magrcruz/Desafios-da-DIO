#Funciones
def mimenu():
    menu = """

    MENUZHINO

    [d] Depositar
    [s] Sacar (Retirar)
    [e] Extrato (Extracto)
    [nc] Nova conta
    [lc] Listar contas
    [nu] Novo usuário
    [q] Sair (Salir)

    => """
    return input(menu)

def depositos(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"

    else:
        print("Operação falhou! O valor informado é inválido.")

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor > saldo: #Excedio saldo
        print("Operação falhou! Você não tem saldo suficiente.")

    elif valor > limite: #Excedio limite
        print("Operação falhou! O valor do saque excede o limite.")

    elif numero_saques >= LIMITE_SAQUES: #Excedio numero de retiros
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

    else:
        print("Operação falhou! O valor informado é inválido.")

def mostrar_saldo(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

#Nuevos
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

def print_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(linha)

#Vars, pueden ir en main

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
AGENCIA = "0142"
usuarios = []
contas = []

while True:

    op = mimenu()

    if op == "d":
        valor = float(input("Informe o valor do depósito: "))
        depositos(saldo, valor, extrato)
    elif op == "s": 
        valor = float(input("Informe o valor do saque: "))

        saldo, extrato = sacar(
            saldo=saldo,
            valor=valor,
            extrato=extrato,
            limite=limite,
            numero_saques=numero_saques,
            limite_saques=LIMITE_SAQUES,
        )

    elif op == "e":
            mostrar_saldo(saldo, extrato=extrato)

    elif op == "nu":
        criar_usuario(usuarios)

    elif op == "nc":
        numero_conta = len(contas) + 1
        conta = criar_conta(AGENCIA, numero_conta, usuarios)

        if conta:
            contas.append(conta)

    elif op == "lc":
        print_contas(contas)

    elif op == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")