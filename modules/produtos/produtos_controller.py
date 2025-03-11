import datetime
import csv
import os

class ProdutosController:
    def __init__(self, db_controller):
        self.db_controller = db_controller
    
    # Find the method that's using fetch_all and replace it with execute_query
    def listar_produtos(self, filtro=None, categoria=None):
        """
        Lista todos os produtos do banco de dados.
        
        Args:
            filtro (str, optional): Filtro de busca por nome ou código.
            categoria (str, optional): Filtro por categoria.
        
        Returns:
            list: Lista de produtos.
        """
        try:
            # Check table structure and count
            table_info = self.db_controller.get_table_info('produtos')
            print(f"Estrutura da tabela produtos: {table_info}")
            
            row_count = self.db_controller.get_table_count('produtos')
            print(f"Número de produtos na tabela: {row_count}")
            
            # Debug para verificar os parâmetros
            print(f"Buscando produtos com filtro: '{filtro}' e categoria: '{categoria}'")
            
            query = "SELECT * FROM produtos"
            params = []
            
            # Adiciona filtros se fornecidos
            if filtro and categoria:
                query += " WHERE (nome LIKE ? OR codigo LIKE ? OR codigo_barras LIKE ?) AND categoria = ?"
                params = [f"%{filtro}%", f"%{filtro}%", f"%{filtro}%", categoria]
            elif filtro:
                query += " WHERE nome LIKE ? OR codigo LIKE ? OR codigo_barras LIKE ?"
                params = [f"%{filtro}%", f"%{filtro}%", f"%{filtro}%"]
            elif categoria:
                query += " WHERE categoria = ?"
                params = [categoria]
            
            query += " ORDER BY nome"
            
            # Debug para verificar a query
            print(f"Query: {query}")
            print(f"Params: {params}")
            
            # Executa a consulta
            result = self.db_controller.execute_query(query, params)
            
            # Se não houver resultados, retorna uma lista vazia
            if not result:
                print("Nenhum produto encontrado na consulta.")
                return []
            
            # Converte os resultados para uma lista de dicionários
            produtos = []
            for row in result:
                produtos.append(dict(row))
            
            print(f"Encontrados {len(produtos)} produtos na consulta.")
            return produtos
            
        except Exception as e:
            print(f"Erro ao listar produtos: {str(e)}")
            return []
    
    def buscar_produtos(self, termo):
        """Busca produtos pelo termo de pesquisa."""
        try:
            query = """
                SELECT * FROM produtos
                WHERE codigo LIKE ? OR nome LIKE ? OR categoria LIKE ?
                ORDER BY nome
            """
            params = (f"%{termo}%", f"%{termo}%", f"%{termo}%")
            
            # Use execute_query instead of fetch_all
            result = self.db_controller.execute_query(query, params)
            
            # Convert results to a list of dictionaries
            produtos = []
            for row in result:
                produtos.append(dict(row))
            
            return produtos
        except Exception as e:
            print(f"Erro ao buscar produtos: {str(e)}")
            return []
    
    def buscar_produto_por_codigo(self, codigo):
        """Busca um produto pelo código."""
        try:
            query = "SELECT * FROM produtos WHERE codigo = ?"
            
            # Use execute_query instead of fetch_one
            result = self.db_controller.execute_query(query, (codigo,))
            
            # Check if we got any results
            if result and len(result) > 0:
                # Return the first row as a dictionary
                return dict(result[0])
            else:
                return None
        except Exception as e:
            print(f"Erro ao buscar produto por código: {str(e)}")
            return None
    
    def obter_produto(self, produto_id):
        """
        Obtém um produto pelo ID.
        
        Args:
            produto_id (int): ID do produto.
        
        Returns:
            dict: Dados do produto ou None se não encontrado.
        """
        try:
            print(f"Carregando produto com ID: {produto_id}")
            
            # Use execute_query instead of fetch_one
            query = "SELECT * FROM produtos WHERE id = ?"
            result = self.db_controller.execute_query(query, [produto_id])
            
            # Check if we got any results
            if result and len(result) > 0:
                # Convert the first row to a dictionary
                produto = dict(result[0])
                print(f"Produto encontrado: {produto}")
                return produto
            else:
                print(f"Produto com ID {produto_id} não encontrado.")
                return None
                
        except Exception as e:
            print(f"Erro ao obter produto: {str(e)}")
            return None
    
    def inserir_produto(self, produto_data):
        """Insere um novo produto no banco de dados."""
        try:
            # Verifica se o código já existe
            produto_existente = self.buscar_produto_por_codigo(produto_data["codigo"])
            if produto_existente:
                return {"sucesso": False, "mensagem": f"Já existe um produto com o código {produto_data['codigo']}."}
            
            query = """
                INSERT INTO produtos (
                    codigo, nome, categoria, preco, estoque, minimo, 
                    fornecedor, descricao, imagem, data_cadastro
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                produto_data["codigo"],
                produto_data["nome"],
                produto_data["categoria"],
                produto_data["preco"],
                produto_data["estoque"],
                produto_data.get("minimo", 0),
                produto_data.get("fornecedor", ""),
                produto_data.get("descricao", ""),
                produto_data.get("imagem", ""),
                produto_data.get("data_cadastro", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            
            self.db_controller.execute_query(query, params)
            return {"sucesso": True}
        except Exception as e:
            print(f"Erro ao inserir produto: {str(e)}")
            return {"sucesso": False, "mensagem": str(e)}
    
    def atualizar_produto(self, produto_data):
        """Atualiza um produto existente no banco de dados."""
        try:
            # Verifica se o código já existe em outro produto
            produto_existente = self.buscar_produto_por_codigo(produto_data["codigo"])
            if produto_existente and str(produto_existente["id"]) != str(produto_data["id"]):
                return {"sucesso": False, "mensagem": f"Já existe outro produto com o código {produto_data['codigo']}."}
            
            query = """
                UPDATE produtos SET 
                    codigo = ?, nome = ?, categoria = ?, preco = ?, 
                    estoque = ?, minimo = ?, fornecedor = ?, 
                    descricao = ?, imagem = ?
                WHERE id = ?
            """
            params = (
                produto_data["codigo"],
                produto_data["nome"],
                produto_data["categoria"],
                produto_data["preco"],
                produto_data["estoque"],
                produto_data.get("minimo", 0),
                produto_data.get("fornecedor", ""),
                produto_data.get("descricao", ""),
                produto_data.get("imagem", ""),
                produto_data["id"]
            )
            
            self.db_controller.execute_query(query, params)
            return {"sucesso": True}
        except Exception as e:
            print(f"Erro ao atualizar produto: {str(e)}")
            return {"sucesso": False, "mensagem": str(e)}
    
    def excluir_produto(self, produto_id):
        """Exclui um produto do banco de dados."""
        try:
            # Verifica se o produto está sendo usado em alguma venda
            query_check = """
                SELECT COUNT(*) as count FROM itens_venda
                WHERE produto_id = ?
            """
            result = self.db_controller.execute_query(query_check, (produto_id,))
            
            # Check if we got any results and if the count is greater than 0
            if result and len(result) > 0 and result[0]['count'] > 0:
                return {
                    "sucesso": False, 
                    "mensagem": "Este produto não pode ser excluído pois está associado a vendas."
                }
            
            # Exclui o produto
            query = "DELETE FROM produtos WHERE id = ?"
            self.db_controller.execute_query(query, (produto_id,))
            
            return {"sucesso": True}
        except Exception as e:
            print(f"Erro ao excluir produto: {str(e)}")
            return {"sucesso": False, "mensagem": str(e)}
    
    def importar_produtos(self, arquivo):
        """Importa produtos de um arquivo CSV."""
        try:
            produtos_importados = 0
            produtos_atualizados = 0
            
            with open(arquivo, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    # Verifica se o produto já existe pelo código
                    produto_existente = self.buscar_produto_por_codigo(row['codigo'])
                    
                    produto_data = {
                        "codigo": row['codigo'],
                        "nome": row['nome'],
                        "categoria": row['categoria'],
                        "preco": float(row['preco'].replace(',', '.')),
                        "estoque": int(row['estoque']),
                        "minimo": int(row.get('minimo', 0)),
                        "fornecedor": row.get('fornecedor', ''),
                        "descricao": row.get('descricao', ''),
                        "imagem": row.get('imagem', '')
                    }
                    
                    if produto_existente:
                        # Atualiza o produto existente
                        produto_data["id"] = produto_existente["id"]
                        self.atualizar_produto(produto_data)
                        produtos_atualizados += 1
                    else:
                        # Insere um novo produto
                        produto_data["data_cadastro"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.inserir_produto(produto_data)
                        produtos_importados += 1
            
            return {
                "sucesso": True, 
                "mensagem": f"Importação concluída! {produtos_importados} produtos importados e {produtos_atualizados} atualizados."
            }
        except Exception as e:
            print(f"Erro ao importar produtos: {str(e)}")
            return {"sucesso": False, "mensagem": f"Erro ao importar produtos: {str(e)}"}
    
    def exportar_produtos(self, arquivo):
        """Exporta produtos para um arquivo CSV."""
        try:
            produtos = self.listar_produtos()
            
            with open(arquivo, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['codigo', 'nome', 'categoria', 'preco', 'estoque', 'minimo', 
                             'fornecedor', 'descricao', 'imagem', 'data_cadastro']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                writer.writeheader()
                for produto in produtos:
                    writer.writerow({
                        'codigo': produto['codigo'],
                        'nome': produto['nome'],
                        'categoria': produto['categoria'],
                        'preco': produto['preco'],
                        'estoque': produto['estoque'],
                        'minimo': produto.get('minimo', 0),
                        'fornecedor': produto.get('fornecedor', ''),
                        'descricao': produto.get('descricao', ''),
                        'imagem': produto.get('imagem', ''),
                        'data_cadastro': produto.get('data_cadastro', '')
                    })
            
            return {"sucesso": True, "mensagem": f"{len(produtos)} produtos exportados com sucesso!"}
        except Exception as e:
            print(f"Erro ao exportar produtos: {str(e)}")
            return {"sucesso": False, "mensagem": f"Erro ao exportar produtos: {str(e)}"}