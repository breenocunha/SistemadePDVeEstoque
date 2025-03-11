import datetime

class ClientesController:
    def __init__(self, db_controller):
        self.db_controller = db_controller
    
    def listar_clientes(self):
        """Lista todos os clientes."""
        try:
            query = """
                SELECT * FROM clientes
                ORDER BY nome
            """
            return self.db_controller.fetch_all(query)
        except Exception as e:
            print(f"Erro ao listar clientes: {str(e)}")
            return []
    
    def buscar_clientes(self, termo):
        """Busca clientes pelo termo de pesquisa."""
        try:
            query = """
                SELECT * FROM clientes
                WHERE nome LIKE ? OR cpf LIKE ? OR telefone LIKE ? OR email LIKE ?
                ORDER BY nome
            """
            params = (f"%{termo}%", f"%{termo}%", f"%{termo}%", f"%{termo}%")
            return self.db_controller.fetch_all(query, params)
        except Exception as e:
            print(f"Erro ao buscar clientes: {str(e)}")
            return []
    
    def obter_cliente(self, cliente_id):
        """Obtém um cliente pelo ID."""
        try:
            query = "SELECT * FROM clientes WHERE id = ?"
            return self.db_controller.fetch_one(query, (cliente_id,))
        except Exception as e:
            print(f"Erro ao obter cliente: {str(e)}")
            return None
    
    def inserir_cliente(self, cliente_data):
        """Insere um novo cliente no banco de dados."""
        try:
            # Verifica se o CPF já existe
            if cliente_data.get("cpf"):
                cliente_existente = self.db_controller.fetch_one(
                    "SELECT * FROM clientes WHERE cpf = ?", 
                    (cliente_data["cpf"],)
                )
                if cliente_existente:
                    return {"sucesso": False, "mensagem": f"Já existe um cliente com o CPF {cliente_data['cpf']}."}
            
            query = """
                INSERT INTO clientes (
                    nome, cpf, telefone, email, endereco, data_cadastro
                ) VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (
                cliente_data["nome"],
                cliente_data.get("cpf", ""),
                cliente_data.get("telefone", ""),
                cliente_data.get("email", ""),
                cliente_data.get("endereco", ""),
                cliente_data.get("data_cadastro", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            
            self.db_controller.execute_query(query, params)
            return {"sucesso": True}
        except Exception as e:
            print(f"Erro ao inserir cliente: {str(e)}")
            return {"sucesso": False, "mensagem": str(e)}
    
    def atualizar_cliente(self, cliente_data):
        """Atualiza um cliente existente no banco de dados."""
        try:
            # Verifica se o CPF já existe em outro cliente
            if cliente_data.get("cpf"):
                cliente_existente = self.db_controller.fetch_one(
                    "SELECT * FROM clientes WHERE cpf = ? AND id != ?", 
                    (cliente_data["cpf"], cliente_data["id"])
                )
                if cliente_existente:
                    return {"sucesso": False, "mensagem": f"Já existe outro cliente com o CPF {cliente_data['cpf']}."}
            
            query = """
                UPDATE clientes SET 
                    nome = ?, cpf = ?, telefone = ?, email = ?, endereco = ?
                WHERE id = ?
            """
            params = (
                cliente_data["nome"],
                cliente_data.get("cpf", ""),
                cliente_data.get("telefone", ""),
                cliente_data.get("email", ""),
                cliente_data.get("endereco", ""),
                cliente_data["id"]
            )
            
            self.db_controller.execute_query(query, params)
            return {"sucesso": True}
        except Exception as e:
            print(f"Erro ao atualizar cliente: {str(e)}")
            return {"sucesso": False, "mensagem": str(e)}
    
    def excluir_cliente(self, cliente_id):
        """Exclui um cliente do banco de dados."""
        try:
            # Verifica se o cliente está sendo usado em alguma venda
            query_check = """
                SELECT COUNT(*) as count FROM vendas
                WHERE cliente_id = ?
            """
            resultado = self.db_controller.fetch_one(query_check, (cliente_id,))
            
            if resultado and resultado["count"] > 0:
                return {
                    "sucesso": False, 
                    "mensagem": "Este cliente não pode ser excluído pois está associado a vendas."
                }
            
            # Exclui o cliente
            query = "DELETE FROM clientes WHERE id = ?"
            self.db_controller.execute_query(query, (cliente_id,))
            
            return {"sucesso": True}
        except Exception as e:
            print(f"Erro ao excluir cliente: {str(e)}")
            return {"sucesso": False, "mensagem": str(e)}