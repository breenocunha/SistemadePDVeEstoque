import datetime
from modules.database.db_controller import DatabaseController

class HistoricoVendasController:
    def __init__(self, db_controller=None):
        self.db_controller = db_controller or DatabaseController()
    
    def listar_vendas(self, filtros=None):
        """Lista todas as vendas com base nos filtros."""
        try:
            query = """
                SELECT v.id, v.data, v.total, v.forma_pagamento, v.status,
                       COUNT(i.id) as itens_count
                FROM vendas v
                LEFT JOIN itens_venda i ON v.id = i.venda_id
                WHERE 1=1
             """
            params = []
            
            # Adiciona filtros se fornecidos
            if filtros:
                if filtros.get('data_inicio') and filtros.get('data_fim'):
                    query += "AND v.data >= ? AND v.data <= ? "
                    params.extend([filtros['data_inicio'], filtros['data_fim']])
                
                if filtros.get('status'):
                    query += "AND v.status = ? "
                    params.append(filtros['status'])
                
                if filtros.get('forma_pagamento'):
                    query += "AND v.forma_pagamento = ? "
                    params.append(filtros['forma_pagamento'])
            
            query += "GROUP BY v.id ORDER BY v.data DESC"
            
            print(f"Query:\n{query}")
            print(f"Params: {params}")
            
            result = self.db_controller.execute_query(query, params)
            
            # Converte os resultados para uma lista de dicionários
            vendas = []
            for row in result:
                vendas.append(dict(row))
            
            return vendas
        except Exception as e:
            print(f"Erro ao listar vendas: {str(e)}")
            return []
    
    def obter_detalhes_venda(self, venda_id):
        """Obtém os detalhes de uma venda específica."""
        try:
            # Obtém os dados da venda
            query_venda = """
                SELECT v.id, v.data, v.total, v.forma_pagamento, v.status
                FROM vendas v
                WHERE v.id = ?
            """
            venda = self.db_controller.execute_query(query_venda, (venda_id,))
            
            if not venda:
                return None
            
            # Obtém os itens da venda
            query_itens = """
                SELECT iv.id, iv.quantidade, iv.preco_unitario, iv.subtotal,
                       p.codigo, p.nome, p.categoria
                FROM itens_venda iv
                JOIN produtos p ON iv.produto_id = p.id
                WHERE iv.venda_id = ?
            """
            itens = self.db_controller.execute_query(query_itens, (venda_id,))
            
            # Converte para dicionários
            venda_dict = dict(venda[0])
            itens_list = [dict(item) for item in itens]
            
            # Adiciona os itens ao dicionário da venda
            venda_dict['itens'] = itens_list
            
            return venda_dict
        except Exception as e:
            print(f"Erro ao obter detalhes da venda: {str(e)}")
            return None