import os
import sqlite3
import shutil
import random
from datetime import datetime

# Configuração do banco de dados
DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'pdv.db')  # Alterado para corresponder ao caminho usado no main.py
IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'images', 'produtos')

# Garantir que o diretório de imagens existe
os.makedirs(IMAGES_DIR, exist_ok=True)

# Lista de produtos para cadastro
produtos = [
    {"nome": "Smartphone Galaxy S23", "descricao": "Smartphone Samsung Galaxy S23 128GB", "preco": 3999.90, "categoria": "Eletrônicos", "imagem": "smartphone.jpg"},
    {"nome": "Notebook Dell Inspiron", "descricao": "Notebook Dell Inspiron 15 8GB RAM 256GB SSD", "preco": 4299.90, "categoria": "Informática", "imagem": "notebook.jpg"},
    {"nome": "Smart TV LG 50\"", "descricao": "Smart TV LG 50 polegadas 4K", "preco": 2799.90, "categoria": "Eletrônicos", "imagem": "tv.jpg"},
    {"nome": "Fone de Ouvido JBL", "descricao": "Fone de Ouvido JBL Bluetooth", "preco": 299.90, "categoria": "Acessórios", "imagem": "fone.jpg"},
    {"nome": "Mouse Gamer Logitech", "descricao": "Mouse Gamer Logitech G502", "preco": 349.90, "categoria": "Informática", "imagem": "mouse.jpg"},
    {"nome": "Teclado Mecânico", "descricao": "Teclado Mecânico RGB", "preco": 399.90, "categoria": "Informática", "imagem": "teclado.jpg"},
    {"nome": "Cafeteira Elétrica", "descricao": "Cafeteira Elétrica 15 Xícaras", "preco": 189.90, "categoria": "Eletrodomésticos", "imagem": "cafeteira.jpg"},
    {"nome": "Liquidificador Philips", "descricao": "Liquidificador Philips 1000W", "preco": 159.90, "categoria": "Eletrodomésticos", "imagem": "liquidificador.jpg"},
    {"nome": "Micro-ondas Consul", "descricao": "Micro-ondas Consul 30L", "preco": 699.90, "categoria": "Eletrodomésticos", "imagem": "microondas.jpg"},
    {"nome": "Fritadeira Air Fryer", "descricao": "Fritadeira Air Fryer 4L", "preco": 399.90, "categoria": "Eletrodomésticos", "imagem": "airfryer.jpg"},
    {"nome": "Caixa de Som Bluetooth", "descricao": "Caixa de Som Bluetooth JBL", "preco": 499.90, "categoria": "Eletrônicos", "imagem": "caixasom.jpg"},
    {"nome": "Tablet Samsung", "descricao": "Tablet Samsung Galaxy Tab A8", "preco": 1299.90, "categoria": "Eletrônicos", "imagem": "tablet.jpg"},
    {"nome": "Impressora HP", "descricao": "Impressora HP Multifuncional", "preco": 899.90, "categoria": "Informática", "imagem": "impressora.jpg"},
    {"nome": "Ventilador de Mesa", "descricao": "Ventilador de Mesa 40cm", "preco": 149.90, "categoria": "Eletrodomésticos", "imagem": "ventilador.jpg"},
    {"nome": "Carregador Portátil", "descricao": "Carregador Portátil 10000mAh", "preco": 129.90, "categoria": "Acessórios", "imagem": "powerbank.jpg"},
    {"nome": "Câmera de Segurança", "descricao": "Câmera de Segurança Wi-Fi", "preco": 299.90, "categoria": "Eletrônicos", "imagem": "camera.jpg"},
    {"nome": "Relógio Smartwatch", "descricao": "Relógio Smartwatch Fitness", "preco": 399.90, "categoria": "Acessórios", "imagem": "smartwatch.jpg"},
    {"nome": "Cadeira Gamer", "descricao": "Cadeira Gamer Ergonômica", "preco": 899.90, "categoria": "Móveis", "imagem": "cadeira.jpg"},
    {"nome": "Mochila para Notebook", "descricao": "Mochila para Notebook 15.6\"", "preco": 149.90, "categoria": "Acessórios", "imagem": "mochila.jpg"},
    {"nome": "Headset Gamer", "descricao": "Headset Gamer com Microfone", "preco": 249.90, "categoria": "Informática", "imagem": "headset.jpg"},
]

