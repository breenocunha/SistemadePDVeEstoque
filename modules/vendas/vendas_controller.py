import os
import json
import datetime

class VendasController:
    def __init__(self, db_controller, produtos_controller=None):
        self.db_controller = db_controller
        self.produtos_controller = produtos_controller
        self.vendas_file = os.path.join(os.path.dirname(__file__), "data", "vendas.json")
        self.ensure_data_dir()
    
    def ensure_data_dir(self):
        """Garante que o diretório de dados existe."""
        data_dir = os.path.dirname(self.vendas_file)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
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
    
    def _venda_no_periodo(self, venda, inicio, fim):
        """Verifica se uma venda está dentro do período especificado."""
        try:
            data_venda = datetime.datetime.strptime(venda["data"], "%Y-%m-%d %H:%M:%S")
            return inicio <= data_venda <= fim
        except (ValueError, KeyError):
            return False
    
    def obter_venda(self, venda_id):
        """Obtém uma venda pelo ID."""
        vendas = self._carregar_vendas()
        
        for venda in vendas:
            if str(venda["id"]) == str(venda_id):
                return venda
        
        return None
    
    def salvar_venda(self, venda_data):
        """Salva uma nova venda."""
        vendas = self._carregar_vendas()
        
        # Gera um novo ID
        novo_id = 1
        if vendas:
            novo_id = max(v["id"] for v in vendas) + 1
        
        # Adiciona o ID à venda
        venda_data["id"] = novo_id
        
        # Atualiza o estoque dos produtos
        if self.produtos_controller:
            for item in venda_data["itens"]:
                produto = self.produtos_controller.obter_produto(item["id"])
                if produto:
                    # Atualiza o estoque
                    produto["estoque"] -= item["quantidade"]
                    self.produtos_controller.atualizar_produto(produto)
        
        # Adiciona a venda à lista
        vendas.append(venda_data)
        
        # Salva a lista atualizada
        self._salvar_vendas(vendas)
        
        return {"sucesso": True, "id": novo_id}
    
    def cancelar_venda(self, venda_id):
        """Cancela uma venda pelo ID."""
        vendas = self._carregar_vendas()
        
        # Procura a venda pelo ID
        for i, venda in enumerate(vendas):
            if str(venda["id"]) == str(venda_id):
                # Marca a venda como cancelada
                vendas[i]["status"] = "Cancelada"
                vendas[i]["data_cancelamento"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Devolve os produtos ao estoque
                if self.produtos_controller:
                    for item in venda["itens"]:
                        produto = self.produtos_controller.obter_produto(item["id"])
                        if produto:
                            # Atualiza o estoque
                            produto["estoque"] += item["quantidade"]
                            self.produtos_controller.atualizar_produto(produto)
                
                # Salva a lista atualizada
                self._salvar_vendas(vendas)
                return {"sucesso": True}
        
        return {"sucesso": False, "mensagem": "Venda não encontrada."}
    
    def buscar_produtos(self, termo):
        """Busca produtos pelo termo de pesquisa."""
        if self.produtos_controller:
            return self.produtos_controller.buscar_produtos(termo)
        return []
    
    def obter_produto(self, produto_id):
        """Obtém um produto pelo ID."""
        if self.produtos_controller:
            return self.produtos_controller.obter_produto(produto_id)
        return None
    
    def _carregar_vendas(self):
        """Carrega as vendas do arquivo JSON."""
        if not os.path.exists(self.vendas_file):
            return []
        
        try:
            with open(self.vendas_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar vendas: {str(e)}")
            return []
    
    def _salvar_vendas(self, vendas):
        """Salva as vendas no arquivo JSON."""
        try:
            with open(self.vendas_file, 'w', encoding='utf-8') as f:
                json.dump(vendas, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Erro ao salvar vendas: {str(e)}")
            return False