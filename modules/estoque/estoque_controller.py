import datetime
from modules.utils.database import get_db_connection

class EstoqueController:
    def __init__(self):
        """Inicializa o controlador de estoque."""
        pass
    
    def listar_produtos(self, filtro=None, categoria_id=None, ordenar_por="nome", ordem="ASC"):
        """
        Lista os produtos do estoque com opções de filtro e ordenação.
        
        Args:
            filtro (str): Texto para filtrar por nome, código ou descrição
            categoria_id (int): ID da categoria para filtrar
            ordenar_por (str): Campo para ordenação
            ordem (str): Ordem (ASC ou DESC)
            
        Returns:
            list: Lista de produtos
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Constrói a consulta SQL
        sql = """
            SELECT p.id, p.codigo, p.nome, p.descricao, p.preco_custo, p.preco_venda,
                   p.estoque_atual, p.estoque_minimo, p.unidade, p.localizacao,
                   c.nome as categoria_nome, f.nome as fornecedor_nome
            FROM produtos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
            WHERE 1=1
        """
        params = []
        
        # Adiciona filtros
        if filtro:
            sql += " AND (p.nome LIKE ? OR p.codigo LIKE ? OR p.descricao LIKE ? OR p.codigo_barras LIKE ?)"
            params.extend([f"%{filtro}%", f"%{filtro}%", f"%{filtro}%", f"%{filtro}%"])
        
        if categoria_id:
            sql += " AND p.categoria_id = ?"
            params.append(categoria_id)
        
        # Adiciona ordenação
        valid_fields = ["nome", "codigo", "preco_venda", "estoque_atual"]
        if ordenar_por in valid_fields:
            sql += f" ORDER BY p.{ordenar_por}"
        else:
            sql += " ORDER BY p.nome"
        
        if ordem.upper() == "DESC":
            sql += " DESC"
        else:
            sql += " ASC"
        
        cursor.execute(sql, params)
        produtos = [dict(produto) for produto in cursor.fetchall()]
        conn.close()
        
        return produtos
    
    def obter_produto(self, produto_id):
        """
        Obtém os detalhes de um produto específico.
        
        Args:
            produto_id (int): ID do produto
            
        Returns:
            dict: Dados do produto ou None se não encontrado
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT p.*, c.nome as categoria_nome, f.nome as fornecedor_nome
            FROM produtos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
            WHERE p.id = ?
        """, (produto_id,))
        
        produto = cursor.fetchone()
        conn.close()
        
        if produto:
            return dict(produto)
        return None
    
    def adicionar_produto(self, produto_data):
        """
        Adiciona um novo produto ao estoque.
        
        Args:
            produto_data (dict): Dados do produto
            
        Returns:
            int: ID do produto adicionado ou None em caso de erro
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Verifica se o código já existe
            cursor.execute("SELECT id FROM produtos WHERE codigo = ?", (produto_data['codigo'],))
            if cursor.fetchone():
                conn.close()
                return {"erro": "Código de produto já cadastrado."}
            
            # Insere o produto
            cursor.execute("""
                INSERT INTO produtos (
                    codigo, nome, descricao, categoria_id, fornecedor_id,
                    preco_custo, preco_venda, margem_lucro, estoque_atual,
                    estoque_minimo, unidade, localizacao, codigo_barras,
                    data_cadastro, ultima_atualizacao
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                produto_data['codigo'],
                produto_data['nome'],
                produto_data.get('descricao', ''),
                produto_data.get('categoria_id'),
                produto_data.get('fornecedor_id'),
                produto_data.get('preco_custo', 0),
                produto_data.get('preco_venda', 0),
                produto_data.get('margem_lucro', 0),
                produto_data.get('estoque_atual', 0),
                produto_data.get('estoque_minimo', 5),
                produto_data.get('unidade', 'UN'),
                produto_data.get('localizacao', ''),
                produto_data.get('codigo_barras', ''),
                datetime.datetime.now(),
                datetime.datetime.now()
            ))
            
            produto_id = cursor.lastrowid
            
            # Se houver estoque inicial, registra a movimentação
            if produto_data.get('estoque_atual', 0) > 0:
                cursor.execute("""
                    INSERT INTO movimentacoes_estoque (
                        produto_id, tipo, quantidade, motivo, usuario_id, data_movimentacao
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    produto_id,
                    'entrada',
                    produto_data.get('estoque_atual', 0),
                    'Estoque inicial',
                    produto_data.get('usuario_id', 1),
                    datetime.datetime.now()
                ))
            
            conn.commit()
            conn.close()
            
            return produto_id
            
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            print(f"Erro ao adicionar produto: {e}")
            return None
    
    def atualizar_produto(self, produto_id, produto_data):
        """
        Atualiza os dados de um produto existente.
        
        Args:
            produto_id (int): ID do produto
            produto_data (dict): Novos dados do produto
            
        Returns:
            bool: True se atualizado com sucesso, False caso contrário
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Verifica se o produto existe
            cursor.execute("SELECT estoque_atual FROM produtos WHERE id = ?", (produto_id,))
            produto_atual = cursor.fetchone()
            if not produto_atual:
                conn.close()
                return False
            
            estoque_atual = produto_atual['estoque_atual']
            
            # Atualiza o produto
            cursor.execute("""
                UPDATE produtos SET
                    codigo = ?,
                    nome = ?,
                    descricao = ?,
                    categoria_id = ?,
                    fornecedor_id = ?,
                    preco_custo = ?,
                    preco_venda = ?,
                    margem_lucro = ?,
                    estoque_minimo = ?,
                    unidade = ?,
                    localizacao = ?,
                    codigo_barras = ?,
                    ultima_atualizacao = ?
                WHERE id = ?
            """, (
                produto_data['codigo'],
                produto_data['nome'],
                produto_data.get('descricao', ''),
                produto_data.get('categoria_id'),
                produto_data.get('fornecedor_id'),
                produto_data.get('preco_custo', 0),
                produto_data.get('preco_venda', 0),
                produto_data.get('margem_lucro', 0),
                produto_data.get('estoque_minimo', 5),
                produto_data.get('unidade', 'UN'),
                produto_data.get('localizacao', ''),
                produto_data.get('codigo_barras', ''),
                datetime.datetime.now(),
                produto_id
            ))
            
            # Se o estoque foi alterado, registra a movimentação
            novo_estoque = produto_data.get('estoque_atual')
            if novo_estoque is not None and novo_estoque != estoque_atual:
                diferenca = novo_estoque - estoque_atual
                tipo = 'entrada' if diferenca > 0 else 'saida'
                
                cursor.execute("""
                    UPDATE produtos SET estoque_atual = ? WHERE id = ?
                """, (novo_estoque, produto_id))
                
                cursor.execute("""
                    INSERT INTO movimentacoes_estoque (
                        produto_id, tipo, quantidade, motivo, usuario_id, data_movimentacao
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    produto_id,
                    tipo,
                    abs(diferenca),
                    'Ajuste de estoque',
                    produto_data.get('usuario_id', 1),
                    datetime.datetime.now()
                ))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            print(f"Erro ao atualizar produto: {e}")
            return False
    
    def excluir_produto(self, produto_id):
        """
        Exclui um produto do estoque.
        
        Args:
            produto_id (int): ID do produto
            
        Returns:
            bool: True se excluído com sucesso, False caso contrário
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Verifica se o produto existe
            cursor.execute("SELECT id FROM produtos WHERE id = ?", (produto_id,))
            if not cursor.fetchone():
                conn.close()
                return False
            
            # Verifica se o produto tem movimentações
            cursor.execute("SELECT COUNT(*) as count FROM movimentacoes_estoque WHERE produto_id = ?", (produto_id,))
            if cursor.fetchone()['count'] > 0:
                conn.close()
                return {"erro": "Não é possível excluir um produto com movimentações de estoque."}
            
            # Verifica se o produto tem vendas
            cursor.execute("SELECT COUNT(*) as count FROM itens_venda WHERE produto_id = ?", (produto_id,))
            if cursor.fetchone()['count'] > 0:
                conn.close()
                return {"erro": "Não é possível excluir um produto com vendas registradas."}
            
            # Exclui o produto
            cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            print(f"Erro ao excluir produto: {e}")
            return False
    
    def registrar_movimentacao(self, movimentacao_data):
        """
        Registra uma movimentação de estoque.
        
        Args:
            movimentacao_data (dict): Dados da movimentação
            
        Returns:
            int: ID da movimentação registrada ou None em caso de erro
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Inicia uma transação
            conn.execute("BEGIN TRANSACTION")
            
            produto_id = movimentacao_data['produto_id']
            quantidade = movimentacao_data['quantidade']
            tipo = movimentacao_data['tipo']
            
            # Atualiza o estoque do produto
            if tipo == 'entrada':
                cursor.execute("""
                    UPDATE produtos
                    SET estoque_atual = estoque_atual + ?, ultima_atualizacao = ?
                    WHERE id = ?
                """, (quantidade, datetime.datetime.now(), produto_id))
            else:  # saída
                # Verifica se há estoque suficiente
                cursor.execute("SELECT estoque_atual FROM produtos WHERE id = ?", (produto_id,))
                estoque_atual = cursor.fetchone()['estoque_atual']
                
                if estoque_atual < quantidade:
                    conn.rollback()
                    conn.close()
                    return {"erro": "Estoque insuficiente para esta movimentação."}
                
                cursor.execute("""
                    UPDATE produtos
                    SET estoque_atual = estoque_atual - ?, ultima_atualizacao = ?
                    WHERE id = ?
                """, (quantidade, datetime.datetime.now(), produto_id))
            
            # Registra a movimentação
            cursor.execute("""
                INSERT INTO movimentacoes_estoque (
                    produto_id, tipo, quantidade, motivo, usuario_id, 
                    data_movimentacao, documento_referencia
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                produto_id,
                tipo,
                quantidade,
                movimentacao_data.get('motivo', ''),
                movimentacao_data.get('usuario_id', 1),
                datetime.datetime.now(),
                movimentacao_data.get('documento_referencia', '')
            ))
            
            movimentacao_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            
            return movimentacao_id
            
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            print(f"Erro ao registrar movimentação: {e}")
            return None
    def listar_movimentacoes(self, produto_id=None, tipo=None, data_inicio=None, data_fim=None):
        """
        Lista as movimentações de estoque com opções de filtro.
        
        Args:
            produto_id (int): ID do produto para filtrar
            tipo (str): Tipo de movimentação (entrada, saida, ajuste)
            data_inicio (str): Data inicial para filtro
            data_fim (str): Data final para filtro
            
        Returns:
            list: Lista de movimentações
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Constrói a consulta SQL
        sql = """
            SELECT m.id, m.tipo, m.quantidade, m.motivo, m.data_movimentacao,
                   p.nome as produto_nome, p.codigo as produto_codigo,
                   u.nome as usuario_nome
            FROM movimentacoes_estoque m
            JOIN produtos p ON m.produto_id = p.id
            LEFT JOIN usuarios u ON m.usuario_id = u.id
            WHERE 1=1
        """
        params = []
        
        # Adiciona filtros
        if produto_id:
            sql += " AND m.produto_id = ?"
            params.append(produto_id)
        
        if tipo:
            sql += " AND m.tipo = ?"
            params.append(tipo)
        
        if data_inicio:
            sql += " AND m.data_movimentacao >= ?"
            params.append(data_inicio)
        
        if data_fim:
            sql += " AND m.data_movimentacao <= ?"
            params.append(data_fim)
        
        # Ordena por data, mais recente primeiro
        sql += " ORDER BY m.data_movimentacao DESC"
        
        cursor.execute(sql, params)
        movimentacoes = [dict(mov) for mov in cursor.fetchall()]
        conn.close()
        
        return movimentacoes
    
    def listar_categorias(self):
        """
        Lista todas as categorias de produtos.
        
        Returns:
            list: Lista de categorias
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, nome, descricao FROM categorias ORDER BY nome")
        categorias = [dict(cat) for cat in cursor.fetchall()]
        conn.close()
        
        return categorias
    
    def listar_fornecedores(self):
        """
        Lista todos os fornecedores.
        
        Returns:
            list: Lista de fornecedores
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, nome, cnpj, telefone FROM fornecedores ORDER BY nome")
        fornecedores = [dict(forn) for forn in cursor.fetchall()]
        conn.close()
        
        return fornecedores
    
    def adicionar_categoria(self, nome, descricao=""):
        """
        Adiciona uma nova categoria de produtos.
        
        Args:
            nome (str): Nome da categoria
            descricao (str): Descrição da categoria
            
        Returns:
            int: ID da categoria adicionada ou None em caso de erro
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO categorias (nome, descricao) VALUES (?, ?)",
                (nome, descricao)
            )
            
            categoria_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return categoria_id
            
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            print(f"Erro ao adicionar categoria: {e}")
            return None
    
    def adicionar_fornecedor(self, fornecedor_data):
        """
        Adiciona um novo fornecedor.
        
        Args:
            fornecedor_data (dict): Dados do fornecedor
            
        Returns:
            int: ID do fornecedor adicionado ou None em caso de erro
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO fornecedores (
                    nome, cnpj, endereco, telefone, email, contato
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                fornecedor_data['nome'],
                fornecedor_data.get('cnpj', ''),
                fornecedor_data.get('endereco', ''),
                fornecedor_data.get('telefone', ''),
                fornecedor_data.get('email', ''),
                fornecedor_data.get('contato', '')
            ))
            
            fornecedor_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return fornecedor_id
            
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            print(f"Erro ao adicionar fornecedor: {e}")
            return None
    
    def gerar_relatorio_estoque(self, filtro=None, categoria_id=None, apenas_baixo_estoque=False):
        """
        Gera um relatório de estoque com opções de filtro.
        
        Args:
            filtro (str): Texto para filtrar por nome, código ou descrição
            categoria_id (int): ID da categoria para filtrar
            apenas_baixo_estoque (bool): Se True, mostra apenas produtos abaixo do estoque mínimo
            
        Returns:
            dict: Dados do relatório
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Constrói a consulta SQL
        sql = """
            SELECT p.id, p.codigo, p.nome, p.preco_custo, p.preco_venda,
                   p.estoque_atual, p.estoque_minimo, p.unidade,
                   c.nome as categoria_nome
            FROM produtos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE 1=1
        """
        params = []
        
        # Adiciona filtros
        if filtro:
            sql += " AND (p.nome LIKE ? OR p.codigo LIKE ? OR p.descricao LIKE ?)"
            params.extend([f"%{filtro}%", f"%{filtro}%", f"%{filtro}%"])
        
        if categoria_id:
            sql += " AND p.categoria_id = ?"
            params.append(categoria_id)
        
        if apenas_baixo_estoque:
            sql += " AND p.estoque_atual < p.estoque_minimo"
        
        # Ordena por nome
        sql += " ORDER BY p.nome"
        
        cursor.execute(sql, params)
        produtos = [dict(produto) for produto in cursor.fetchall()]
        
        # Calcula estatísticas
        cursor.execute("SELECT COUNT(*) as total FROM produtos")
        total_produtos = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM produtos WHERE estoque_atual < estoque_minimo")
        produtos_baixo_estoque = cursor.fetchone()['total']
        
        cursor.execute("SELECT SUM(estoque_atual * preco_custo) as valor_total FROM produtos")
        valor_total = cursor.fetchone()['valor_total'] or 0
        
        conn.close()
        
        # Monta o relatório
        relatorio = {
            "data_geracao": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "total_produtos": total_produtos,
            "produtos_baixo_estoque": produtos_baixo_estoque,
            "valor_total_estoque": valor_total,
            "produtos": produtos
        }
        
        return relatorio