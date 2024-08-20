# frontend.py
from tkinter import *
from tkinter import messagebox
from backend import TransactionObject

class Gui:
    x_pad = 5
    y_pad = 3
    width_entry = 30

    def __init__(self, window):
        self.window = window
        self.window.wm_title("PYSQL versão 1.0")

        # Definição das variáveis que recebem os dados inseridos pelo usuário
        self.txtNome = StringVar()
        self.txtSobrenome = StringVar()
        self.txtEmail = StringVar()
        self.txtCPF = StringVar()

        # Criando os objetos que farão parte das janelas
        self.lblnome = Label(self.window, text="Nome")
        self.lblsobrenome = Label(self.window, text="Sobrenome")
        self.lblemail = Label(self.window, text="Email")
        self.lblcpf = Label(self.window, text="CPF")

        self.entNome = Entry(self.window, textvariable=self.txtNome, width=self.width_entry)
        self.entSobrenome = Entry(self.window, textvariable=self.txtSobrenome, width=self.width_entry)
        self.entEmail = Entry(self.window, textvariable=self.txtEmail, width=self.width_entry)
        self.entCPF = Entry(self.window, textvariable=self.txtCPF, width=self.width_entry)

        self.listClientes = Listbox(self.window, width=100)
        self.scrollClientes = Scrollbar(self.window)

        self.btnViewAll = Button(self.window, text="Ver todos", command=self.view_all)
        self.btnBuscar = Button(self.window, text="Buscar", command=self.search)
        self.btnInserir = Button(self.window, text="Inserir", command=self.insert)
        self.btnUpdate = Button(self.window, text="Atualizar Selecionados", command=self.update)
        self.btnDel = Button(self.window, text="Deletar Selecionados", command=self.delete)
        self.btnClose = Button(self.window, text="Fechar", command=self.window.quit)

        # Posicionando os widgets na grade
        self.lblnome.grid(row=0, column=0)
        self.lblsobrenome.grid(row=1, column=0)
        self.lblemail.grid(row=2, column=0)
        self.lblcpf.grid(row=3, column=0)

        self.entNome.grid(row=0, column=1, padx=50, pady=50)
        self.entSobrenome.grid(row=1, column=1)
        self.entEmail.grid(row=2, column=1)
        self.entCPF.grid(row=3, column=1)

        self.listClientes.grid(row=0, column=2, rowspan=10)
        self.scrollClientes.grid(row=0, column=3, rowspan=10)

        self.btnViewAll.grid(row=4, column=0, columnspan=2)
        self.btnBuscar.grid(row=5, column=0, columnspan=2)
        self.btnInserir.grid(row=6, column=0, columnspan=2)
        self.btnUpdate.grid(row=7, column=0, columnspan=2)
        self.btnDel.grid(row=8, column=0, columnspan=2)
        self.btnClose.grid(row=9, column=0, columnspan=2)

        # União do Scrollbar com a Listbox
        self.listClientes.configure(yscrollcommand=self.scrollClientes.set)
        self.scrollClientes.configure(command=self.listClientes.yview)

        # Adicionar SWAG (aparência) à interface
        for child in self.window.winfo_children():
            widget_class = child.__class__.__name__
            if widget_class == "Button":
                child.grid_configure(sticky='WE', padx=self.x_pad, pady=self.y_pad)
            elif widget_class == "Listbox":
                child.grid_configure(padx=0, pady=0, sticky='NS')
            elif widget_class == "Scrollbar":
                child.grid_configure(padx=0, pady=0, sticky='NS')
            else:
                child.grid_configure(padx=self.x_pad, pady=self.y_pad, sticky='N')

    # Função para ver todos os clientes
    def view_all(self):
        self.listClientes.delete(0, END)
        trans = TransactionObject()
        trans.connect()
        trans.execute("SELECT * FROM clientes")
        rows = trans.fetchall()
        for row in rows:
            self.listClientes.insert(END, row)
        trans.disconnect()

    # Função para buscar clientes
    def search(self):
        self.listClientes.delete(0, END)
        trans = TransactionObject()
        trans.connect()
        trans.execute("SELECT * FROM clientes WHERE nome=? OR sobrenome=? OR email=? OR cpf=?",
                      (self.txtNome.get(), self.txtSobrenome.get(), self.txtEmail.get(), self.txtCPF.get()))
        rows = trans.fetchall()
        for row in rows:
            self.listClientes.insert(END, row)
        trans.disconnect()

    # Função para inserir um novo cliente
    def insert(self):
        trans = TransactionObject()
        trans.connect()
        trans.execute("INSERT INTO clientes (nome, sobrenome, email, cpf) VALUES (?, ?, ?, ?)",
                      (self.txtNome.get(), self.txtSobrenome.get(), self.txtEmail.get(), self.txtCPF.get()))
        trans.persist()
        trans.disconnect()
        self.view_all()

    # Função para atualizar um cliente selecionado
    def update(self):
        try:
            selected_item = self.listClientes.curselection()[0]
            selected_cliente = self.listClientes.get(selected_item)
            trans = TransactionObject()
            trans.connect()
            trans.execute("UPDATE clientes SET nome=?, sobrenome=?, email=?, cpf=? WHERE id=?",
                          (self.txtNome.get(), self.txtSobrenome.get(), self.txtEmail.get(), self.txtCPF.get(), selected_cliente[0]))
            trans.persist()
            trans.disconnect()
            self.view_all()
        except IndexError:
            messagebox.showerror("Erro", "Por favor, selecione um cliente para atualizar.")

    # Função para deletar um cliente selecionado
    def delete(self):
        try:
            selected_item = self.listClientes.curselection()[0]
            selected_cliente = self.listClientes.get(selected_item)
            trans = TransactionObject()
            trans.connect()
            trans.execute("DELETE FROM clientes WHERE id=?", (selected_cliente[0],))
            trans.persist()
            trans.disconnect()
            self.view_all()
        except IndexError:
            messagebox.showerror("Erro", "Por favor, selecione um cliente para deletar.")

    def run(self):
        self.window.mainloop()
