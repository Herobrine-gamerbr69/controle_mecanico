import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ================= BANCO DE DADOS =================
def criar_banco():
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_cliente TEXT NOT NULL,
            tipo_servico TEXT NOT NULL,
            tipo_carro TEXT NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()

# ================= CLASSE DO SISTEMA =================
class SistemaMecanico:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x200")

        tk.Label(root, text="Usuário:").pack()
        self.entrada_usuario = tk.Entry(root)
        self.entrada_usuario.pack()

        tk.Label(root, text="Senha:").pack()
        self.entrada_senha = tk.Entry(root, show="*")
        self.entrada_senha.pack()

        tk.Button(root, text="Entrar", command=self.fazer_login).pack(pady=5)
        tk.Button(root, text="Cadastrar Novo Usuário", command=self.abrir_tela_cadastro).pack()

    def abrir_tela_cadastro(self):
        tela = tk.Toplevel()
        tela.title("Cadastro de Novo Usuário")
        tela.geometry("300x150")

        tk.Label(tela, text="Novo Usuário:").pack()
        entrada_novo_usuario = tk.Entry(tela)
        entrada_novo_usuario.pack()

        tk.Label(tela, text="Nova Senha:").pack()
        entrada_nova_senha = tk.Entry(tela, show="*")
        entrada_nova_senha.pack()

        def cadastrar():
            usuario = entrada_novo_usuario.get()
            senha = entrada_nova_senha.get()
            if not usuario or not senha:
                messagebox.showwarning("Atenção", "Preencha todos os campos!")
                return
            conexao = sqlite3.connect("banco.db")
            cursor = conexao.cursor()
            try:
                cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
                conexao.commit()
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
                tela.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Usuário já existe!")
            finally:
                conexao.close()

        tk.Button(tela, text="Cadastrar", command=cadastrar).pack(pady=10)

    def fazer_login(self):
        usuario = self.entrada_usuario.get()
        senha = self.entrada_senha.get()

        conexao = sqlite3.connect("banco.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
        resultado = cursor.fetchone()
        conexao.close()

        if resultado:
            self.root.destroy()
            self.abrir_tela_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")

    def abrir_tela_principal(self):
        janela = tk.Tk()
        janela.title("Controle de Serviços")
        janela.geometry("700x500")

        tk.Label(janela, text="Nome do Cliente").grid(row=0, column=0)
        entrada_nome = tk.Entry(janela)
        entrada_nome.grid(row=0, column=1)

        tk.Label(janela, text="Tipo de Serviço").grid(row=1, column=0)
        entrada_servico = tk.Entry(janela)
        entrada_servico.grid(row=1, column=1)

        tk.Label(janela, text="Tipo de Carro").grid(row=2, column=0)
        entrada_carro = tk.Entry(janela)
        entrada_carro.grid(row=2, column=1)

        def cadastrar():
            nome = entrada_nome.get()
            servico = entrada_servico.get()
            carro = entrada_carro.get()
            if not nome or not servico or not carro:
                messagebox.showwarning("Atenção", "Preencha todos os campos!")
                return
            conexao = sqlite3.connect("banco.db")
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO servicos (nome_cliente, tipo_servico, tipo_carro) VALUES (?, ?, ?)",
                           (nome, servico, carro))
            conexao.commit()
            conexao.close()
            listar()

        def excluir():
            item = tabela.selection()
            if not item:
                messagebox.showwarning("Atenção", "Selecione um serviço para excluir")
                return
            id_servico = tabela.item(item)['values'][0]
            conexao = sqlite3.connect("banco.db")
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM servicos WHERE id = ?", (id_servico,))
            conexao.commit()
            conexao.close()
            listar()

        def editar():
            item = tabela.selection()
            if not item:
                messagebox.showwarning("Atenção", "Selecione um serviço para editar")
                return
            valores = tabela.item(item)['values']
            id_servico = valores[0]
            entrada_nome.delete(0, tk.END)
            entrada_servico.delete(0, tk.END)
            entrada_carro.delete(0, tk.END)
            entrada_nome.insert(0, valores[1])
            entrada_servico.insert(0, valores[2])
            entrada_carro.insert(0, valores[3])

            def salvar_edicao():
                novo_nome = entrada_nome.get()
                novo_servico = entrada_servico.get()
                novo_carro = entrada_carro.get()
                conexao = sqlite3.connect("banco.db")
                cursor = conexao.cursor()
                cursor.execute("""
                    UPDATE servicos SET nome_cliente = ?, tipo_servico = ?, tipo_carro = ? WHERE id = ?
                """, (novo_nome, novo_servico, novo_carro, id_servico))
                conexao.commit()
                conexao.close()
                listar()
                tk.messagebox.showinfo("Sucesso", "Serviço atualizado!")

            tk.Button(janela, text="Salvar Edição", command=salvar_edicao).grid(row=6, column=1)

        def listar():
            for i in tabela.get_children():
                tabela.delete(i)
            conexao = sqlite3.connect("banco.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM servicos")
            for row in cursor.fetchall():
                tabela.insert("", "end", values=row)
            conexao.close()

        def abrir_relatorio():
            relatorio = tk.Toplevel()
            relatorio.title("Relatório de Serviços")
            relatorio.geometry("500x400")
            rel_tabela = ttk.Treeview(relatorio, columns=("ID", "Cliente", "Serviço", "Carro"), show="headings")
            for col in ("ID", "Cliente", "Serviço", "Carro"):
                rel_tabela.heading(col, text=col)
            rel_tabela.pack(fill=tk.BOTH, expand=True)

            conexao = sqlite3.connect("banco.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM servicos")
            for row in cursor.fetchall():
                rel_tabela.insert("", "end", values=row)
            conexao.close()

        tk.Button(janela, text="Cadastrar Serviço", command=cadastrar).grid(row=3, column=0, columnspan=2, pady=5)
        tk.Button(janela, text="Editar Serviço", command=editar).grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(janela, text="Excluir Serviço", command=excluir).grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(janela, text="Relatórios", command=abrir_relatorio).grid(row=7, column=0, columnspan=2, pady=10)

        tabela = ttk.Treeview(janela, columns=("ID", "Cliente", "Serviço", "Carro"), show="headings")
        for col in ("ID", "Cliente", "Serviço", "Carro"):
            tabela.heading(col, text=col)
        tabela.grid(row=8, column=0, columnspan=2)

        listar()
        janela.mainloop()

# ================= EXECUTAR =================
criar_banco()
root = tk.Tk()
SistemaMecanico(root)
root.mainloop()

    

