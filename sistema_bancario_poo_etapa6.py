import datetime
import json
import os

"""
Foram modificados as funções "salvar contas" e "carregar contas", 
além de ser incluido um nova função para criar ou escolher uma conta.
Também foi incluido um novo item no menu principal: trocar de conta.
Para cada conta é criado respectivamente um arquivo JSON.
"""

class  ContaBancaria():
    """ Representa uma conta bancária com saldo e histórico de transações."""
    def __init__(self,numero_conta, saldo_inicial = 0, extrato_inicial = None):
        self.saldo = saldo_inicial
        self.numero_conta = numero_conta
        self.extrato = extrato_inicial if extrato_inicial is not None else []

    def consultar_saldo(self):
        """ Exibe o saldo atual da conta."""
        print(f"Seu saldo atual é: R$ {self.saldo:.2f}")

    def depositar(self,valor):
        """Realiza uma operação de depósito na conta."""
        try:
            valor_deposito = float(valor)
            if valor_deposito <= 0:
                print("Valor de depósito inválido. Digite um número positivo.")
                return
            self.saldo += valor_deposito # atualiza o saldo somando o valor do depósito.
            # Registra a transação no extrato.
            agora = datetime.datetime.now()
            self.extrato.append({
                "data_hora": agora.strftime("%d/%m/%Y - %H:%M:%S"),
                "tipo": "Depósito",
                "valor": valor_deposito
            })
            print(f"Depósito de R$ {valor_deposito:.2f} realizado com sucesso.")
            print(f"Seu novo saldo é {self.saldo:.2f}")
        except ValueError:
            print("Valor inválido para depósito. Por favor digite um número.")

    def sacar(self,valor):
        """Realiza uma operação de saque na conta, verificando o saldo."""
        try:
            valor_saque = float(valor)
            if valor_saque <= 0:
                print("Valor de saque inválido. Digite um número positivo.")
                return
            if valor_saque <= self.saldo: # verifica se o saldo é sufuciente.
                self.saldo -= valor_saque # atualiza o saldo.
                # Registra a transação no extrato.
                agora = datetime.datetime.now()
                self.extrato.append({
                    "data_hora": agora.strftime("%d/%m/%Y - %H:%M:%S"),
                    "tipo": "Saque",
                    "valor": valor_saque
                })
                print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso.")
                print(f"Seu novo saldo é {self.saldo:.2f}")
            else:
                print("Saldo insuficiente")
        except ValueError:
            print("Valor inválido para saque. Por favor digite um número.")

    def exibir_extrato(self):
        """Exibe o histórico detalhado das transações da conta."""
        if not self.extrato: # Verifica se o extrato está vazio.
            print("Não foram realizadas transações.")
        else:
            print("\n--- Extrato Bancário ---")
            for transacao in self.extrato: # Iterar sobre a lista extrato e exiba cada transação formatada.
                data_hora = transacao["data_hora"]
                tipo = transacao["tipo"]
                valor = transacao["valor"]
                print(f"{data_hora} - {tipo}: R$ {valor:.2f}")
            print(f"Saldo atual: R$ {self.saldo:.2f}") # Exibir o saldo atual da conta.

    def transferir(self, conta_destino, valor):
        """realiza uma tranferência de valor para outra conta bancária."""
        try:
            valor_transferencia = float(valor) # O sistema deverá pedir o número da conta de destino e depois o valor a ser transferido.
            if valor_transferencia <= 0 :
                print("Valor de transferência inválido. Digite um número positivo.")
                
                
            if not isinstance(conta_destino, ContaBancaria): # Verifica se existe a conta de destino.
                print("Erro: a conta de destino não é válida de Contabancaria. ")
                return
            
            if valor_transferencia <= self.saldo: # Verificar se há saldo suficiente na conta de origem.
                self.saldo -= valor_transferencia # O valor deve ser subtraído do saldo.
                # Registrar a transação na conta de origem.
                agora = datetime.datetime.now()
                self.extrato.append({
                    "data_hora": agora.strftime("%d/%m/%Y - %H:%M:%S"),
                    "tipo": f"Transferência para {conta_destino.numero_conta}",
                    "valor": valor_transferencia
                })
                print(f"Transferência de R$ {valor_transferencia:.2f} para a conta {conta_destino.numero_conta} realizada com sucesso.")
                print(f"Seu novo saldo é: R$ {self.saldo:.2f}")

                # Chamar o método depositar da conta destino.
                conta_destino.depositar(valor_transferencia) # Chamar o método depositar() da conta_destino para adicionar o valor.
            else:
                print("Saldo insuficiente para realizar a transferência.")

        except ValueError:
            print("Valor inválido para a transferência. Por favor, digite um número.")

