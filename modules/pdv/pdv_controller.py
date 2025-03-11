import sqlite3
import datetime

class PDVController:
    def __init__(self, db_path):
        self.db_path = db_path
    
    def buscar_produto_para_venda(self, termo):
        """Busca um produto pelo código ou nome para adicionar à venda."""
        try:
            # Primeiro tenta buscar pelo código exato
            query = "SELECT * FROM produtos WHERE codigo = ?"
            produto = self.db_controller.fetch_one(query, (termo,))
            
            # Se não encontrar pelo código, busca pelo nome (parcial)
            if not produto:
                query = "SELECT * FROM produtos WHERE nome LIKE ?"
                produto = self.db_controller.fetch_one(query, (f"%{termo}%",))
            
            return produto
        except Exception as e:
            print(f"Erro ao buscar produto para venda: {str(e)}")
            return None
    
    def buscar_cliente(self, termo):
        """Busca um cliente pelo nome, CPF ou telefone."""
        try:
            query = """
                SELECT * FROM clientes 
                WHERE nome LIKE ? OR cpf LIKE ? OR telefone LIKE ?
            """
            params = (f"%{termo}%", f"%{termo}%", f"%{termo}%")
            return self.db_controller.fetch_all(query, params)
        except Exception as e:
            print(f"Erro ao buscar cliente: {str(e)}")
            return []
    
    def registrar_venda(self, venda_data, itens):
        """Registra uma nova venda no sistema."""
        try:
            # Inicia uma transação
            self.db_controller.begin_transaction()
            
            # Insere a venda
            query_venda = """
                INSERT INTO vendas (
                    cliente_id, data, total, forma_pagamento, 
                    status, observacoes
                ) VALUES (?, ?, ?, ?, ?, ?)
            """
            params_venda = (
                venda_data.get("cliente_id"),
                venda_data.get("data", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                venda_data.get("total", 0),
                venda_data.get("forma_pagamento", "Dinheiro"),
                venda_data.get("status", "Concluída"),
                venda_data.get("observacoes", "")
            )
            
            venda_id = self.db_controller.execute_insert(query_venda, params_venda)
            
            # Insere os itens da venda
            for item in itens:
                query_item = """
                    INSERT INTO itens_venda (
                        venda_id, produto_id, quantidade, 
                        preco_unitario, subtotal
                    ) VALUES (?, ?, ?, ?, ?)
                """
                params_item = (
                    venda_id,
                    item["id"],
                    item["quantidade"],
                    item["preco"],
                    item["subtotal"]
                )
                
                self.db_controller.execute_query(query_item, params_item)
                
                # Atualiza o estoque do produto
                query_estoque = """
                    UPDATE produtos 
                    SET estoque = estoque - ? 
                    WHERE id = ?
                """
                params_estoque = (item["quantidade"], item["id"])
                self.db_controller.execute_query(query_estoque, params_estoque)
            
            # Finaliza a transação
            self.db_controller.commit_transaction()
            
            return {"sucesso": True, "venda_id": venda_id}
        except Exception as e:
            # Reverte a transação em caso de erro
            self.db_controller.rollback_transaction()
            print(f"Erro ao registrar venda: {str(e)}")
            return {"sucesso": False, "mensagem": str(e)}
    
    def listar_vendas(self, data_inicio=None, data_fim=None, cliente_id=None):
        """Lista as vendas com filtros opcionais."""
        try:
            query = """
                SELECT v.*, c.nome as cliente_nome
                FROM vendas v
                LEFT JOIN clientes c ON v.cliente_id = c.id
                WHERE 1=1
            """
            params = []
            
            if data_inicio:
                query += " AND v.data >= ?"
                params.append(data_inicio)
            
            if data_fim:
                query += " AND v.data <= ?"
                params.append(data_fim)
            
            if cliente_id:
                query += " AND v.cliente_id = ?"
                params.append(cliente_id)
            
            query += " ORDER BY v.data DESC"
            
            return self.db_controller.fetch_all(query, tuple(params))
        except Exception as e:
            print(f"Erro ao listar vendas: {str(e)}")
            return []
    
    def obter_detalhes_venda(self, venda_id):
        """Obtém os detalhes de uma venda específica."""
        try:
            # Obtém os dados da venda
            query_venda = """
                SELECT v.*, c.nome as cliente_nome, c.cpf as cliente_cpf
                FROM vendas v
                LEFT JOIN clientes c ON v.cliente_id = c.id
                WHERE v.id = ?
            """
            venda = self.db_controller.fetch_one(query_venda, (venda_id,))
            
            if not venda:
                return None
            
            # Obtém os itens da venda
            query_itens = """
                SELECT iv.*, p.codigo as produto_codigo, p.nome as produto_nome
                FROM itens_venda iv
                JOIN produtos p ON iv.produto_id = p.id
                WHERE iv.venda_id = ?
            """
            itens = self.db_controller.fetch_all(query_itens, (venda_id,))
            
            # Monta o resultado
            resultado = {
                "venda": venda,
                "itens": itens
            }
            
            return resultado
        except Exception as e:
            print(f"Erro ao obter detalhes da venda: {str(e)}")
            return None
    
    def cancelar_venda(self, venda_id):
        """Cancela uma venda e estorna o estoque."""
        try:
            # Inicia uma transação
            self.db_controller.begin_transaction()
            
            # Verifica se a venda existe e não está cancelada
            query_check = "SELECT status FROM vendas WHERE id = ?"
            status = self.db_controller.fetch_one(query_check, (venda_id,))
            
            if not status:
                return {"sucesso": False, "mensagem": "Venda não encontrada."}
            
            if status["status"] == "Cancelada":
                return {"sucesso": False, "mensagem": "Venda já está cancelada."}
            
            # Obtém os itens da venda para estornar o estoque
            query_itens = """
                SELECT produto_id, quantidade
                FROM itens_venda
                WHERE venda_id = ?
            """
            itens = self.db_controller.fetch_all(query_itens, (venda_id,))
            
            # Estorna o estoque de cada item
            for item in itens:
                query_estoque = """
                    UPDATE produtos 
                    SET estoque = estoque + ? 
                    WHERE id = ?
                """
                params_estoque = (item["quantidade"], item["produto_id"])
                self.db_controller.execute_query(query_estoque, params_estoque)
            
            # Atualiza o status da venda para cancelada
            query_update = """
                UPDATE vendas 
                SET status = 'Cancelada', 
                    observacoes = observacoes || ' | Cancelada em: ' || ?
                WHERE id = ?
            """
            data_cancelamento = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            params_update = (data_cancelamento, venda_id)
            self.db_controller.execute_query(query_update, params_update)
            
            # Finaliza a transação
            self.db_controller.commit_transaction()
            
            return {"sucesso": True, "mensagem": "Venda cancelada com sucesso!"}
        except Exception as e:
            # Reverte a transação em caso de erro
            self.db_controller.rollback_transaction()
            print(f"Erro ao cancelar venda: {str(e)}")
            return {"sucesso": False, "mensagem": str(e)}
    
    def obter_produto(self, produto_id):
        """Obtém um produto pelo ID."""
        try:
            query = "SELECT * FROM produtos WHERE id = ?"
            return self.db_controller.fetch_one(query, (produto_id,))
        except Exception as e:
            print(f"Erro ao obter produto: {str(e)}")
            return None
    
    def buscar_produtos(self, termo):
        """Busca produtos pelo código ou nome."""
        try:
            query = """
                SELECT * FROM produtos 
                WHERE codigo LIKE ? OR nome LIKE ?
                ORDER BY nome
            """
            params = (f"%{termo}%", f"%{termo}%")
            return self.db_controller.fetch_all(query, params)
        except Exception as e:
            print(f"Erro ao buscar produtos: {str(e)}")
            return []
    
    def verificar_estoque(self, produto_id, quantidade):
        """Verifica se há estoque suficiente para um produto."""
        try:
            query = "SELECT estoque FROM produtos WHERE id = ?"
            resultado = self.db_controller.fetch_one(query, (produto_id,))
            
            if not resultado:
                return False
            
            return resultado["estoque"] >= quantidade
        except Exception as e:
            print(f"Erro ao verificar estoque: {str(e)}")
            return False
    
    def obter_cliente(self, cliente_id):
        """Obtém um cliente pelo ID."""
        try:
            query = "SELECT * FROM clientes WHERE id = ?"
            return self.db_controller.fetch_one(query, (cliente_id,))
        except Exception as e:
            print(f"Erro ao obter cliente: {str(e)}")
            return None
    
    def listar_clientes(self):
        """Lista todos os clientes."""
        try:
            query = "SELECT * FROM clientes ORDER BY nome"
            return self.db_controller.fetch_all(query)
        except Exception as e:
            print(f"Erro ao listar clientes: {str(e)}")
            return []
    
    def gerar_relatorio_vendas(self, data_inicio, data_fim):
        """Gera um relatório de vendas por período."""
        try:
            query = """
                SELECT 
                    v.id, 
                    v.data, 
                    c.nome as cliente_nome,
                    v.total,
                    v.forma_pagamento,
                    v.status
                FROM vendas v
                LEFT JOIN clientes c ON v.cliente_id = c.id
                WHERE v.data BETWEEN ? AND ?
                ORDER BY v.data DESC
            """
            vendas = self.db_controller.fetch_all(query, (data_inicio, data_fim))
            
            # Calcula totais
            total_vendas = len(vendas)
            valor_total = sum(venda["total"] for venda in vendas)
            vendas_por_status = {}
            vendas_por_pagamento = {}
            
            for venda in vendas:
                status = venda["status"]
                pagamento = venda["forma_pagamento"]
                
                if status not in vendas_por_status:
                    vendas_por_status[status] = 0
                vendas_por_status[status] += 1
                
                if pagamento not in vendas_por_pagamento:
                    vendas_por_pagamento[pagamento] = 0
                vendas_por_pagamento[pagamento] += 1
            
            return {
                "vendas": vendas,
                "total_vendas": total_vendas,
                "valor_total": valor_total,
                "por_status": vendas_por_status,
                "por_pagamento": vendas_por_pagamento
            }
        except Exception as e:
            print(f"Erro ao gerar relatório de vendas: {str(e)}")
            return {
                "vendas": [],
                "total_vendas": 0,
                "valor_total": 0,
                "por_status": {},
                "por_pagamento": {}
            }
    
    def gerar_relatorio_produtos_vendidos(self, data_inicio, data_fim):
        """Gera um relatório dos produtos mais vendidos por período."""
        try:
            query = """
                SELECT 
                    p.id,
                    p.codigo,
                    p.nome,
                    SUM(iv.quantidade) as quantidade_total,
                    SUM(iv.subtotal) as valor_total
                FROM itens_venda iv
                JOIN produtos p ON iv.produto_id = p.id
                JOIN vendas v ON iv.venda_id = v.id
                WHERE v.data BETWEEN ? AND ? AND v.status != 'Cancelada'
                GROUP BY p.id, p.codigo, p.nome
                ORDER BY quantidade_total DESC
            """
            produtos = self.db_controller.fetch_all(query, (data_inicio, data_fim))
            
            return produtos
        except Exception as e:
            print(f"Erro ao gerar relatório de produtos vendidos: {str(e)}")
            return []
    
    def salvar_venda(self, venda_data):
        """Salva uma venda completa."""
        try:
            # Inicia uma transação
            self.db_controller.begin_transaction()
            
            # Insere a venda
            query_venda = """
                INSERT INTO vendas (
                    cliente_id, data, total, forma_pagamento, 
                    status, observacoes
                ) VALUES (?, ?, ?, ?, ?, ?)
            """
            params_venda = (
                venda_data.get("cliente_id"),
                venda_data.get("data", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                venda_data.get("total", 0),
                venda_data.get("forma_pagamento", "Dinheiro"),
                venda_data.get("status", "Concluída"),
                venda_data.get("observacoes", "")
            )
            
            venda_id = self.db_controller.execute_insert(query_venda, params_venda)
            
            # Insere os itens da venda
            for item in venda_data.get("itens", []):
                query_item = """
                    INSERT INTO itens_venda (
                        venda_id, produto_id, quantidade, 
                        preco_unitario, subtotal
                    ) VALUES (?, ?, ?, ?, ?)
                """
                params_item = (
                    venda_id,
                    item["produto_id"],
                    item["quantidade"],
                    item["preco"],
                    item["subtotal"]
                )
                
                self.db_controller.execute_query(query_item, params_item)
                
                # Atualiza o estoque do produto
                query_estoque = """
                    UPDATE produtos 
                    SET estoque = estoque - ? 
                    WHERE id = ?
                """
                params_estoque = (item["quantidade"], item["produto_id"])
                self.db_controller.execute_query(query_estoque, params_estoque)
            
            # Finaliza a transação
            self.db_controller.commit_transaction()
            
            return {"sucesso": True, "venda_id": venda_id}
        except Exception as e:
            # Reverte a transação em caso de erro
            self.db_controller.rollback_transaction()
            print(f"Erro ao salvar venda: {str(e)}")
            return {"sucesso": False, "mensagem": str(e)}