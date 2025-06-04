import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# ==== CRIAR BANCO E TABELAS ====
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

# ==== CADASTRAR NOVO USUÁRIO ====
def cadastrar_usuario():
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
        tela_cadastro.destroy()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Usuário já existe!")
    finally:
        conexao.close()

# ==== ABRIR TELA DE CADASTRO ====
def abrir_tela_cadastro():
    global tela_cadastro, entrada_novo_usuario, entrada_nova_senha
    tela_cadastro = tk.Toplevel()
    tela_cadastro.title("Cadastro de Novo Usuário")
    tela_cadastro.geometry("300x150")

    tk.Label(tela_cadastro, text="Novo Usuário:").pack()
    entrada_novo_usuario = tk.Entry(tela_cadastro)
    entrada_novo_usuario.pack()

    tk.Label(tela_cadastro, text="Nova Senha:").pack()
    entrada_nova_senha = tk.Entry(tela_cadastro, show="*")
    entrada_nova_senha.pack()

    tk.Button(tela_cadastro, text="Cadastrar", command=cadastrar_usuario).pack(pady=10)

# ==== FAZER LOGIN ====
def fazer_login():
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
    resultado = cursor.fetchone()
    conexao.close()

    if resultado:
        janela_login.destroy()
        abrir_sistema()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos")

# ==== CADASTRAR SERVIÇO ====
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

# ==== LISTAR SERVIÇOS ====
def listar_servicos():
    for item in tabela.get_children():
        tabela.delete(item)
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM servicos")
    for row in cursor.fetchall():
        tabela.insert("", "end", values=row)
    conexao.close()

# ==== EXCLUIR SERVIÇO ====
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

# ==== ABRIR SISTEMA PRINCIPAL ====
def abrir_sistema():
    global entrada_nome, entrada_servico, entrada_carro, tabela

    janela = tk.Tk()
    janela.title("Controle de Serviços do Mecânico")
    janela.geometry("600x400")

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

    tabela = ttk.Treeview(janela, columns=("ID", "Cliente", "Serviço", "Carro"), show="headings")
    tabela.heading("ID", text="ID")
    tabela.heading("Cliente", text="Cliente")
    tabela.heading("Serviço", text="Serviço")
    tabela.heading("Carro", text="Carro")
    tabela.grid(row=4, column=0, columnspan=2, pady=10)

    tk.Button(janela, text="Excluir Serviço", command=excluir_servico).grid(row=5, column=0, columnspan=2)

    listar_servicos()
    janela.mainloop()

# ==== INICIAR APLICAÇÃO ====
criar_banco()

janela_login = tk.Tk()
janela_login.title("Login")
janela_login.geometry("300x200")

tk.Label(janela_login, text="Usuário:").pack()
entrada_usuario = tk.Entry(janela_login)
entrada_usuario.pack()

tk.Label(janela_login, text="Senha:").pack()
entrada_senha = tk.Entry(janela_login, show="*")
entrada_senha.pack()

tk.Button(janela_login, text="Entrar", command=fazer_login).pack(pady=5)
tk.Button(janela_login, text="Cadastrar Novo Usuário", command=abrir_tela_cadastro).pack()

janela_login.mainloop()

