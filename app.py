from datetime import datetime
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Inicializar a janela principal
root = ttkb.Window(themename="cyborg")
root.title("Gerenciador Financeiro")
root.geometry("1400x700")
root.resizable(False, False)

# Conectar e criar o banco de dados com a nova coluna 'tipo' e 'valor_despesas'
def init_db():
    conn = sqlite3.connect("financial_records.db")
    cursor = conn.cursor()

    # Criar tabela e colunas se ainda não existirem
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Registros (
            id INTEGER PRIMARY KEY,
            data TEXT,
            receita TEXT,
            inquilino TEXT,
            valor REAL,
            tipo TEXT,
            observacao TEXT,
            predio TEXT,
            categoria TEXT,
            despesas_observacao TEXT,
            valor_despesas REAL,
            socios TEXT,
            percentual_predio_a REAL,
            percentual_predio_b REAL
        )
    ''')
    conn.commit()
    conn.close()
    print("Banco de dados inicializado e atualizado.")

init_db()

# Variável global para armazenar o ID do último registro inserido
last_record_id = None

# Função para adicionar placeholders nos Entry widgets
def add_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.config(foreground="grey")

    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, "end")
            entry.config(foreground="white")

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder_text)
            entry.config(foreground="grey")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# Função para abrir a janela de Lançamento de Receitas
def open_add_receita_window():
    add_receita_window = tk.Toplevel(root)
    add_receita_window.title("Lançamento de Receitas")
    add_receita_window.geometry("400x450")

    # Título
    ttkb.Label(add_receita_window, text="Lançamento de Receitas", font="-size 16 -weight bold").pack(pady=20)

    # Campos com placeholders
    entries = {}
    fields = {
        "Receita": "Digite a receita",
        "Inquilino": "Digite o inquilino",
        "Valor (R$)": "Digite o valor",
        "Tipo": "Tipo de receita",
        "Observação": "Observações"
    }
    
    for field, placeholder in fields.items():
        entry = ttkb.Entry(add_receita_window, width=40)
        entry.pack(padx=20, pady=10)
        add_placeholder(entry, placeholder)
        entries[field] = entry

    # Campo adicional para Data com placeholder
    data_entry = ttkb.Entry(add_receita_window, width=40)
    data_entry.pack(padx=20, pady=10)
    add_placeholder(data_entry, "Data (YYYY-MM-DD)")

    # Função para salvar a receita no banco de dados e abrir a interface de despesas
    def save_receita():
        global last_record_id
        data = data_entry.get()

        # Validar o formato de data
        try:
            datetime.strptime(data, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erro", "Data inválida! Use o formato YYYY-MM-DD.")
            return

        # Conectar ao banco de dados e inserir os dados
        conn = sqlite3.connect("financial_records.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Registros (data, receita, inquilino, valor, tipo, observacao)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data, entries["Receita"].get(), entries["Inquilino"].get(), float(entries["Valor (R$)"].get()), entries["Tipo"].get(), entries["Observação"].get()))

        # Obter o ID do último registro inserido
        last_record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        update_table()
        add_receita_window.destroy()
        open_add_despesa_window()

    # Botão para salvar o registro
    ttkb.Button(add_receita_window, text="Salvar Receita", command=save_receita).pack(pady=20)

# Função para abrir a janela de Lançamento de Despesas
def open_add_despesa_window():
    add_despesa_window = tk.Toplevel(root)
    add_despesa_window.title("Lançamento de Despesas")
    add_despesa_window.geometry("400x400")

    # Título
    ttkb.Label(add_despesa_window, text="Lançamento de Despesas", font="-size 16 -weight bold").pack(pady=20)

    # Campos com placeholders
    entries = {}
    fields = {
        "Prédio": "Digite o prédio",
        "Categoria": "Digite a categoria",
        "Despesas_Observação": "Observação de despesas",
        "Valor Despesas": "Digite o valor da despesa"
    }
    
    for field, placeholder in fields.items():
        entry = ttkb.Entry(add_despesa_window, width=40)
        entry.pack(padx=20, pady=10)
        add_placeholder(entry, placeholder)
        entries[field] = entry

    # Função para salvar a despesa no banco de dados e abrir a interface de lucros
    def save_despesa():
        global last_record_id
        # Conectar ao banco de dados e atualizar o registro existente com as informações de despesas
        conn = sqlite3.connect("financial_records.db")
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Registros
            SET predio = ?, categoria = ?, despesas_observacao = ?, valor_despesas = ?
            WHERE id = ?
        ''', (entries["Prédio"].get(), entries["Categoria"].get(), entries["Despesas_Observação"].get(), float(entries["Valor Despesas"].get()), last_record_id))

        conn.commit()
        conn.close()
        update_table()
        add_despesa_window.destroy()
        open_add_lucro_window()

    # Botão para salvar a despesa
    ttkb.Button(add_despesa_window, text="Salvar Despesa", command=save_despesa).pack(pady=20)

