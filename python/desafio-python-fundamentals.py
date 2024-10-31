menu = """

MENUZHINO

[d] Depositar
[s] Sacar (Retirar)
[e] Extrato (Extracto)
[q] Sair (Salir)

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    op = input(menu)

    if op == "d":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif op == "s":
        valor = float(input("Informe o valor do saque: "))

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

    elif op == "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    elif op == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")