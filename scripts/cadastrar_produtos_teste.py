import sys
import os
import sqlite3
import random

# Adiciona o diretório raiz ao PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Conecta ao banco de dados
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Primeiro, vamos verificar a estrutura atual da tabela
cursor.execute("PRAGMA table_info(produtos)")
colunas_existentes = [info[1] for info in cursor.fetchall()]
print(f"Colunas existentes na tabela: {colunas_existentes}")

# Se a tabela não existir ou não tiver as colunas necessárias, vamos recriá-la
if not colunas_existentes:
    print("Criando tabela produtos...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE,
            nome TEXT,
            descricao TEXT,
            preco REAL,
            estoque INTEGER,
            categoria TEXT,
            fornecedor TEXT,
            data_cadastro TEXT,
            imagem TEXT
        )
    ''')
    conn.commit()
    print("Tabela produtos criada.")

# Lista de produtos para cadastro
produtos = [
    {
        "codigo": "P001",
        "nome": "Smartphone Galaxy S21",
        "descricao": "Smartphone Samsung Galaxy S21 128GB",
        "preco": 3499.99,
        "estoque": 15,
        "categoria": "Eletrônicos",
        "fornecedor": "Samsung Brasil"
    },
    {
        "codigo": "P002",
        "nome": "Notebook Dell Inspiron",
        "descricao": "Notebook Dell Inspiron 15 8GB RAM 256GB SSD",
        "preco": 4299.99,
        "estoque": 8,
        "categoria": "Informática",
        "fornecedor": "Dell Computadores"
    },
    {
        "codigo": "P003",
        "nome": "Smart TV LG 50\"",
        "descricao": "Smart TV LG 50\" 4K UHD",
        "preco": 2899.99,
        "estoque": 10,
        "categoria": "Eletrônicos",
        "fornecedor": "LG Electronics"
    },
    {
        "codigo": "P004",
        "nome": "Fone de Ouvido JBL",
        "descricao": "Fone de Ouvido JBL Bluetooth",
        "preco": 249.99,
        "estoque": 30,
        "categoria": "Acessórios",
        "fornecedor": "JBL Audio"
    },
    {
        "codigo": "P005",
        "nome": "Mouse Gamer Logitech",
        "descricao": "Mouse Gamer Logitech G502 Hero",
        "preco": 349.99,
        "estoque": 25,
        "categoria": "Informática",
        "fornecedor": "Logitech"
    },
    {
        "codigo": "P006",
        "nome": "Teclado Mecânico Redragon",
        "descricao": "Teclado Mecânico Redragon Kumara RGB",
        "preco": 299.99,
        "estoque": 20,
        "categoria": "Informática",
        "fornecedor": "Redragon"
    },
    {
        "codigo": "P007",
        "nome": "Impressora HP LaserJet",
        "descricao": "Impressora HP LaserJet Pro M428fdw",
        "preco": 2499.99,
        "estoque": 7,
        "categoria": "Informática",
        "fornecedor": "HP Brasil"
    },
    {
        "codigo": "P008",
        "nome": "Caixa de Som Bluetooth",
        "descricao": "Caixa de Som Bluetooth JBL Charge 4",
        "preco": 699.99,
        "estoque": 12,
        "categoria": "Áudio",
        "fornecedor": "JBL Audio"
    },
    {
        "codigo": "P009",
        "nome": "Carregador Portátil",
        "descricao": "Carregador Portátil 10000mAh",
        "preco": 149.99,
        "estoque": 40,
        "categoria": "Acessórios",
        "fornecedor": "Anker"
    },
    {
        "codigo": "P010",
        "nome": "Webcam Logitech C920",
        "descricao": "Webcam Logitech C920 HD Pro",
        "preco": 549.99,
        "estoque": 18,
        "categoria": "Informática",
        "fornecedor": "Logitech"
    }
]

# Função para gerar data de cadastro aleatória nos últimos 30 dias
import datetime
import random

def gerar_data_aleatoria():
    hoje = datetime.datetime.now()
    dias_aleatorios = random.randint(0, 30)
    data_aleatoria = hoje - datetime.timedelta(days=dias_aleatorios)
    return data_aleatoria.strftime("%Y-%m-%d %H:%M:%S")

# Cadastra os produtos
produtos_inseridos = 0
for produto in produtos:
    try:
        # Verifica se o produto já existe
        cursor.execute("SELECT id FROM produtos WHERE codigo = ?", (produto["codigo"],))
        if cursor.fetchone() is None:
            # Adiciona data de cadastro aleatória
            produto["data_cadastro"] = gerar_data_aleatoria()
            
            # Insere o produto - adaptado para a estrutura atual da tabela
            cursor.execute('''
                INSERT INTO produtos (
                    codigo, nome, descricao, preco, estoque, 
                    categoria, fornecedor, data_cadastro
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                produto["codigo"], produto["nome"], produto["descricao"],
                produto["preco"], produto["estoque"], 
                produto["categoria"], produto["fornecedor"],
                produto["data_cadastro"]
            ))
            produtos_inseridos += 1
            print(f"Produto {produto['codigo']} - {produto['nome']} inserido com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao inserir produto {produto['codigo']}: {e}")

# Commit e fecha a conexão
conn.commit()
conn.close()

print(f"Cadastro concluído! {produtos_inseridos} produtos foram inseridos no banco de dados.")