# Função para abrir a janela de Distribuição de Lucros
def open_add_lucro_window():
    add_lucro_window = tk.Toplevel(root)
    add_lucro_window.title("Distribuição de Lucros")
    add_lucro_window.geometry("400x350")

    # Título
    ttkb.Label(add_lucro_window, text="Distribuição de Lucros", font="-size 16 -weight bold").pack(pady=20)

    # Campos com placeholders
    entries = {}
    fields = {
        "Sócio": "Digite o sócio",
        "P% do Prédio A": "Percentual do Prédio A",
        "P% do Prédio B": "Percentual do Prédio B"
    }
    
    for field, placeholder in fields.items():
        entry = ttkb.Entry(add_lucro_window, width=40)
        entry.pack(padx=20, pady=10)
        add_placeholder(entry, placeholder)
        entries[field] = entry

    # Função para salvar a distribuição de lucros no banco de dados
    def save_lucro():
        global last_record_id
        # Conectar ao banco de dados e atualizar o registro existente com as informações de lucros
        conn = sqlite3.connect("financial_records.db")
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Registros
            SET socios = ?, percentual_predio_a = ?, percentual_predio_b = ?
            WHERE id = ?
        ''', (entries["Sócio"].get(), float(entries["P% do Prédio A"].get()), float(entries["P% do Prédio B"].get()), last_record_id))

        conn.commit()
        conn.close()
        update_table()
        add_lucro_window.destroy()

    # Botão para salvar a distribuição de lucros
    ttkb.Button(add_lucro_window, text="Salvar Lucro", command=save_lucro).pack(pady=20)

# Função para abrir o menu de contexto (Editar e Excluir) na tabela
def open_context_menu(event):
    # Obter o item da linha onde o clique direito foi feito
    selected_item = tree.identify_row(event.y)
    if selected_item:
        # Selecionar a linha onde o clique foi feito
        tree.selection_set(selected_item)
        
        # Criar o menu de contexto
        context_menu = tk.Menu(root, tearoff=0)
        context_menu.add_command(label="Editar", command=lambda: edit_record(selected_item))
        context_menu.add_command(label="Excluir", command=lambda: delete_record(selected_item))
        
        # Exibir o menu de contexto
        context_menu.tk_popup(event.x_root, event.y_root)

# Função para editar o registro com o uso do iid para o ID
def edit_record(item_id):
    # Obter os valores do item selecionado
    record = tree.item(item_id, "values")
    if not record:
        messagebox.showerror("Erro", "Registro não encontrado.")
        return

    # Abrir uma nova janela de edição com os valores preenchidos
    edit_window = tk.Toplevel(root)
    edit_window.title("Editar Registro")
    edit_window.geometry("450x500")
    edit_window.resizable(False, False)

    # Canvas e Scrollbar para adicionar rolagem
    canvas = tk.Canvas(edit_window)
    scrollbar = ttkb.Scrollbar(edit_window, orient="vertical", command=canvas.yview)
    scrollable_frame = ttkb.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="center")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Função de rolagem
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Habilitar rolagem com o scroll do mouse enquanto a janela está aberta
    scrollable_frame.bind("<MouseWheel>", on_mouse_wheel)

    # Campos de edição com placeholders centralizados
    fields = ["Data", "Receita", "Inquilino", "Valor Receitas", "Tipo Receitas", "Observacao", "Predio", 
              "Categoria", "Despesas_Observação", "Valor Despesas", "Socios", "P% Predio A", "P% Predio B"]
    entries = {}

    for index, field in enumerate(fields):
        entry = ttkb.Entry(scrollable_frame, width=40, font="-size 12")
        entry.pack(padx=20, pady=10, anchor="center")
        entry.insert(0, record[index])
        entry.config(foreground="white")
        entries[field] = entry

    # Função para salvar o registro editado
    def save_edited_record():
        try:
            updated_values = {field: entry.get() for field, entry in entries.items()}
            
            # Conectar ao banco de dados e atualizar o registro
            conn = sqlite3.connect("financial_records.db")
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Registros SET
                data = ?, receita = ?, inquilino = ?, valor = ?, tipo = ?, observacao = ?,
                predio = ?, categoria = ?, despesas_observacao = ?, valor_despesas = ?,
                socios = ?, percentual_predio_a = ?, percentual_predio_b = ?
                WHERE id = ?
            ''', (
                updated_values["Data"], updated_values["Receita"], updated_values["Inquilino"], 
                float(updated_values["Valor Receitas"]), updated_values["Tipo Receitas"], 
                updated_values["Observacao"], updated_values["Predio"], updated_values["Categoria"], 
                updated_values["Despesas_Observação"], float(updated_values["Valor Despesas"]), 
                updated_values["Socios"], float(updated_values["P% Predio A"]), 
                float(updated_values["P% Predio B"]), int(item_id)  # Uso direto de item_id como ID
            ))

            conn.commit()
            conn.close()
            
            # Atualizar a tabela e fechar a janela de edição
            update_table()
            edit_window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar o registro: {e}")

    ttkb.Button(scrollable_frame, text="Salvar Alterações", command=save_edited_record).pack(pady=20)

    # Layout para o Canvas e Scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

