import sqlite3
import os

class DatabaseController:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_tables()  # Add this line to create tables on initialization
        
    def connect(self):
        """Conecta ao banco de dados."""
        try:
            # Verifica se o diretório existe, se não, cria
            db_dir = os.path.dirname(self.db_path)
            if not os.path.exists(db_dir):
                os.makedirs(db_dir)
                
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            print(f"Conectado ao banco de dados: {self.db_path}")
            return True
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {str(e)}")
            return False
    
    def create_tables(self):
        """Cria as tabelas necessárias no banco de dados."""
        try:
            # Tabela de clientes
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cpf TEXT UNIQUE,
                    email TEXT,
                    telefone TEXT,
                    endereco TEXT,
                    data_cadastro TEXT
                )
            ''')
            
            # Tabela de produtos
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT UNIQUE,
                    nome TEXT NOT NULL,
                    categoria TEXT,
                    preco REAL NOT NULL,
                    estoque INTEGER DEFAULT 0,
                    minimo INTEGER DEFAULT 0,
                    fornecedor TEXT,
                    descricao TEXT,
                    imagem TEXT,
                    data_cadastro TEXT
                )
            ''')
            
            # Tabela de vendas
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS vendas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT NOT NULL,
                    cliente_id INTEGER,
                    total REAL NOT NULL,
                    forma_pagamento TEXT,
                    status TEXT DEFAULT 'Concluída',
                    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
                )
            ''')
            
            # Tabela de itens de venda
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS itens_venda (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    venda_id INTEGER NOT NULL,
                    produto_id INTEGER NOT NULL,
                    quantidade INTEGER NOT NULL,
                    preco_unitario REAL NOT NULL,
                    subtotal REAL NOT NULL,
                    FOREIGN KEY (venda_id) REFERENCES vendas (id),
                    FOREIGN KEY (produto_id) REFERENCES produtos (id)
                )
            ''')
            
            # Tabela de log de operações
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS log_operacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT NOT NULL,
                    descricao TEXT,
                    data TEXT NOT NULL,
                    usuario_id INTEGER
                )
            ''')
            
            self.connection.commit()
            print("Tabelas criadas com sucesso!")
            return True
        except sqlite3.Error as e:
            print(f"Erro ao criar tabelas: {str(e)}")
            return False
    
    def execute_query(self, query, params=None, commit=True):
        """Executa uma query SQL."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            if commit:
                self.connection.commit()
            
            # Se for um SELECT, retorna os resultados
            if query.strip().upper().startswith("SELECT") or query.strip().upper().startswith("PRAGMA"):
                return self.cursor.fetchall()
            
            return True
        except sqlite3.Error as e:
            print(f"Erro ao executar query: {str(e)}")
            print(f"Query:\n{query}")
            if params:
                print(f"Params: {params}")
            return False
    
    def begin_transaction(self):
        """Inicia uma transação."""
        try:
            self.connection.execute("BEGIN TRANSACTION")
            return True
        except sqlite3.Error as e:
            print(f"Erro ao iniciar transação: {str(e)}")
            return False
    
    def commit_transaction(self):
        """Confirma uma transação."""
        try:
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao confirmar transação: {str(e)}")
            return False
    
    def rollback_transaction(self):
        """Desfaz uma transação."""
        try:
            self.connection.rollback()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao desfazer transação: {str(e)}")
            return False
    
    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self.connection:
            self.connection.close()
            print("Conexão com o banco de dados fechada.")
    
    def get_table_info(self, table_name):
        """
        Get information about a table's structure.
        
        Args:
            table_name (str): The name of the table.
            
        Returns:
            list: List of dictionaries containing column information.
        """
        try:
            query = f"PRAGMA table_info({table_name})"
            result = self.execute_query(query)
            return result  # This should return a list of dictionaries
        except Exception as e:
            print(f"Error getting table info: {str(e)}")
            return []  # Return an empty list instead of a boolean
    
    def get_table_count(self, table_name):
        """
        Get the number of rows in a table.
        
        Args:
            table_name (str): The name of the table.
            
        Returns:
            int: Number of rows in the table.
        """
        try:
            query = f"SELECT COUNT(*) as count FROM {table_name}"
            result = self.execute_query(query)
            if result and len(result) > 0:
                return result[0]['count']
            return 0
        except Exception as e:
            print(f"Error getting table count: {str(e)}")
            return 0

    def add_cliente_id_to_vendas(self):
        """Add cliente_id column to vendas table if it doesn't exist."""
        try:
            # Check if the column exists
            table_info = self.get_table_info('vendas')
            
            # Make sure table_info is a list
            if not isinstance(table_info, list):
                print(f"Unexpected table_info type: {type(table_info)}")
                return False
                
            # Extract column names from table_info
            column_names = [col['name'] for col in table_info] if table_info else []
            
            if 'cliente_id' not in column_names:
                print("Adding cliente_id column to vendas table...")
                query = "ALTER TABLE vendas ADD COLUMN cliente_id INTEGER REFERENCES clientes(id)"
                self.execute_query(query)
                print("cliente_id column added successfully.")
            else:
                print("cliente_id column already exists in vendas table.")
                
            return True
        except Exception as e:
            print(f"Error adding cliente_id column: {str(e)}")
            return False