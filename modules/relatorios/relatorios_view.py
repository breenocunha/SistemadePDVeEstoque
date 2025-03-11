import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import datetime
import csv

class RelatoriosView:
    def __init__(self, parent, db_controller):
        self.parent = parent
        self.db_controller = db_controller
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título com estilo
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="#9b59b6", corner_radius=10)
        title_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="RELATÓRIOS", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=10)
        
        # Frame para seleção de relatório
        select_frame = ctk.CTkFrame(self.main_frame)
        select_frame.pack(fill="x", padx=10, pady=10)
        
        select_label = ctk.CTkLabel(select_frame, text="Selecione o relatório:")
        select_label.pack(side="left", padx=5)
        
        self.relatorio_var = ctk.StringVar(value="Vendas por Período")
        relatorio_options = ["Vendas por Período", "Produtos Mais Vendidos", "Estoque Baixo", "Clientes por Compras"]
        
        relatorio_combobox = ctk.CTkComboBox(
            select_frame, 
            values=relatorio_options,
            variable=self.relatorio_var,
            width=250,
            state="readonly"
        )
        relatorio_combobox.pack(side="left", padx=5)
        
        # Frame para filtros
        self.filtros_frame = ctk.CTkFrame(self.main_frame)
        self.filtros_frame.pack(fill="x", padx=10, pady=10)
        
        # Filtros para Vendas por Período (padrão)
        self.criar_filtros_vendas_periodo()
        
        # Bind para alteração do tipo de relatório
        self.relatorio_var.trace_add("write", self.alterar_filtros)
        
        # Frame para botões de ação
        actions_frame = ctk.CTkFrame(self.main_frame)
        actions_frame.pack(fill="x", padx=10, pady=10)
        
        gerar_btn = ctk.CTkButton(
            actions_frame, 
            text="Gerar Relatório", 
            command=self.gerar_relatorio,
            fg_color="#9b59b6",
            hover_color="#8e44ad",
            height=40
        )
        gerar_btn.pack(side="left", padx=5)
        
        exportar_btn = ctk.CTkButton(
            actions_frame, 
            text="Exportar para CSV", 
            command=self.exportar_csv,
            fg_color="#3498db",
            hover_color="#2980b9",
            height=40
        )
        exportar_btn.pack(side="left", padx=5)
        
        # Frame para a tabela de resultados
        table_frame = ctk.CTkFrame(self.main_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tabela de resultados (inicialmente vazia)
        self.resultados_tree = ttk.Treeview(table_frame)
        
        # Configuração inicial para Vendas por Período
        self.resultados_tree["columns"] = ("id", "data", "cliente", "total", "pagamento", "status")
        self.resultados_tree.heading("id", text="ID")
        self.resultados_tree.heading("data", text="Data")
        self.resultados_tree.heading("cliente", text="Cliente")
        self.resultados_tree.heading("total", text="Total")
        self.resultados_tree.heading("pagamento", text="Pagamento")
        self.resultados_tree.heading("status", text="Status")
        
        self.resultados_tree.column("id", width=50)
        self.resultados_tree.column("data", width=150)
        self.resultados_tree.column("cliente", width=200)
        self.resultados_tree.column("total", width=100)
        self.resultados_tree.column("pagamento", width=150)
        self.resultados_tree.column("status", width=100)
        
        # Oculta a coluna de índice
        self.resultados_tree["show"] = "headings"
        
        # Adiciona barra de rolagem
        scrollbar = ctk.CTkScrollbar(table_frame, command=self.resultados_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.resultados_tree.configure(yscrollcommand=scrollbar.set)
        
        self.resultados_tree.pack(fill="both", expand=True)
        
        # Frame para resumo
        self.resumo_frame = ctk.CTkFrame(self.main_frame)
        self.resumo_frame.pack(fill="x", padx=10, pady=10)
        
        self.resumo_label = ctk.CTkLabel(
            self.resumo_frame, 
            text="Total: R$ 0,00 | Quantidade: 0",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.resumo_label.pack(pady=10)
    
    def criar_filtros_vendas_periodo(self):
        """Cria os filtros para o relatório de vendas por período."""
        # Limpa o frame de filtros
        for widget in self.filtros_frame.winfo_children():
            widget.destroy()
        
        # Data inicial
        data_inicial_frame = ctk.CTkFrame(self.filtros_frame)
        data_inicial_frame.pack(side="left", padx=10, pady=5)
        
        data_inicial_label = ctk.CTkLabel(data_inicial_frame, text="Data Inicial:")
        data_inicial_label.pack(anchor="w")
        
        self.data_inicial_var = ctk.StringVar(value=datetime.datetime.now().strftime("%Y-%m-%d"))
        data_inicial_entry = ctk.CTkEntry(data_inicial_frame, textvariable=self.data_inicial_var, width=120)
        data_inicial_entry.pack(pady=5)
        
        # Data final
        data_final_frame = ctk.CTkFrame(self.filtros_frame)
        data_final_frame.pack(side="left", padx=10, pady=5)
        
        data_final_label = ctk.CTkLabel(data_final_frame, text="Data Final:")
        data_final_label.pack(anchor="w")
        
        self.data_final_var = ctk.StringVar(value=datetime.datetime.now().strftime("%Y-%m-%d"))
        data_final_entry = ctk.CTkEntry(data_final_frame, textvariable=self.data_final_var, width=120)
        data_final_entry.pack(pady=5)
        
        # Status
        status_frame = ctk.CTkFrame(self.filtros_frame)
        status_frame.pack(side="left", padx=10, pady=5)
        
        status_label = ctk.CTkLabel(status_frame, text="Status:")
        status_label.pack(anchor="w")
        
        self.status_var = ctk.StringVar(value="Todos")
        status_options = ["Todos", "Concluída", "Cancelada"]
        
        status_combobox = ctk.CTkComboBox(
            status_frame, 
            values=status_options,
            variable=self.status_var,
            width=120,
            state="readonly"
        )
        status_combobox.pack(pady=5)
    
    def criar_filtros_produtos_vendidos(self):
        """Cria os filtros para o relatório de produtos mais vendidos."""
        # Limpa o frame de filtros
        for widget in self.filtros_frame.winfo_children():
            widget.destroy()
        
        # Data inicial
        data_inicial_frame = ctk.CTkFrame(self.filtros_frame)
        data_inicial_frame.pack(side="left", padx=10, pady=5)
        
        data_inicial_label = ctk.CTkLabel(data_inicial_frame, text="Data Inicial:")
        data_inicial_label.pack(anchor="w")
        
        self.data_inicial_var = ctk.StringVar(value=datetime.datetime.now().strftime("%d/%m/%Y"))
        data_inicial_entry = ctk.CTkEntry(data_inicial_frame, textvariable=self.data_inicial_var, width=120)
        data_inicial_entry.pack(pady=5)
        
        # Data final
        data_final_frame = ctk.CTkFrame(self.filtros_frame)
        data_final_frame.pack(side="left", padx=10, pady=5)
        
        data_final_label = ctk.CTkLabel(data_final_frame, text="Data Final:")
        data_final_label.pack(anchor="w")
        
        self.data_final_var = ctk.StringVar(value=datetime.datetime.now().strftime("%d/%m/%Y"))
        data_final_entry = ctk.CTkEntry(data_final_frame, textvariable=self.data_final_var, width=120)
        data_final_entry.pack(pady=5)
        
        # Limite
        limite_frame = ctk.CTkFrame(self.filtros_frame)
        limite_frame.pack(side="left", padx=10, pady=5)
        
        limite_label = ctk.CTkLabel(limite_frame, text="Limite:")
        limite_label.pack(anchor="w")
        
        self.limite_var = ctk.StringVar(value="10")
        limite_entry = ctk.CTkEntry(limite_frame, textvariable=self.limite_var, width=80)
        limite_entry.pack(pady=5)
    
    def criar_filtros_estoque_baixo(self):
        """Cria os filtros para o relatório de estoque baixo."""
        # Limpa o frame de filtros
        for widget in self.filtros_frame.winfo_children():
            widget.destroy()
        
        # Categoria
        categoria_frame = ctk.CTkFrame(self.filtros_frame)
        categoria_frame.pack(side="left", padx=10, pady=5)
        
        categoria_label = ctk.CTkLabel(categoria_frame, text="Categoria:")
        categoria_label.pack(anchor="w")
        
        self.categoria_var = ctk.StringVar(value="Todas")
        
        # Busca as categorias no banco de dados
        categorias = ["Todas"]
        try:
            query = "SELECT DISTINCT categoria FROM produtos ORDER BY categoria"
            resultado = self.db_controller.execute_query(query)
            if resultado:
                for item in resultado:
                    if item["categoria"] and item["categoria"] not in categorias:
                        categorias.append(item["categoria"])
        except Exception as e:
            print(f"Erro ao buscar categorias: {str(e)}")
        
        categoria_combobox = ctk.CTkComboBox(
            categoria_frame, 
            values=categorias,
            variable=self.categoria_var,
            width=150,
            state="readonly"
        )
        categoria_combobox.pack(pady=5)
        
        # Mostrar apenas abaixo do mínimo
        self.abaixo_minimo_var = ctk.BooleanVar(value=True)
        abaixo_minimo_check = ctk.CTkCheckBox(
            self.filtros_frame, 
            text="Apenas produtos abaixo do mínimo",
            variable=self.abaixo_minimo_var
        )
        abaixo_minimo_check.pack(side="left", padx=10, pady=5)
    
    def criar_filtros_clientes_compras(self):
        """Cria os filtros para o relatório de clientes por compras."""
        # Limpa o frame de filtros
        for widget in self.filtros_frame.winfo_children():
            widget.destroy()
        
        # Data inicial
        data_inicial_frame = ctk.CTkFrame(self.filtros_frame)
        data_inicial_frame.pack(side="left", padx=10, pady=5)
        
        data_inicial_label = ctk.CTkLabel(data_inicial_frame, text="Data Inicial:")
        data_inicial_label.pack(anchor="w")
        
        self.data_inicial_var = ctk.StringVar(value=datetime.datetime.now().strftime("%d/%m/%Y"))
        data_inicial_entry = ctk.CTkEntry(data_inicial_frame, textvariable=self.data_inicial_var, width=120)
        data_inicial_entry.pack(pady=5)
        
        # Data final
        data_final_frame = ctk.CTkFrame(self.filtros_frame)
        data_final_frame.pack(side="left", padx=10, pady=5)
        
        data_final_label = ctk.CTkLabel(data_final_frame, text="Data Final:")
        data_final_label.pack(anchor="w")
        
        self.data_final_var = ctk.StringVar(value=datetime.datetime.now().strftime("%d/%m/%Y"))
        data_final_entry = ctk.CTkEntry(data_final_frame, textvariable=self.data_final_var, width=120)
        data_final_entry.pack(pady=5)
        
        # Limite
        limite_frame = ctk.CTkFrame(self.filtros_frame)
        limite_frame.pack(side="left", padx=10, pady=5)
        
        limite_label = ctk.CTkLabel(limite_frame, text="Limite:")
        limite_label.pack(anchor="w")
        
        self.limite_var = ctk.StringVar(value="10")
        limite_entry = ctk.CTkEntry(limite_frame, textvariable=self.limite_var, width=80)
        limite_entry.pack(pady=5)
    
    def alterar_filtros(self, *args):
        """Altera os filtros de acordo com o tipo de relatório selecionado."""
        relatorio = self.relatorio_var.get()
        
        if relatorio == "Vendas por Período":
            self.criar_filtros_vendas_periodo()
            
            # Configura a tabela
            self.resultados_tree["columns"] = ("id", "data", "cliente", "total", "pagamento", "status")
            self.resultados_tree.heading("id", text="ID")
            self.resultados_tree.heading("data", text="Data")
            self.resultados_tree.heading("cliente", text="Cliente")
            self.resultados_tree.heading("total", text="Total")
            self.resultados_tree.heading("pagamento", text="Pagamento")
            self.resultados_tree.heading("status", text="Status")
            
            self.resultados_tree.column("id", width=50)
            self.resultados_tree.column("data", width=150)
            self.resultados_tree.column("cliente", width=200)
            self.resultados_tree.column("total", width=100)
            self.resultados_tree.column("pagamento", width=150)
            self.resultados_tree.column("status", width=100)
            
        elif relatorio == "Produtos Mais Vendidos":
            self.criar_filtros_produtos_vendidos()
            
            # Configura a tabela
            self.resultados_tree["columns"] = ("codigo", "nome", "quantidade", "total", "percentual")
            self.resultados_tree.heading("codigo", text="Código")
            self.resultados_tree.heading("nome", text="Produto")
            self.resultados_tree.heading("quantidade", text="Quantidade")
            self.resultados_tree.heading("total", text="Total Vendido")
            self.resultados_tree.heading("percentual", text="% do Total")
            
            self.resultados_tree.column("codigo", width=100)
            self.resultados_tree.column("nome", width=250)
            self.resultados_tree.column("quantidade", width=100)
            self.resultados_tree.column("total", width=150)
            self.resultados_tree.column("percentual", width=100)
            
        elif relatorio == "Estoque Baixo":
            self.criar_filtros_estoque_baixo()
            
            # Configura a tabela
            self.resultados_tree["columns"] = ("codigo", "nome", "categoria", "estoque", "minimo", "status")
            self.resultados_tree.heading("codigo", text="Código")
            self.resultados_tree.heading("nome", text="Produto")
            self.resultados_tree.heading("categoria", text="Categoria")
            self.resultados_tree.heading("estoque", text="Estoque")
            self.resultados_tree.heading("minimo", text="Mínimo")
            self.resultados_tree.heading("status", text="Status")
            
            self.resultados_tree.column("codigo", width=100)
            self.resultados_tree.column("nome", width=250)
            self.resultados_tree.column("categoria", width=150)
            self.resultados_tree.column("estoque", width=80)
            self.resultados_tree.column("minimo", width=80)
            self.resultados_tree.column("status", width=100)
            
        elif relatorio == "Clientes por Compras":
            self.criar_filtros_clientes_compras()
            
            # Configura a tabela
            self.resultados_tree["columns"] = ("id", "nome", "cpf", "compras", "total", "media")
            self.resultados_tree.heading("id", text="ID")
            self.resultados_tree.heading("nome", text="Cliente")
            self.resultados_tree.heading("cpf", text="CPF")
            self.resultados_tree.heading("compras", text="Nº Compras")
            self.resultados_tree.heading("total", text="Total Gasto")
            self.resultados_tree.heading("media", text="Média por Compra")
            
            self.resultados_tree.column("id", width=50)
            self.resultados_tree.column("nome", width=250)
            self.resultados_tree.column("cpf", width=150)
            self.resultados_tree.column("compras", width=100)
            self.resultados_tree.column("total", width=150)
            self.resultados_tree.column("media", width=150)
        
        # Limpa a tabela
        for item in self.resultados_tree.get_children():
            self.resultados_tree.delete(item)
        
        # Atualiza o resumo
        self.resumo_label.configure(text="Total: R$ 0,00 | Quantidade: 0")
    
    def gerar_relatorio(self):
        """Gera o relatório de acordo com o tipo selecionado."""
        relatorio = self.relatorio_var.get()
        
        # Limpa a tabela
        for item in self.resultados_tree.get_children():
            self.resultados_tree.delete(item)
        
        if relatorio == "Vendas por Período":
            self.gerar_relatorio_vendas()
        elif relatorio == "Produtos Mais Vendidos":
            self.gerar_relatorio_produtos_vendidos()
        elif relatorio == "Estoque Baixo":
            self.gerar_relatorio_estoque_baixo()
        elif relatorio == "Clientes por Compras":
            self.gerar_relatorio_clientes_compras()
    
    def gerar_relatorio_vendas(self):
        """Gera o relatório de vendas."""
        try:
            # Obtém as datas do período
            data_inicio = self.data_inicial_var.get()  # Changed from data_inicio_var to data_inicial_var
            data_fim = self.data_final_var.get()       # Changed from data_fim_var to data_final_var
            
            # Valida as datas
            if not data_inicio or not data_fim:
                messagebox.showerror("Erro", "Selecione as datas de início e fim.")
                return
            
            # Formata a data de fim para incluir o final do dia
            data_fim = data_fim + " 23:59:59"
            
            # Consulta as vendas do período
            query = """
                SELECT v.id, v.data, v.total, v.forma_pagamento, v.status,
                       COUNT(i.id) as itens_count
                FROM vendas v
                LEFT JOIN itens_venda i ON v.id = i.venda_id
                WHERE v.data BETWEEN ? AND ?
                GROUP BY v.id
                ORDER BY v.data DESC
            """
            
            vendas = self.db_controller.execute_query(query, (data_inicio, data_fim))
            
            # Se não houver vendas, exibe mensagem
            if not vendas:
                messagebox.showinfo("Informação", "Não há vendas no período selecionado.")
                return
            
            # Calcula o total de vendas
            total_vendas = sum(venda['total'] for venda in vendas)
            
            # Preenche a tabela
            for venda in vendas:
                cliente_nome = "N/A"  # Default value if no client is associated
                
                self.resultados_tree.insert(
                    "", "end", 
                    values=(
                        venda["id"],
                        venda["data"],
                        cliente_nome,
                        f"R$ {venda['total']:.2f}",
                        venda["forma_pagamento"],
                        venda["status"]
                    )
                )
            
            # Atualiza o resumo
            self.resumo_label.configure(text=f"Total: R$ {total_vendas:.2f} | Vendas: {len(vendas)}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório de vendas: {str(e)}")
    
    def gerar_relatorio_produtos_vendidos(self):
        """Gera o relatório de produtos mais vendidos."""
        try:
            # Converte as datas para o formato do banco
            data_inicial = datetime.datetime.strptime(self.data_inicial_var.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
            data_final = datetime.datetime.strptime(self.data_final_var.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
            data_final += " 23:59:59"  # Inclui o último dia inteiro
            
            # Obtém o limite
            limite = int(self.limite_var.get())
            
            # Monta a query
            query = """
                SELECT p.codigo, p.nome, 
                       SUM(iv.quantidade) as quantidade_total,
                       SUM(iv.subtotal) as valor_total
                FROM itens_venda iv
                JOIN produtos p ON iv.produto_id = p.id
                JOIN vendas v ON iv.venda_id = v.id
                WHERE v.data BETWEEN ? AND ?
                AND v.status = 'Concluída'
                GROUP BY p.id
                ORDER BY quantidade_total DESC
                LIMIT ?
            """
            params = (data_inicial, data_final, limite)
            
            # Use execute_query instead of fetch_all
            produtos = self.db_controller.execute_query(query, params)
            
            # Calcula o total geral para o percentual
            total_geral = 0
            for produto in produtos:
                total_geral += produto["valor_total"]
            
            # Preenche a tabela
            for produto in produtos:
                percentual = (produto["valor_total"] / total_geral * 100) if total_geral > 0 else 0
                
                self.resultados_tree.insert(
                    "", "end", 
                    values=(
                        produto["codigo"],
                        produto["nome"],
                        produto["quantidade_total"],
                        f"R$ {produto['valor_total']:.2f}",
                        f"{percentual:.2f}%"
                    )
                )
            
            # Atualiza o resumo
            self.resumo_label.configure(text=f"Total: R$ {total_geral:.2f} | Produtos: {len(produtos)}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")
    
    def gerar_relatorio_estoque_baixo(self):
        """Gera o relatório de produtos com estoque baixo."""
        try:
            # Monta a query
            query = "SELECT * FROM produtos WHERE 1=1"
            params = []
            
            # Adiciona filtro de categoria se necessário
            if self.categoria_var.get() != "Todas":
                query += " AND categoria = ?"
                params.append(self.categoria_var.get())
            
            # Adiciona filtro de estoque abaixo do mínimo se necessário
            if self.abaixo_minimo_var.get():
                query += " AND estoque < minimo"
            
            query += " ORDER BY (estoque - minimo) ASC"
            
            # Use execute_query instead of fetch_all
            produtos = self.db_controller.execute_query(query, tuple(params))
            
            # Preenche a tabela
            for produto in produtos:
                # Define o status do estoque
                if produto["estoque"] <= 0:
                    status = "Esgotado"
                elif produto["estoque"] < produto["minimo"]:
                    status = "Crítico"
                else:
                    status = "Normal"
                
                self.resultados_tree.insert(
                    "", "end", 
                    values=(
                        produto["codigo"],
                        produto["nome"],
                        produto["categoria"],
                        produto["estoque"],
                        produto["minimo"],
                        status
                    )
                )
            
            # Atualiza o resumo
            produtos_criticos = sum(1 for p in produtos if p["estoque"] < p["minimo"])
            self.resumo_label.configure(text=f"Total de produtos: {len(produtos)} | Abaixo do mínimo: {produtos_criticos}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")
    
    def gerar_relatorio_clientes_compras(self):
        """Gera o relatório de clientes por compras."""
        try:
            # Converte as datas para o formato do banco
            data_inicial = datetime.datetime.strptime(self.data_inicial_var.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
            data_final = datetime.datetime.strptime(self.data_final_var.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
            data_final += " 23:59:59"  # Inclui o último dia inteiro
            
            # Obtém o limite
            limite = int(self.limite_var.get())
            
            # Monta a query
            query = """
                SELECT c.id, c.nome, c.cpf,
                       COUNT(v.id) as num_compras,
                       SUM(v.total) as total_gasto
                FROM clientes c
                JOIN vendas v ON c.id = v.cliente_id
                WHERE v.data BETWEEN ? AND ?
                AND v.status = 'Concluída'
                GROUP BY c.id
                ORDER BY total_gasto DESC
                LIMIT ?
            """
            params = (data_inicial, data_final, limite)
            
            # Use execute_query instead of fetch_all
            clientes = self.db_controller.execute_query(query, params)
            
            # Preenche a tabela
            total_geral = 0
            for cliente in clientes:
                media = cliente["total_gasto"] / cliente["num_compras"] if cliente["num_compras"] > 0 else 0
                
                self.resultados_tree.insert(
                    "", "end", 
                    values=(
                        cliente["id"],
                        cliente["nome"],
                        cliente["cpf"],
                        cliente["num_compras"],
                        f"R$ {cliente['total_gasto']:.2f}",
                        f"R$ {media:.2f}"
                    )
                )
                
                total_geral += cliente["total_gasto"]
            
            # Atualiza o resumo
            self.resumo_label.configure(text=f"Total: R$ {total_geral:.2f} | Clientes: {len(clientes)}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {'Nenhum resultado encontrado' if not self.resultados_tree.get_children() else 'Erro desconhecido'}")
    
    def exportar_csv(self):
        """Exporta o relatório para o formato CSV."""
        try:
            # Verifica se há dados para exportar
            if not self.resultados_tree.get_children():
                messagebox.showinfo("Aviso", "Não há dados para exportar.")
                return
            
            # Solicita o local para salvar o arquivo
            relatorio_tipo = self.relatorio_var.get()
            data_atual = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"Relatorio_{relatorio_tipo.replace(' ', '_')}_{data_atual}.csv"
            
            arquivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv")],
                initialfile=nome_arquivo
            )
            
            if not arquivo:  # Se o usuário cancelou a operação
                return
            
            # Obtém os cabeçalhos
            colunas = self.resultados_tree["columns"]
            cabecalhos = [self.resultados_tree.heading(col)["text"] for col in colunas]
            
            # Abre o arquivo para escrita
            with open(arquivo, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Escreve o cabeçalho
                writer.writerow(cabecalhos)
                
                # Escreve os dados
                for item_id in self.resultados_tree.get_children():
                    valores = self.resultados_tree.item(item_id)["values"]
                    writer.writerow(valores)
            
            messagebox.showinfo("Sucesso", f"Relatório exportado com sucesso para {arquivo}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar relatório: {str(e)}")