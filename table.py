import sqlite3

# Cria uma conexão global com o banco de dados
conn = sqlite3.connect("financial_records.db", check_same_thread=False)  # check_same_thread=False permite o uso em múltiplas threads
cursor = conn.cursor()

# Função para inicializar o banco de dados
def init_db():
    conn = sqlite3.connect("financial_records.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Registros (
            id INTEGER PRIMARY KEY,
            data TEXT,
            condominio TEXT,
            inquilino TEXT,
            valor REAL,
            receita TEXT,
            observacao TEXT,
            predio TEXT,
            categoria TEXT,
            socios TEXT,
            percentual_predio_a REAL,
            percentual_predio_b REAL
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized with updated schema.")

# Chame init_db para garantir que o banco de dados esteja inicializado
init_db()

# Certifique-se de fechar a conexão ao sair do aplicativo
import atexit
atexit.register(conn.close)
