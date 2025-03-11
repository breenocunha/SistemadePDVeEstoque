import os
import sqlite3

def setup_database():
    """Inicializa o banco de dados SQLite."""
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database.db')
    
    # Cria a conexão com o banco de dados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Cria as tabelas se não existirem
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT NOT NULL,
        nome TEXT NOT NULL,
        descricao TEXT,
        categoria_id INTEGER,
        fornecedor_id INTEGER,
        preco_custo REAL NOT NULL DEFAULT 0,
        preco_venda REAL NOT NULL DEFAULT 0,
        estoque_atual INTEGER NOT NULL DEFAULT 0,
        estoque_minimo INTEGER NOT NULL DEFAULT 0,
        unidade TEXT,
        localizacao TEXT,
        codigo_barras TEXT,
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id),
        FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id)
    )
    ''')
    
    # Tabela de categorias
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT,
        cor TEXT DEFAULT '#3498db'
    )
    ''')
    
    # Tabela de fornecedores
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fornecedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cnpj TEXT,
        endereco TEXT,
        telefone TEXT,
        email TEXT,
        contato TEXT,
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabela de movimentações de estoque
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movimentacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        tipo TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        motivo TEXT,
        usuario_id INTEGER,
        data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (produto_id) REFERENCES produtos(id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    ''')
    
    # Tabela de vendas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        usuario_id INTEGER,
        data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        valor_total REAL NOT NULL DEFAULT 0,
        desconto REAL DEFAULT 0,
        forma_pagamento TEXT,
        status TEXT DEFAULT 'finalizada',
        FOREIGN KEY (cliente_id) REFERENCES clientes(id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    ''')
    
    # Tabela de itens de venda
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS itens_venda (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venda_id INTEGER NOT NULL,
        produto_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        preco_unitario REAL NOT NULL,
        desconto REAL DEFAULT 0,
        FOREIGN KEY (venda_id) REFERENCES vendas(id),
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    ''')
    
    # Tabela de clientes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf_cnpj TEXT,
        endereco TEXT,
        telefone TEXT,
        email TEXT,
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabela de usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        usuario TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        nivel_acesso TEXT DEFAULT 'vendedor',
        ativo INTEGER DEFAULT 1,
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Inserir usuário admin padrão se não existir
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE usuario = 'admin'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
        INSERT INTO usuarios (nome, usuario, senha, nivel_acesso)
        VALUES ('Administrador', 'admin', 'admin123', 'admin')
        ''')
    
    # Inserir algumas categorias padrão
    categorias_padrao = [
        ('Peças de Motor', 'Componentes para motor', '#e74c3c'),
        ('Suspensão', 'Peças de suspensão e amortecedores', '#2ecc71'),
        ('Freios', 'Sistema de freios', '#f39c12'),
        ('Elétrica', 'Componentes elétricos', '#9b59b6'),
        ('Acessórios', 'Acessórios diversos', '#3498db')
    ]
    
    for cat in categorias_padrao:
        cursor.execute("SELECT COUNT(*) FROM categorias WHERE nome = ?", (cat[0],))
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
            INSERT INTO categorias (nome, descricao, cor)
            VALUES (?, ?, ?)
            ''', cat)
    
    conn.commit()
    conn.close()
    
    print("Banco de dados inicializado com sucesso.")
    return True

def get_db_connection():
    """Retorna uma conexão com o banco de dados."""
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Para acessar as colunas pelo nome
    return conn