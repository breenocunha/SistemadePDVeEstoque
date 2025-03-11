import sys
import os
import sqlite3

# Adiciona o diretório raiz ao PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Conecta ao banco de dados
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Verifica se a tabela produtos existe
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='produtos'")
if cursor.fetchone():
    # Conta quantos produtos existem
    cursor.execute("SELECT COUNT(*) FROM produtos")
    count = cursor.fetchone()[0]
    print(f"Total de produtos no banco de dados: {count}")
    
    # Lista os produtos
    cursor.execute("SELECT id, codigo, nome, preco, estoque FROM produtos")
    produtos = cursor.fetchall()
    
    print("\nLista de produtos:")
    print("ID | Código | Nome | Preço | Estoque")
    print("-" * 60)
    for produto in produtos:
        print(f"{produto[0]} | {produto[1]} | {produto[2]} | R$ {produto[3]:.2f} | {produto[4]}")
else:
    print("A tabela 'produtos' não existe no banco de dados.")

# Fecha a conexão
conn.close()