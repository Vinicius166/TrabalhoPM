from ...viagens.persistencia.banco import BancoDeDados, Persistente
from ...viagens.modelo.models import Cliente, Destino, Reserva, ItemReserva
from tkinter import *
from tkinter.ttk import Treeview, Combobox

class GUI:
    def __init__(self, banco):
        self.banco = banco
        
        self.janela = Tk()
        self.janela.title("Sistema de Viagens")
        self.janela.geometry("300x250")

        self._menu_principal()

        self.janela.mainloop()

    def limpar_tela(self):

        for widget in self.janela.winfo_children():
            widget.destroy()

    def mostrar_tudo (self):

        tela = Toplevel(self.janela)
        tela.title("Todos os Dados")

        txt = Text(tela, width=120, height=40)
        txt.pack(padx=10, pady=10)

        txt.insert("1.0", str(self.banco))
        txt.config(state="disabled")

    def _menu_principal(self):

        self.janela.geometry("300x250")
        self.limpar_tela()
        
        Label(self.janela, text="Bem vindo!!").pack()
        Button(self.janela, text="Clientes", width=25, command=self._gui_clientes).pack(pady=5)
        Button(self.janela, text="Destinos", width=25, command=self._gui_destinos).pack(pady=5)
        Button(self.janela, text="Reservas", width=25, command=self._gui_reservas).pack(pady=5)
        Button(self.janela, text="Mostrar Tudo",width=25, command=self.mostrar_tudo).pack(pady=5)
        Button(self.janela, text="Sair", width=25, command=self.janela.quit).pack(pady=5)

    def _gui_clientes (self):
        self.janela.geometry("600x600")
        self.limpar_tela()
        repo = self.banco.clientes

        frame = Frame(self.janela)
        frame.pack(fill="both", expand=True)

        Label(frame, text="Menu Clientes", font=("Arial", 18)).pack(pady=15)
        Button(frame, text="Inserir Cliente", width=25, command=lambda: self.inserir_cliente("clientes", repo)).pack(pady=5)
        Button(frame, text="Alterar Cliente", width=25, command=lambda: self.alterar_cliente("clientes", repo)).pack(pady=5)
        Button(frame, text="Apagar Cliente", width=25, command=lambda: self.apagar_cliente("clientes", repo)).pack(pady=5)
        #Button(frame, text="Visualizar por ID", width=25, command=lambda: self.cliente_id("clientes", repo)).pack(pady=5)
        Button(frame, text="Voltar", width=25, command=self._menu_principal).pack(pady=20)

        Label(frame, text="Clientes cadastrados:", font=("Arial", 14)).pack(pady=10)
        colunas = ("ID", "Nome", "Email")
        tabela = Treeview(frame, columns=colunas, show="headings", height=15)

        tabela.heading('ID',text='ID')
        tabela.heading('Nome',text='Nome')
        tabela.heading('Email',text='Email')
        tabela.column('ID', width=60)
        tabela.column('Nome', width=100)
        tabela.column('Email', width=200)

        tabela.pack(fill="both", expand=True, padx=10, pady=10)
        
        for cliente in repo.listar_todos():
            tabela.insert("", "end", values=(cliente.id, cliente.nome, cliente.email))

    def inserir_cliente(self, tipo, repo):

        janela = Toplevel()
        janela.title("Inserir Cliente")
        janela.geometry("300x200")

        Label(janela, text="ID:").pack()
        entry_id = Entry(janela)
        entry_id.pack()

        Label(janela, text="Nome:").pack()
        entry_nome = Entry(janela)
        entry_nome.pack()

        Label(janela, text="Email:").pack()
        entry_email = Entry(janela)
        entry_email.pack()

        def salvar():
                id_cliente = int(entry_id.get())
                nome = entry_nome.get()
                email = entry_email.get()

                novo = Cliente(id_cliente, nome, email)
                repo.inserir(novo)
                self._gui_clientes()
                janela.destroy()

        Button(janela, text="Salvar", command=salvar).pack(pady=10)
    
    def alterar_cliente(self, nome, repo):

        janela_id = Toplevel(self.janela)
        janela_id.title("Alterar Cliente")

        nomes_clientes = [cliente.nome for cliente in repo.listar_todos()]
        combo = Combobox(janela_id, values=nomes_clientes, state="readonly")
        combo.pack(pady=5)

        def buscar_cliente():
            nome_escolhido = combo.get()
            if not nome_escolhido:
                return
            
            cliente = None
            for c in repo.listar_todos():
                if c.nome == nome_escolhido:
                    cliente = c
                    break

            janela_edicao = Toplevel(self.janela)
            janela_edicao.title(f"Editar Cliente {cliente.id}")

            Label(janela_edicao, text="Nome:").pack()
            entry_nome = Entry(janela_edicao)
            entry_nome.insert(0, cliente.nome)
            entry_nome.pack(pady=5)

            Label(janela_edicao, text="Email:").pack()
            entry_email = Entry(janela_edicao)
            entry_email.insert(0, cliente.email)
            entry_email.pack(pady=5)

            def salvar():
                novo_nome = entry_nome.get()
                novo_email = entry_email.get()

                cliente.nome = novo_nome
                cliente.email = novo_email
                self._gui_clientes()
                janela_edicao.destroy()
                janela_id.destroy()

            Button(janela_edicao, text="Salvar", command=salvar).pack(pady=10)

        Button(janela_id, text="Buscar", command=buscar_cliente).pack(pady=10)

    def apagar_cliente(self, tipo, repo):

        janela_id = Toplevel(self.janela)
        janela_id.title("Deletar Cliente")

        Label(janela_id, text="Selecione o cliente:").pack(pady=5)
        mapa = {cliente.nome: cliente.id for cliente in repo.listar_todos()}
        nomes_clientes = [cliente.nome for cliente in repo.listar_todos()]
        combo = Combobox(janela_id, values=nomes_clientes, state="readonly")
        combo.pack(pady=5)

        def salvar():
            nome_escolhido = combo.get()
            id_cliente = mapa[nome_escolhido]
            repo.excluir(id_cliente)
            self._gui_clientes()
            janela_id.destroy()
            
        Button(janela_id, text="Salvar", command=salvar).pack(pady=10)
    '''
    def cliente_id(self, tipo, repo):

        janela_id = Toplevel(self.janela)
        janela_id.title("Consulta de cliente")

        Label(janela_id, text="Digite o ID do cliente:").pack(pady=5)
        entry_id = Entry(janela_id)
        entry_id.pack(pady=5)

        def buscar():

            id_cliente = int(entry_id.get())
            cliente = repo.buscar_por_id(id_cliente)

            janela_res = Toplevel(self.janela)
            janela_res.title(f"Cliente {id_cliente}")

            Label(janela_res, text=str(cliente)).pack(padx=10, pady=10)
            janela_id.destroy()

        Button(janela_id, text="Buscar", command=buscar).pack(pady=10)
    '''
    def _gui_destinos (self):

        self.limpar_tela()
        self.janela.geometry('600x600')
        repo = self.banco.destinos

        frame = Frame(self.janela)
        frame.pack(fill="both", expand=True)

        Label(frame, text="Menu Destinos", font=("Arial", 18)).pack(pady=15)
        Button(frame, text="Inserir Destino", width=25, command=lambda: self.inserir_destino("destinos", repo)).pack(pady=5)
        Button(frame, text="Alterar Destino", width=25, command=lambda: self.alterar_destino("destinos", repo)).pack(pady=5)
        Button(frame, text="Apagar Destino", width=25, command=lambda: self.apagar_destino("destinos", repo)).pack(pady=5)
        #Button(frame, text="Visualizar por ID", width=25, command=lambda: self.destino_id("destinos", repo)).pack(pady=5)
        Button(frame, text="Voltar", width=25, command=self._menu_principal).pack(pady=20)
        
        Label(frame, text="Destinos cadastrados:", font=("Arial", 14)).pack(pady=10)
        colunas = ("ID", "Cidade", "Hotel", "Diária")
        tabela = Treeview(frame, columns=colunas, show="headings", height=15)

        tabela.heading('ID',text='ID')
        tabela.heading('Cidade',text='Cidade')
        tabela.heading('Hotel',text='Hotel')
        tabela.heading('Diária',text='Diária(R$)')
        tabela.column('ID', width=60)
        tabela.column('Cidade', width=100)
        tabela.column('Hotel', width=200)
        tabela.column('Diária', width=60)

        tabela.pack(fill="both", expand=True, padx=10, pady=10)
        
        for destino in repo.listar_todos():
            tabela.insert("", "end", values=(destino.id, destino.cidade, destino.hotel, destino.valor_diaria))


    def inserir_destino(self, tipo, repo):

        janela = Toplevel()
        janela.title("Inserir Destino")
        janela.geometry("300x200")

        Label(janela, text="ID:").pack()
        entry_id = Entry(janela)
        entry_id.pack()

        Label(janela, text="Cidade:").pack()
        entry_cidade = Entry(janela)
        entry_cidade.pack()

        Label(janela, text="Hotel:").pack()
        entry_Hotel = Entry(janela)
        entry_Hotel.pack()

        Label(janela, text="Valor da diaria:").pack()
        entry_Valor = Entry(janela)
        entry_Valor.pack()

        def salvar():
                id_destino = int(entry_id.get())
                cidade = entry_cidade.get()
                hotel = entry_Hotel.get()
                valor = float(entry_Valor.get())

                novo = Destino(id_destino, cidade, hotel, valor)
                repo.inserir(novo)
                self._gui_destinos()

                janela.destroy()

        Button(janela, text="Salvar", command=salvar).pack(pady=10)

    def alterar_destino(self, nome, repo):

        janela_id = Toplevel(self.janela)
        janela_id.title("Alterar Destino")

        nomes_cidades = [destino.cidade for destino in repo.listar_todos()]
        combo = Combobox(janela_id, values=nomes_cidades, state="readonly")
        combo.pack(pady=5)

        def buscar_cidade():
            nome_escolhido = combo.get()
            if not nome_escolhido:
                return
            
            destino = None
            for c in repo.listar_todos():
                if c.cidade == nome_escolhido:
                    destino = c
                    break

            janela_edicao = Toplevel(self.janela)
            janela_edicao.title(f"Editar Destino {destino.id}")

            Label(janela_edicao, text="Cidade:").pack()
            entry_cidade = Entry(janela_edicao)
            entry_cidade.insert(0, destino.cidade)
            entry_cidade.pack(pady=5)

            Label(janela_edicao, text="Hotel:").pack()
            entry_hotel = Entry(janela_edicao)
            entry_hotel.insert(0, destino.hotel)
            entry_hotel.pack(pady=5)

            Label(janela_edicao, text="Valor da Diária:").pack()
            entry_valor = Entry(janela_edicao)
            entry_valor.insert(0, destino.valor_diaria)
            entry_valor.pack(pady=5)

            def salvar():
                novo_cidade = entry_cidade.get()
                novo_hotel = entry_hotel.get()
                novo_valor = float(entry_valor.get())

                destino.cidade = novo_cidade
                destino.hotel = novo_hotel
                destino.valor_diaria = novo_valor
                self._gui_destinos()
                janela_edicao.destroy()
                janela_id.destroy()

            Button(janela_edicao, text="Salvar", command=salvar).pack(pady=10)

        Button(janela_id, text="Buscar", command=buscar_cidade).pack(pady=10)

    def apagar_destino(self, tipo, repo):

        janela_id = Toplevel(self.janela)
        janela_id.title("Deletar Destino")

        Label(janela_id, text="Selecione o destino:").pack(pady=5)
        mapa = {destino.cidade: destino.id for destino in repo.listar_todos()}
        nomes_cidades = [destino.cidade for destino in repo.listar_todos()]
        combo = Combobox(janela_id, values=nomes_cidades, state="readonly")
        combo.pack(pady=5)

        def salvar():
            destino_escolhido = combo.get()
            id_destino = mapa[destino_escolhido]
            repo.excluir(id_destino)
            self._gui_destinos()
            janela_id.destroy()
            
        Button(janela_id, text="Salvar", command=salvar).pack(pady=10)
    '''   
    def destino_id(self, tipo, repo):

        janela_id = Toplevel(self.janela)
        janela_id.title("Consulta de destino")

        Label(janela_id, text="Digite o ID do destino:").pack(pady=5)
        entry_id = Entry(janela_id)
        entry_id.pack(pady=5)

        def buscar():

            id_destino = int(entry_id.get())
            destino = repo.buscar_por_id(id_destino)

            janela_res = Toplevel(self.janela)
            janela_res.title(f"Cliente {id_destino}")

            Label(janela_res, text=str(destino)).pack(padx=10, pady=10)
            janela_id.destroy()

        Button(janela_id, text="Buscar", command=buscar).pack(pady=10)
    '''
    def _gui_reservas (self):
        self.janela.geometry("800x600")
        self.limpar_tela()
        repo = self.banco.reservas

        frame = Frame(self.janela)
        frame.pack(expand=True)

        Label(frame, text="Menu Reservas", font=("Arial", 18)).pack(pady=15)
        Button(frame, text="Fazer Reservas", width=25, command=self.inserir_reserva).pack(pady=5)
        Button(frame, text="Alterar Reserva", width=25, command=self.alterar_reserva).pack(pady=5)
        Button(frame, text="Apagar Reserva", width=25, command=self.apagar_reserva).pack(pady=5)
        Button(frame, text="Voltar", width=25, command=self._menu_principal).pack(pady=20)

        Label(frame, text="Destinos cadastrados:", font=("Arial", 14)).pack(pady=10)
        colunas = ("ID", "Cliente")
        tabela = Treeview(frame, columns=colunas, show="headings", height=15)

        tabela.heading('ID',text='ID')
        tabela.heading('Cliente',text='Cliente')
        tabela.column('ID', width=60)
        tabela.column('Cliente', width=100)
        tabela.pack(pady=10)

        for reserva in repo.listar_todos():
            tabela.insert("", "end", values=(reserva.id, reserva.cliente.nome))

        self.info_label = Label(frame, text="", font=("Arial", 12))
        self.info_label.pack(pady=10)
        
        def ao_clicar(event):
            item = tabela.focus()
            if not item:
                return

            valores = tabela.item(item, "values")
            id_reserva = int(valores[0])

            reserva = repo.buscar_por_id(id_reserva)

            janela_info = Toplevel(self.janela)
            janela_info.title(f"Reserva {id_reserva}")
            janela_info.geometry("400x300")

            texto = f"Cliente: {reserva.cliente.nome}\n\nDestinos:\n"

            for item_reserva in reserva.itens:
                texto += (
                    f" - {item_reserva.destino.cidade}"
                    f" | {item_reserva.dias} dias"
                    f" | Custo: R$ {item_reserva.custo():.2f}\n"
                )

            texto += f"\nCusto total: R$ {reserva.custo_total():.2f}"
            Label(janela_info, text=texto, justify="left", font=("Arial", 12)).pack(padx=10, pady=10)

        tabela.bind("<ButtonRelease-1>", ao_clicar) 

    def inserir_reserva(self):
        
        janela = Toplevel(self.janela)
        janela.title("Nova Reserva")
        repo = self.banco.clientes

        Label(janela, text="Selecionar Cliente:").pack(pady=5)
        combo = Combobox(janela, state="readonly")
        combo.pack(pady=5)

        
        def atualizar_combo():
            combo["values"] = [c.nome for c in repo.listar_todos()]
        atualizar_combo()

        def continuar():
            nome_escolhido = combo.get()
            if not nome_escolhido:
                return
            
            mapa = {cliente.nome: cliente for cliente in repo.listar_todos()}

            cliente_obj = mapa[nome_escolhido]
            nova_reserva = Reserva(
                id=len(self.banco.reservas.listar_todos()) + 1,
                cliente=cliente_obj
            )
            janela.destroy()
            self._add_destino(cliente_obj, nova_reserva)

        Button(janela, text="Continuar", width=20, command=continuar).pack(pady=10)
        Button(janela, text="Adicionar Cliente", width=20, command=lambda: self.inserir_cliente_reserva(repo, combo)).pack(pady=5)


    def inserir_cliente_reserva(self, repo, combo):

        janela = Toplevel(self.janela)
        janela.title("Inserir Cliente")
        janela.geometry("300x200")

        Label(janela, text="ID:").pack()
        entry_id = Entry(janela)
        entry_id.pack()

        Label(janela, text="Nome:").pack()
        entry_nome = Entry(janela)
        entry_nome.pack()

        Label(janela, text="Email:").pack()
        entry_email = Entry(janela)
        entry_email.pack()

        def salvar():
            id_cliente = int(entry_id.get())
            nome = entry_nome.get()
            email = entry_email.get()

            novo = Cliente(id_cliente, nome, email) 
            repo.inserir(novo)

            mapa = {cliente.nome: cliente for cliente in repo.listar_todos()}
            combo["values"] = list(mapa.keys())

            janela.destroy()

        Button(janela, text="Salvar", command=salvar).pack(pady=10) 

    def _add_destino(self, cliente, reserva):
        janela = Toplevel(self.janela)
        janela.title("Adicionar Destino")

        Label(janela, text=f"Cliente: {cliente.nome}").pack(pady=5)
        Label(janela, text="Selecione um destino:").pack(pady=5)

        destinos = self.banco.destinos.listar_todos()

        listbox = Listbox(janela, width=70, height=10)
        listbox.pack()

        for d in destinos:
            listbox.insert(END, f"{d.id} - {d.cidade} - R$ {d.valor_diaria:.2f}")

        Label(janela, text="Dias:").pack(pady=5)
        entry_dias = Entry(janela)
        entry_dias.pack(pady=5)

        def salvar_item():
            idx = listbox.curselection()[0]
            destino = destinos[idx]
            dias = int(entry_dias.get())

            reserva.adicionar_item(ItemReserva(destino, dias))
            janela.destroy()
            self.perguntar_outro_destino(cliente, reserva)

        Button(janela, text="Adicionar Item", command=salvar_item).pack(pady=10)

    def perguntar_outro_destino(self, cliente, reserva):
        janela = Toplevel(self.janela)
        janela.title("Continuar?")

        Label(janela, text="Deseja adicionar outro destino?").pack(pady=10)

        def sim():
            janela.destroy()
            self._add_destino(cliente, reserva)

        def nao():
            janela.destroy()    
            self.tela_pagamento(reserva)

        Button(janela, text="Sim", width=15, command=sim).pack(pady=5)
        Button(janela, text="Não", width=15, command=nao).pack(pady=5)

    def tela_pagamento(self, reserva):
        janela = Toplevel(self.janela)
        janela.title("Pagamento")

        Label(janela, text="Método de Pagamento:").pack(pady=5)

        var_pag = IntVar()
        var_pag.set(2)

        Radiobutton(janela, text="Pix (Desconto de 2%)", variable=var_pag, value=1).pack(anchor="w")
        Radiobutton(janela, text="Débito (sem alteração)", variable=var_pag, value=2).pack(anchor="w")
        Radiobutton(janela, text="Crédito (3% juros)", variable=var_pag, value=3).pack(anchor="w")

        frame_credito = Frame(janela)
        frame_credito.pack(pady=10)

        label_parc = Label(frame_credito, text="")
        label_parc.pack()

        combo_parc = None

        def atualizar_credito(*args):

            nonlocal combo_parc
            if var_pag.get() == 3:
                total = reserva.custo_bruto() * 1.03
                label_parc.config(text=f"Total com juros: R$ {total:.2f}")

                if combo_parc:
                    combo_parc.destroy()

                combo_parc = Combobox(frame_credito, values=["1x", "2x", "3x", "4x", "5x"])
                combo_parc.current(0)
                combo_parc.pack(pady=5)
            else:
                label_parc.config(text="")
                if combo_parc:
                    combo_parc.destroy()
                    combo_parc = None

        var_pag.trace_add("write", atualizar_credito)

        def finalizar():
            metodo = var_pag.get()
            reserva.metodo_pagamento = metodo
            self.banco.reservas.inserir(reserva)
            self._gui_reservas()
            janela.destroy()

        Button(janela, text="Finalizar Reserva", width=20, command=finalizar).pack(pady=10)

    def alterar_reserva(self):

        janela = Toplevel(self.janela)
        janela.title("Alterar Reserva")
        repo = self.banco.reservas

        Label(janela, text="Selecione a Reserva:").pack(pady=5)
        nomes = [f"{res.id} - {res.cliente.nome}" for res in repo.listar_todos()]
        combo = Combobox(janela, values=nomes, state="readonly")
        combo.pack(pady=5)

        def carregar():
            item = combo.get()
            if not item:
                return
            
            rid = int(item.split(" - ")[0])
            reserva = repo.buscar_por_id(rid)

            janela.destroy()
            self.tela_editar_reserva(reserva)

        Button(janela, text="Carregar", width=20, command=carregar).pack(pady=10)

    
    def tela_editar_reserva(self, reserva):

        janela = Toplevel(self.janela)
        janela.geometry("600x400")
        janela.title(f"Editando Reserva {reserva.id}")
        Label(janela, text=f"Cliente: {reserva.cliente.id} - {reserva.cliente.nome}").pack(pady=5)
        Label(janela, text=f"Método de pagamento atual: {reserva.metodo_pagamento}").pack(pady=5)
        Label(janela, text="Destinos da Reserva:").pack(pady=5)

        frame_itens = Frame(janela)
        frame_itens.pack()

        def atualizar_lista():
            for widget in frame_itens.winfo_children():
                widget.destroy()

            for idx, item in enumerate(reserva.itens):
                Label(frame_itens, text=f"{idx} - {item.destino.cidade} ({item.dias} dias)").grid(row=idx, column=0, sticky="w")
                Button(frame_itens, text="Apagar",command=lambda i=idx: remover_item(i)).grid(row=idx, column=1, padx=10)

        def remover_item(i):
            reserva.remover_item(i)
            atualizar_lista()

        atualizar_lista()

        def adicionar_destino():
            j = Toplevel(janela)
            j.title("Adicionar Destino")

            Label(j, text="Destino:").pack(pady=5)
            mapa_destinos = {d.cidade: d for d in self.banco.destinos.listar_todos()}
            nomes_destinos = list(mapa_destinos.keys())
            combo = Combobox(j, values=nomes_destinos, state="readonly", width=30)
            combo.pack()

            Label(j, text="Dias:").pack(pady=5)
            e_dias = Entry(j)
            e_dias.pack()

            def confirmar():
                selecionado = combo.get()

                destino = mapa_destinos[selecionado]
                dias = int(e_dias.get())

                reserva.adicionar_item(ItemReserva(destino, dias))
                atualizar_lista()
                j.destroy()

            Button(j, text="Adicionar", width=20, command=confirmar).pack(pady=10)

        Button(janela, text="Adicionar Destino", width=20, command=adicionar_destino).pack(pady=10)
        Button(janela, text="Alterar Pagamento", width=20, command=lambda: self.tela_pagamento_reserva(reserva)).pack(pady=10)

        def salvar():
            self.banco.reservas.alterar(reserva)
            self._gui_reservas()
            janela.destroy()

        Button(janela, text="Salvar Alterações", width=20, command=salvar).pack(pady=10)

    def tela_pagamento_reserva(self, reserva):
        janela = Toplevel(self.janela)
        janela.title("Pagamento")

        Label(janela, text="Método de Pagamento:").pack(pady=5)

        var_pag = IntVar()
        var_pag.set(2)

        Radiobutton(janela, text="Pix (Desconto de 2%)", variable=var_pag, value=1).pack(anchor="w")
        Radiobutton(janela, text="Débito (sem alteração)", variable=var_pag, value=2).pack(anchor="w")
        Radiobutton(janela, text="Crédito (3% juros)", variable=var_pag, value=3).pack(anchor="w")

        frame_credito = Frame(janela)
        frame_credito.pack(pady=10)

        label_parc = Label(frame_credito, text="")
        label_parc.pack()

        combo_parc = None

        def atualizar_credito(*args):

            nonlocal combo_parc
            if var_pag.get() == 3:
                total = reserva.custo_bruto() * 1.03
                label_parc.config(text=f"Total com juros: R$ {total:.2f}")

                if combo_parc:
                    combo_parc.destroy()

                combo_parc = Combobox(frame_credito, values=["1x", "2x", "3x", "4x", "5x"])
                combo_parc.current(0)
                combo_parc.pack(pady=5)
            else:
                label_parc.config(text="")
                if combo_parc:
                    combo_parc.destroy()
                    combo_parc = None

        var_pag.trace_add("write", atualizar_credito)

        def finalizar1():
            metodo = var_pag.get()
            reserva.metodo_pagamento = metodo
            self.banco.reservas.alterar(reserva)
            janela.destroy()

        Button(janela, text="Finalizar Reserva", width=20, command=finalizar1).pack(pady=10)

    def apagar_reserva(self):

        janela = Toplevel(self.janela)
        janela.title("Excluir Reserva")

        Label(janela, text="Selecione a Reserva para excluir:").pack(pady=5)
        repo = self.banco.reservas
        mapa = {reserva.cliente.nome: reserva for reserva in repo.listar_todos()}
        nomes = list(mapa.keys())
        combo = Combobox(janela, values=nomes, state="readonly")
        combo.pack(pady=5)

        def excluir():
            nome = combo.get()
            if not nome:
                return
            reserva = mapa[nome]
            self.banco.reservas.excluir(reserva.id)

            self._gui_reservas()

        Button(janela, text="Excluir", width=20, command=excluir).pack(pady=10)