# Novo: salvar e carregar múltiplas contas, criando um arquivo para cada conta7

def salvar_todas_contas(contas):
    for numero, conta in contas.items():
        filename = f"conta_{numero}.json"
        dados = {
            "numero_conta": conta.numero_conta,
            "saldo": conta.saldo,
            "extrato": conta.extrato
        }
        with open(filename, "w") as f:
            json.dump(dados, f, indent=4)
    print("Todas as contas foram salvas com sucesso!")

def carregar_todas_contas():
    contas = {}
    for arquivo in os.listdir():
        if arquivo.startswith("conta_") and arquivo.endswith(".json"):
            with open(arquivo, "r") as f:
                dados = json.load(f)
                conta = ContaBancaria(dados["numero_conta"], dados["saldo"], dados["extrato"])
                contas[dados["numero_conta"]] = conta
    return contas

# Novo: menu para gerenciar contas
def escolher_conta(contas):
    while True:
        print("\nContas disponíveis:")
        for num in contas:
            print(f"- {num}")
        print("1 - Selecionar conta existente")
        print("2 - Criar nova conta")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            numero = input("Digite o número da conta: ")
            if numero in contas:
                return contas[numero]
            else:
                print("Conta não encontrada.")
        elif opcao == "2":
            novo_numero = input("Digite o número da nova conta: ")
            if novo_numero in contas:
                print("Essa conta já existe.")
            else:
                conta = ContaBancaria(novo_numero)
                contas[novo_numero] = conta
                print(f"Conta {novo_numero} criada com sucesso!")
                return conta
        else:
            print("Opção inválida.")

# Bloco principal atualizado
if __name__ == "__main__":
    contas = carregar_todas_contas()
    print("\nBem-vindo ao sistema bancário com múltiplas contas!")

    conta_atual = escolher_conta(contas)

    while True:
        print(f"\n--- Menu da Conta {conta_atual.numero_conta} ---")
        print("1 - Consultar Saldo")
        print("2 - Depositar")
        print("3 - Sacar")
        print("4 - Exibir Extrato")
        print("5 - Transferir para outra conta")
        print("6 - Trocar de conta")
        print("7 - Sair")

        opcao = input("Digite a opção desejada: ")

        if opcao == "1":
            conta_atual.consultar_saldo()
        elif opcao == "2":
            valor = input("Digite o valor a depositar: R$ ")
            conta_atual.depositar(valor)
        elif opcao == "3":
            valor = input("Digite o valor a sacar: R$ ")
            conta_atual.sacar(valor)
        elif opcao == "4":
            conta_atual.exibir_extrato()
        elif opcao == "5":
            destino_numero = input("Digite o número da conta de destino: ")
            if destino_numero in contas:
                valor = input("Digite o valor a transferir: R$ ")
                conta_atual.transferir(contas[destino_numero], valor)
            else:
                print("Conta de destino não encontrada.")
        elif opcao == "6":
            conta_atual = escolher_conta(contas)
        elif opcao == "7":
            salvar_todas_contas(contas)
            print("Obrigado por utilizar o Banco virtual!")
            break
        else:
            print("Opção inválida. Tente novamente.")