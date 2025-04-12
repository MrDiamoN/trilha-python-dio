import textwrap
from datetime import datetime

def menu ():
    menu = """
    ================ MENU ================\n
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [se]\tSaque Extra
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair

    => """
    return input(textwrap.dedent(menu))

def deposito(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito efetuado!")

    else:
        print("Falha na operação! O valor informado é inválido.")
    
    return saldo, extrato


def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Falha na operação! Saldo insuficiente.")

    elif excedeu_limite:
        print("Falha na operação! Valor limite de saque excedido.")

    elif excedeu_saques:
        print("Falha na operação! Limite de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque efetuado!")

    else:
        print("Falha na operação! O valor informado é inválido.")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
   # global saldo, extrato # "global" utilizada apenas com o intuito de deixar claro que as variáveis estão fora do escopo da função
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\tR$ {saldo:.2f}")
    print("==========================================")

def saque_extra(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
   # global saldo, extrato, numero_saques # "global" utilizada apenas com o intuito de deixar claro que as variáveis estão fora do escopo da função
   
    if numero_saques < limite_saques:
        taxa = valor * 0.05 # 5% de taxa
        # valor_taxado = valor + valor * 0.05 # 0.05% de taxa
        
        if (valor + taxa) > saldo:
            print("Falha na operação! Saldo insuficiente.")
    
        elif (valor + taxa) > limite:
            print("Falha na operação! Valor limite de saque excedido.")      

        elif saldo >= valor + taxa:
            numero_saques -= 1
            saldo -= taxa
            saque(valor)

            extrato += f"^===> taxa de saque extra: R$ {taxa:.2f}\n"
    
    else:
        print("Falha na operação! O numero de saques ainda está dentro do limite diario.")
    
    return saldo, extrato

def criar_usuario(usuarios):
    cpf = input("Informe o seu CPF (informe somente números): ")
    usuario = filtro_usuario(cpf, usuarios)

    if usuario:
        print("Usuario ja cadastrado!")
        return
    
    nome = input("Informe o seu nome completo: ")
    data_de_nascimento = datetime.strptime(input("Informe a data de nascimento (dd-mm-aaaa): "), "%d-%m-%Y")
    if maior_idade(data_de_nascimento):

        endereco = input("Informe o seu endereço (logradouro, numero - bairro - cidade/estado): ")

        usuarios.append({"nome": nome, "data_de_nascimento": data_de_nascimento, "cpf": cpf, "endereco": endereco})

        print("Usuario cadastrado!")

    else:
        print("Cadastro não realizado! Idade menor que a permitida.")

def maior_idade(data_de_nascimento):
    hoje = datetime.today()

    idade = hoje.year - data_de_nascimento.year

    return idade


def filtro_usuario(cpf, usuarios):
    ususarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return ususarios_filtrados[0] if ususarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF cadastrado (somente números): ")
    usuario = filtro_usuario(cpf, usuarios)

    if usuario:
        print("Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    else:
        print("Usuario não encontrado!")

def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada!")

    else:
        for conta in contas:
            linha = f"""\
                Agência:\t{conta['agencia']}
                C/C:\t\t{conta['numero_conta']}
                Titular:\t{conta['usuario']['nome']}
            """
            print("=" * 100)
            print(textwrap.dedent(linha))



def main():

    AGENCIA = "0011"
    LIMITE_SAQUES = 3
    
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    
    while True:

        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = deposito(saldo, valor, extrato)


        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = saque(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)
        
        elif opcao == "se":
            valor = float(input("Informe o valor do saque extra: "))
            saldo, extrato = saque_extra(saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,)
            
        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()