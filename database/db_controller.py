import sqlite3
import os

class DatabaseController:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.initialize_db()
    
    def connect(self):
        """Estabelece conexão com o banco de dados."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {str(e)}")
            return False
    
    def disconnect(self):
        """Fecha a conexão com o banco de dados."""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
    
    def initialize_db(self):
        """Inicializa o banco de dados se não existir."""
        # Verifica se o diretório existe
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        # Cria as tabelas se não existirem
        if self.connect():
            self.create_tables()
            self.disconnect()
    
    def initialize_sample_data(self):
        """Inicializa dados de exemplo se as tabelas estiverem vazias."""
        try:
            # Check if produtos table is empty
            count = self.fetch_one("SELECT COUNT(*) as count FROM produtos")
            if count and count['count'] == 0:
                # Insert sample products
                sample_products = [
                    ('P001', 'Camiseta Básica', 'Camiseta de algodão', 29.90, 15.00, 50, 10, 'Vestuário', 'Fornecedor A', '2023-01-01'),
                    ('P002', 'Calça Jeans', 'Calça jeans tradicional', 89.90, 45.00, 30, 5, 'Vestuário', 'Fornecedor B', '2023-01-01'),
                    ('P003', 'Tênis Casual', 'Tênis para uso diário', 129.90, 70.00, 20, 3, 'Calçados', 'Fornecedor C', '2023-01-01'),
                    ('P004', 'Mochila', 'Mochila para notebook', 59.90, 30.00, 15, 2, 'Acessórios', 'Fornecedor D', '2023-01-01')
                ]
                
                for product in sample_products:
                    self.execute_query("""
                        INSERT INTO produtos (codigo, nome, descricao, preco, custo, estoque, estoque_minimo, categoria, fornecedor, data_cadastro)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, product)
                
                print("Dados de exemplo de produtos inseridos com sucesso!")
            
            # Check if clientes table is empty
            count = self.fetch_one("SELECT COUNT(*) as count FROM clientes")
            if count and count['count'] == 0:
                # Insert sample clients
                sample_clients = [
                    ('João Silva', '123.456.789-00', '(11) 98765-4321', 'joao@email.com', 'Rua A, 123', '2023-01-01'),
                    ('Maria Oliveira', '987.654.321-00', '(11) 91234-5678', 'maria@email.com', 'Rua B, 456', '2023-01-01'),
                    ('Pedro Santos', '456.789.123-00', '(11) 92345-6789', 'pedro@email.com', 'Rua C, 789', '2023-01-01')
                ]
                
                for client in sample_clients:
                    self.execute_query("""
                        INSERT INTO clientes (nome, cpf, telefone, email, endereco, data_cadastro)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, client)
                
                print("Dados de exemplo de clientes inseridos com sucesso!")
                
        except Exception as e:
            print(f"Erro ao inicializar dados de exemplo: {str(e)}")
    
    def create_tables(self):
        """Cria as tabelas do banco de dados."""
        try:
            # Tabela de Clientes
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cpf TEXT,
                    telefone TEXT,
                    email TEXT,
                    endereco TEXT,
                    data_cadastro TEXT
                )
            ''')
            
            # Tabela de Produtos
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT NOT NULL UNIQUE,
                    nome TEXT NOT NULL,
                    descricao TEXT,
                    preco REAL NOT NULL,
                    custo REAL,
                    estoque REAL NOT NULL DEFAULT 0,
                    estoque_minimo REAL DEFAULT 0,
                    categoria TEXT,
                    fornecedor TEXT,
                    data_cadastro TEXT
                )
            ''')
            
            # Tabela de Vendas
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS vendas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER,
                    data TEXT NOT NULL,
                    total REAL NOT NULL,
                    forma_pagamento TEXT,
                    status TEXT NOT NULL,
                    observacoes TEXT,
                    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
                )
            ''')
            
            # Tabela de Itens da Venda
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS itens_venda (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    venda_id INTEGER NOT NULL,
                    produto_id INTEGER NOT NULL,
                    quantidade REAL NOT NULL,
                    preco_unitario REAL NOT NULL,
                    subtotal REAL NOT NULL,
                    FOREIGN KEY (venda_id) REFERENCES vendas (id),
                    FOREIGN KEY (produto_id) REFERENCES produtos (id)
                )
            ''')
            
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao criar tabelas: {str(e)}")
            return False
    
    def execute_query(self, query, params=()):
        """Executa uma query SQL."""
        try:
            if not self.connection:
                self.connect()
            
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao executar query: {str(e)}")
            return False
    
    def execute_insert(self, query, params=()):
        """Executa uma query de inserção e retorna o ID gerado."""
        try:
            if not self.connection:
                self.connect()
            
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao executar inserção: {str(e)}")
            return None
    
    def fetch_one(self, query, params=()):
        """Executa uma query e retorna um único resultado."""
        try:
            if not self.connection:
                self.connect()
            
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Erro ao buscar registro: {str(e)}")
            return None
    
    def fetch_all(self, query, params=()):
        """Executa uma query e retorna todos os resultados."""
        try:
            if not self.connection:
                self.connect()
            
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao buscar registros: {str(e)}")
            return []
    
    def begin_transaction(self):
        """Inicia uma transação."""
        if not self.connection:
            self.connect()
    
    def commit_transaction(self):
        """Confirma uma transação."""
        if self.connection:
            self.connection.commit()
    
    def rollback_transaction(self):
        """Reverte uma transação."""
        if self.connection:
            self.connection.rollback()