# Função para baixar imagens de exemplo (simulada)
def baixar_imagens_exemplo():
    """
    Esta função simula o download de imagens.
    Em um ambiente real, você baixaria imagens da internet ou usaria imagens locais.
    Aqui, vamos apenas criar arquivos de imagem vazios para demonstração.
    """
    print("Simulando download de imagens de produtos...")
    
    # Cria arquivos de imagem vazios para cada produto
    for produto in produtos:
        imagem_path = os.path.join(IMAGES_DIR, produto["imagem"])
        
        # Se o arquivo não existir, cria um arquivo vazio
        if not os.path.exists(imagem_path):
            with open(imagem_path, 'w') as f:
                f.write("Placeholder para imagem")
            print(f"Criado placeholder para: {produto['imagem']}")

# Função para cadastrar produtos no banco de dados
def cadastrar_produtos():
    """Cadastra os produtos no banco de dados."""
    try:
        # Conecta ao banco de dados
        print(f"Conectando ao banco de dados: {DB_PATH}")
        if not os.path.exists(DB_PATH):
            print(f"ERRO: O arquivo do banco de dados não existe: {DB_PATH}")
            os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
            print(f"Diretório criado: {os.path.dirname(DB_PATH)}")
            
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Para acessar colunas pelo nome
        cursor = conn.cursor()
        
        # Verifica se a tabela de produtos existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='produtos'")
        if not cursor.fetchone():
            print("Tabela de produtos não encontrada. Criando tabela...")
            # Cria a tabela de produtos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT,
                    codigo_barras TEXT,
                    nome TEXT NOT NULL,
                    descricao TEXT,
                    preco_venda REAL,
                    categoria TEXT,
                    imagem TEXT,
                    estoque_atual INTEGER DEFAULT 0,
                    estoque_minimo INTEGER DEFAULT 5,
                    data_cadastro TEXT
                )
            """)
            conn.commit()
            print("Tabela de produtos criada com sucesso!")
        
        # Obtém informações sobre as colunas da tabela produtos
        cursor.execute("PRAGMA table_info(produtos)")
        colunas = {info['name'] for info in cursor.fetchall()}
        print(f"Colunas disponíveis na tabela: {', '.join(colunas)}")
        
        # Cadastra cada produto
        for produto in produtos:
            # Gera um código de barras aleatório
            codigo_barras = ''.join([str(random.randint(0, 9)) for _ in range(13)])
            
            # Verifica se o produto já existe pelo nome
            cursor.execute("SELECT id FROM produtos WHERE nome = ?", (produto["nome"],))
            if cursor.fetchone():
                print(f"Produto '{produto['nome']}' já existe. Pulando...")
                continue
            
            # Prepara os dados do produto de acordo com as colunas disponíveis
            dados_produto = {}
            
            # Mapeamento de campos
            if 'codigo_barras' in colunas:
                dados_produto['codigo_barras'] = codigo_barras
            elif 'codigo' in colunas:
                dados_produto['codigo'] = codigo_barras
            
            # Campos comuns
            dados_produto['nome'] = produto["nome"]
            dados_produto['descricao'] = produto["descricao"]
            
            # Verifica o nome correto da coluna de preço
            if 'preco_venda' in colunas:
                dados_produto['preco_venda'] = produto["preco"]
            elif 'preco' in colunas:
                dados_produto['preco'] = produto["preco"]
            
            # Outros campos
            if 'categoria' in colunas:
                dados_produto['categoria'] = produto["categoria"]
            
            if 'imagem' in colunas:
                dados_produto['imagem'] = produto["imagem"]
            
            if 'estoque_atual' in colunas:
                dados_produto['estoque_atual'] = random.randint(10, 50)
            elif 'estoque' in colunas:
                dados_produto['estoque'] = random.randint(10, 50)
            
            if 'estoque_minimo' in colunas:
                dados_produto['estoque_minimo'] = 5
            
            if 'data_cadastro' in colunas:
                dados_produto['data_cadastro'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Constrói a query de inserção dinamicamente
            campos = ', '.join(dados_produto.keys())
            placeholders = ', '.join(['?' for _ in dados_produto])
            
            query = f"INSERT INTO produtos ({campos}) VALUES ({placeholders})"
            
            cursor.execute(query, list(dados_produto.values()))
            
            print(f"Produto '{produto['nome']}' cadastrado com sucesso!")
        
        # Commit das alterações
        conn.commit()
        
        # Verifica quantos produtos foram cadastrados
        cursor.execute("SELECT COUNT(*) FROM produtos")
        count = cursor.fetchone()[0]
        print(f"Total de produtos no banco de dados: {count}")
        
        print("Todos os produtos foram cadastrados com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao cadastrar produtos: {str(e)}")
        return False
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("Iniciando cadastro de produtos de demonstração...")
    baixar_imagens_exemplo()
    if cadastrar_produtos():
        print("Processo concluído com sucesso!")
    else:
        print("Ocorreram erros durante o processo.")