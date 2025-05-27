import datetime # Necessário para registrar a data e hora das transações

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
                    "tipo": f"Transferência para{conta_destino.numero_conta}",
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

# Exemplo de uso da Classe (para adicionar os métodos adicionados):
if __name__=="__main__":
    # Criando uma conta bancária de exemplo
    minha_conta = ContaBancaria(numero_conta = "12345-X", saldo_inicial = 1000.0)
    conta_joaob = ContaBancaria(numero_conta = "67890-Y", saldo_inicial = 200.0)

    print(f"Conta: {minha_conta.numero_conta}, criada com saldo: R$ {minha_conta.saldo:.2f}")
    print(f"Conta: {conta_joaob.numero_conta}, criada com saldo: R$ {conta_joaob.saldo:.2f}")

    print("\n--- Testando Extrato (Inicial) ---")
    minha_conta.exibir_extrato() # Exibe as últimas transações realizadas na conta.
    
    print("\n--- Realizando Operações para popular o Extrato ---")
    minha_conta.depositar(300) # Permite ao usuário depositar um valor na conta.
    minha_conta.sacar(150) # Permite ao usuário sacar um valor da conta, verificando se há saldo suficiente.

    print("\n--- Testando Extrato (após operações) ---")
    minha_conta.exibir_extrato()

    print("\n--- Testando Transferência ---")
    minha_conta.transferir(conta_joaob,400) # Realiza uma transferência.
    print("\n--- Saldos após Transferência ---")
    minha_conta.consultar_saldo()
    conta_joaob.consultar_saldo()

    print("\n--- Extrato da minha conta após Transferência ---")
    minha_conta.exibir_extrato()

    print("\n--- Extrato da conta do Joãob após Transferência ---")
    conta_joaob.exibir_extrato()

    minha_conta.transferir(conta_joaob, 1500) # Tentativa de transferência com saldo insuficiente


            
