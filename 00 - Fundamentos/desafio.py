menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[p] Saque Extra
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

def depoisito(valor):
    global saldo, extrato # "global" utilizada apenas com o intuito de deixar claro que as variáveis estão fora do escopo da função
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Falha na operação! O valor informado é inválido.")

def saque(valor):
    global saldo, extrato, numero_saques # "global" utilizada apenas com o intuito de deixar claro que as variáveis estão fora do escopo da função
    if valor > saldo:
        print("Falha na operação! Saldo insuficiente.")
    elif valor > limite:
        print("Falha na operação! Valor limite de saque excedido.")
    elif numero_saques >= LIMITE_SAQUES:
        print("Falha na operação! Limite de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
    else:
        print("Falha na operação! O valor informado é inválido.")

def exibir_extrato():
    global saldo, extrato # "global" utilizada apenas com o intuito de deixar claro que as variáveis estão fora do escopo da função
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimendtações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def saque_extra(valor):
    global saldo, extrato, numero_saques # "global" utilizada apenas com o intuito de deixar claro que as variáveis estão fora do escopo da função
    valor_taxado = valor + valor * 0.05 # 0.05% de taxa
    if saldo >= valor_taxado:
        numero_saques -= 1
        saque(valor)
        extrato += f"^===> taxa de saque extra: R$ {valor * 0.05:.2f}\n"


while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        depoisito(valor)


    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        saque(valor)

    elif opcao == "e":
        exibir_extrato()
    
    elif opcao == "p":
        valor = float(input("Informe o valor do saque extra: "))
        saque_extra(valor)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
