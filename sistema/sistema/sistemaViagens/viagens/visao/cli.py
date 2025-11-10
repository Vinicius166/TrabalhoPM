from ...viagens.persistencia.banco import BancoDeDados, Persistente
from ...viagens.modelo.models import Cliente, Destino, Reserva, ItemReserva

class CLI:
    def __init__(self, banco: BancoDeDados):
        self.banco = banco

    def _obter_inteiro(self, prompt: str) -> int:
        while True:
            try:
                return int(input(prompt).strip())
            except ValueError:
                print("Entrada inválida. Por favor, digite um número inteiro.")

    def _obter_string(self, prompt: str) -> str:
        while True:
            texto = input(prompt).strip()
            if texto:
                return texto
            print("Entrada inválida. Não pode ser vazio.")

    def _obter_float(self, prompt: str) -> float:
        while True:
            try:
                valor = input(prompt).strip().replace(',', '.')
                return float(valor)
            except ValueError:
                print("Entrada inválida. Por favor, digite um valor numérico (ex: 100.00).")

    def menu_principal(self):
        while True:
       
            print("\n=== Sistema de Viagens ===")
            print("1 - Clientes")
            print("2 - Fazer Nova Reserva")
            print("3 - Gerenciar Reservas Existentes")
            print("4 - Mostrar tudo")
            print("0 - Sair")
            
            escolha = input("Escolha: ").strip()
            
            if escolha == '1':
                self.menu_entidade('clientes')
            elif escolha == '2':
                self._inserir_reserva_simplificada()
            elif escolha == '3':
                self.menu_entidade('reservas')
            elif escolha == '4':
                print(self.banco)
            elif escolha == '0':
                print("Saindo...")
                break
            else:
                print("Opção inválida.")

    def menu_entidade(self, nome: str):
        if nome == 'destinos':
            print("Os destinos são pré-determinados e não podem ser alterados.")
            return

        repo = getattr(self.banco, nome)
        while True:
            print(f"\n=== Menu {nome} ===")
            print("1 - Inserir")
            print("2 - Alterar")
            print("3 - Apagar")
            print("4 - Visualizar por id")
            print("5 - Visualizar todos")
            print("0 - Voltar")
            
            escolha = input("Escolha: ").strip()

            if escolha == '1':
                self._inserir(nome, repo)
            elif escolha == '2':
                self._alterar(nome, repo)
            elif escolha == '3':
                self._apagar(nome, repo)
            elif escolha == '4':
                self._visualizar_id(nome, repo)
            elif escolha == '5':
                self._visualizar_todos(nome, repo)
            elif escolha == '0':
                break
            else:
                print("Opção inválida.")
    
    def _inserir_reserva_simplificada(self):
        print("\n--- FAZER NOVA RESERVA ---")
        try:
            cliente_id = self._obter_inteiro("Insira seu ID de Cliente para continuar: ")
            cliente = self.banco.clientes.buscar_por_id(cliente_id)
            
            if not cliente:
                print("Cliente não encontrado. Por favor, cadastre-se primeiro no menu 'Clientes'.")
                return

            print("\n--- DESTINOS DISPONÍVEIS ---")
            for destino in self.banco.destinos.listar_todos():
                print(f"ID {destino.id}: {destino.cidade} ({destino.hotel}) - R$ {destino.valor_diaria:.2f}/diária")
            
            destino_id = self._obter_inteiro("Escolha o ID do destino desejado: ")
            destino = self.banco.destinos.buscar_por_id(destino_id)
            
            if not destino:
                print("Destino inválido. Retornando ao menu principal.")
                return

            dias = self._obter_inteiro("Quantos dias de viagem? ")
            if dias <= 0:
                 print("A duração deve ser de pelo menos 1 dia.")
                 return

            print("\n--- MÉTODOS DE PAGAMENTO ---")
            print("1 - Débito/PIX (2% de Desconto)")
            print("2 - Cartão de Crédito em 1x (Preço Normal)")
            print("3 - Parcelamento (3% de Acréscimo)")
            metodo = self._obter_inteiro("Escolha o método de pagamento (1, 2 ou 3): ")
            
            if metodo not in [1, 2, 3]:
                print("Método de pagamento inválido. Usando opção Normal (2).")
                metodo = 2
                
            novo_id = len(self.banco.reservas.listar_todos()) + 1 
            
            nova_reserva = Reserva(novo_id, cliente, metodo)
            
            item_reserva = ItemReserva(destino, dias)
            nova_reserva.adicionar_item(item_reserva)
            
            self.banco.reservas.inserir(nova_reserva)

            print("\n==================================")
            print("SUA RESERVA FOI REALIZADA COM SUCESSO!")
            print(f"Cliente: {cliente.nome}")
            print(f"Destino: {destino.cidade} por {dias} dias.")
            print(f"Custo Bruto: R$ {nova_reserva.custo_bruto():.2f}")
            print(f"Custo Total (com ajuste): R$ {nova_reserva.custo_total():.2f}")
            print("==================================")
            
        except ValueError as e:
            print(f"Erro de entrada: {e}. Retornando ao menu.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            
    def _inserir(self, nome: str, repo: Persistente):
        try:
            id = self._obter_inteiro("id: ")
            
            if nome == 'clientes':
                nome_c = self._obter_string("nome: ")
                email_c = self._obter_string("email: ")
                obj = Cliente(id, nome_c, email_c)
            
            elif nome == 'reservas':
                cliente_id = self._obter_inteiro("ID do cliente: ")
                cliente = self.banco.clientes.buscar_por_id(cliente_id)
                if cliente is None:
                    print("Cliente não encontrado.")
                    return

                metodo = self._obter_inteiro("Metodo de pagamento (1=desc, 2=normal, 3=acresc): ")
                obj = Reserva(id, cliente, metodo)
                
                while True:
                    print("\n--- Adicionar Itens (Destinos) ---")
                    print("Destinos disponíveis:")
                    for d in self.banco.destinos.listar_todos():
                        print(f"  ID {d.id}: {d.cidade} - R$ {d.valor_diaria:.2f}/dia")

                    destino_id = self._obter_inteiro("ID do Destino para adicionar (0 para sair): ")
                    if destino_id == 0:
                        break
                    
                    destino = self.banco.destinos.buscar_por_id(destino_id)
                    if destino is None:
                        print("Destino inválido.")
                        continue

                    dias = self._obter_inteiro("Dias de viagem: ")
                    if dias <= 0:
                        print("Dias deve ser maior que zero.")
                        continue

                    item = ItemReserva(destino, dias)
                    obj.adicionar_item(item)
                    print(f"Item '{destino.cidade}' adicionado. Custo atual: R$ {obj.custo_total():.2f}")

            else:
                print("Entidade não suportada.")
                return

            repo.inserir(obj)
            print("Inserido.")
            
        except Exception as e:
            print("Erro ao inserir:", e)

    def _alterar(self, nome: str, repo: Persistente):
        try:
            id = self._obter_inteiro("id: ")
            obj = repo.buscar_por_id(id)

            if obj is None:
                print("Não encontrado.")
                return

            if nome == 'clientes':
                obj.nome = self._obter_string(f"Novo nome ({obj.nome}): ")
                obj.email = self._obter_string(f"Novo email ({obj.email}): ")
                repo.alterar(obj)
                print("Alterado.")
            
            elif nome == 'reservas':
                while True:
                    print("\n--- Alterar Reserva ---")
                    print(f"Itens atuais ({len(obj.itens)}):")
                    for i, it in enumerate(obj.itens):
                        print(f"  [{i+1}] {it}")
                    
                    print(f"\nMetodo de pagamento atual: {obj.metodo_pagamento}")
                    print("1 - Adicionar Item (Destino)")
                    print("2 - Remover Item (pelo número)")
                    print("3 - Alterar Metodo de Pagamento")
                    print("0 - Voltar")
                    opt = input("Opção: ").strip()
                    
                    if opt == '1':
                        print("Destinos disponíveis:")
                        for d in self.banco.destinos.listar_todos():
                            print(f"  ID {d.id}: {d.cidade} - R$ {d.valor_diaria:.2f}/dia")

                        destino_id = self._obter_inteiro("ID do Destino para adicionar: ")
                        destino = self.banco.destinos.buscar_por_id(destino_id)
                        if destino is None:
                            print("Destino inválido.")
                            continue

                        dias = self._obter_inteiro("Dias de viagem: ")
                        item = ItemReserva(destino, dias)
                        obj.adicionar_item(item)
                        print("Item adicionado.")
                        repo.alterar(obj)
                    
                    elif opt == '2':
                        try:
                            index = self._obter_inteiro("Número do item para remover (ex: 1): ")
                            obj.remover_item(index - 1) 
                            print("Item removido.")
                            repo.alterar(obj)
                        except IndexError:
                            print("Índice de item inválido.")
                        except Exception as e:
                            print("Erro ao remover:", e)

                    elif opt == '3':
                        metodo = self._obter_inteiro("Novo metodo (1=desc, 2=normal, 3=acresc): ")
                        obj.metodo_pagamento = metodo
                        repo.alterar(obj)
                        print("Metodo alterado.")
                    
                    elif opt == '0':
                        break
                    
                    else:
                        print("Opção inválida.")
            
            else:
                print("Entidade não suportada.")

        except Exception as e:
            print("Erro ao alterar:", e)

    def _apagar(self, nome: str, repo: Persistente):
        try:
            id = self._obter_inteiro("id: ")
            repo.excluir(id)
            print("Removido.")
        except Exception as e:
            print("Erro ao apagar:", e)

    def _visualizar_id(self, nome: str, repo: Persistente):
        try:
            id = self._obter_inteiro("id: ")
            obj = repo.buscar_por_id(id)
            if obj is None:
                print("Não encontrado.")
            else:
                print(obj)
                if nome == 'reservas':
                    for it in obj.itens:
                        print("  -", it)
        except Exception as e:
            print("Erro ao visualizar:", e)

    def _visualizar_todos(self, nome: str, repo: Persistente):
        all_objs = repo.listar_todos()
        if not all_objs:
            print("Nenhum registro.")
            return
        for o in all_objs:
            print(o)
            if nome == 'reservas':
                for it in o.itens:
                    print("  -", it)