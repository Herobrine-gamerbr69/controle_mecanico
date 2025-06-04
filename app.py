import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# ==== Função para criar o banco de dados ====
def criar_banco():
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
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

# ==== Função para login ====
def fazer_login():
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()
    if usuario == "admin" and senha == "admin123":
        janela_login.destroy()
        abrir_sistema()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos")

# ==== Função para cadastrar serviço ====
def cadastrar_servico():
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
    listar_servicos()
    entrada_nome.delete(0, tk.END)
    entrada_servico.delete(0, tk.END)
    entrada_carro.delete(0, tk.END)

# ==== Função para listar serviços ====
def listar_servicos():
    for item in tabela.get_children():
        tabela.delete(item)
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM servicos")
    for row in cursor.fetchall():
        tabela.insert("", "end", values=row)
    conexao.close()

# ==== Função para excluir serviço ====
def excluir_servico():
    item_selecionado = tabela.selection()
    if not item_selecionado:
        messagebox.showwarning("Atenção", "Selecione um serviço para excluir")
        return
    item = tabela.item(item_selecionado)
    id_servico = item['values'][0]

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM servicos WHERE id = ?", (id_servico,))
    conexao.commit()
    conexao.close()
    listar_servicos()

# ==== Interface principal ====
def abrir_sistema():
    global entrada_nome, entrada_servico, entrada_carro, tabela

    janela = tk.Tk()
    janela.title("Controle de Serviços do Mecânico")
    janela.geometry("600x400")

    # Campos de entrada
    tk.Label(janela, text="Nome do Cliente").grid(row=0, column=0)
    entrada_nome = tk.Entry(janela)
    entrada_nome.grid(row=0, column=1)

    tk.Label(janela, text="Tipo de Serviço").grid(row=1, column=0)
    entrada_servico = tk.Entry(janela)
    entrada_servico.grid(row=1, column=1)

    tk.Label(janela, text="Tipo de Carro").grid(row=2, column=0)
    entrada_carro = tk.Entry(janela)
    entrada_carro.grid(row=2, column=1)

    tk.Button(janela, text="Cadastrar Serviço", command=cadastrar_servico).grid(row=3, column=0, columnspan=2, pady=10)

    # Tabela de serviços
    tabela = ttk.Treeview(janela, columns=("ID", "Cliente", "Serviço", "Carro"), show="headings")
    tabela.heading("ID", text="ID")
    tabela.heading("Cliente", text="Cliente")
    tabela.heading("Serviço", text="Serviço")
    tabela.heading("Carro", text="Carro")
    tabela.grid(row=4, column=0, columnspan=2, pady=10)

    tk.Button(janela, text="Excluir Serviço", command=excluir_servico).grid(row=5, column=0, columnspan=2)

    listar_servicos()
    janela.mainloop()

# ==== Interface de login ====
criar_banco()
janela_login = tk.Tk()
janela_login.title("Login")
janela_login.geometry("300x150")

tk.Label(janela_login, text="Usuário:").pack()
entrada_usuario = tk.Entry(janela_login)
entrada_usuario.pack()

tk.Label(janela_login, text="Senha:").pack()
entrada_senha = tk.Entry(janela_login, show="*")
entrada_senha.pack()

tk.Button(janela_login, text="Entrar", command=fazer_login).pack(pady=10)

janela_login.mainloop()