# Função para excluir o registro
def delete_record(item_id):
    # Conectar ao banco de dados e deletar o registro
    conn = sqlite3.connect("financial_records.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Registros WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    
    # Remover o item da tabela e atualizar a interface
    tree.delete(item_id)
    update_table()

# Função para carregar dados financeiros filtrados por mês e ano
def load_data(month, year):
    conn = sqlite3.connect("financial_records.db")
    cursor = conn.cursor()
    month_number = str(months.index(month) + 1).zfill(2)
    cursor.execute('''
        SELECT id, data, receita, inquilino, valor, tipo, observacao, predio, categoria, despesas_observacao, 
               valor_despesas, socios, percentual_predio_a, percentual_predio_b 
        FROM Registros 
        WHERE strftime('%m', data) = ? AND strftime('%Y', data) = ? 
        ORDER BY data ASC
    ''', (month_number, year))
    rows = cursor.fetchall()
    conn.close()
    return rows

# Exibir dados na tabela
def update_table():
    selected_month = month_var.get()
    selected_year = year_var.get()

    # Limpar conteúdo atual da tabela
    for i in tree.get_children():
        tree.delete(i)
    
    # Carregar dados financeiros filtrados por mês e ano
    data = load_data(selected_month, selected_year)
    
    # Inserir dados na Treeview com o ID do banco como iid
    for row in data:
        formatted_row = list(row[1:])  # Excluindo o ID do registro ao inserir os valores
        try:
            formatted_row[0] = datetime.strptime(formatted_row[0], "%Y-%m-%d").strftime("%d/%m/%Y")
        except ValueError:
            pass
        # Define o id do registro como iid do item na Treeview
        tree.insert("", "end", iid=row[0], values=formatted_row)

# Frame para o menu de seleção de mês e ano
menu_frame = ttkb.Frame(root, padding=10)
menu_frame.pack(fill="x", pady=10)

# Seleção de mês
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
month_var = tk.StringVar(value=months[0])
ttkb.Label(menu_frame, text="Selecione o Mês:", font=('Helvetica', 12)).pack(side="left", padx=10)
month_menu = ttk.Combobox(menu_frame, textvariable=month_var, values=months, width=10)
month_menu.pack(side="left", padx=5)

# Seleção de ano
years = ["2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026", "2027"]
year_var = tk.StringVar(value=years[0])
ttkb.Label(menu_frame, text="Selecione o Ano:", font=('Helvetica', 12)).pack(side="left", padx=10)
year_menu = ttk.Combobox(menu_frame, textvariable=year_var, values=years, width=10)
year_menu.pack(side="left", padx=5)

# Botão para abrir a janela de adição de receita
ttkb.Button(menu_frame, text="Adicionar Gestão", command=open_add_receita_window).pack(side="right", padx=20)

# Frame para a tabela
table_frame = ttkb.Frame(root, padding=10)
table_frame.pack(fill="both", expand=True)

# Configuração da tabela
columns = ["Data", "Receita", "Inquilino", "Valor Receitas", "Tipo Receitas", "Observacao", "Predio", "Categoria", "Despesas_Observação", "Valor Despesas", "Socios", "P% Predio A", "P% Predio B"]
tree = ttkb.Treeview(table_frame, columns=columns, show='headings', height=15, style="dark.Treeview")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=100)

tree.pack(fill="both", expand=True, padx=10, pady=10)

tree.bind("<Button-3>", open_context_menu)

# Atualizar a tabela ao iniciar e ao alterar mês ou ano
update_table()
month_menu.bind("<<ComboboxSelected>>", lambda e: update_table())
year_menu.bind("<<ComboboxSelected>>", lambda e: update_table())

# Rodar a aplicação
root.mainloop()
