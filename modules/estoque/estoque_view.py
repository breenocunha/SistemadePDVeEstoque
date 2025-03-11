import customtkinter as ctk
from tkinter import ttk, messagebox
import datetime
from modules.estoque.estoque_controller import EstoqueController
from modules.utils.widgets import NumericEntry, SearchableComboBox

class EstoqueView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = EstoqueController()
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="GESTÃO DE ESTOQUE", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=10)
        
        # Abas para diferentes funcionalidades
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Cria as abas
        self.tab_produtos = self.tabview.add("Produtos")
        self.tab_movimentacoes = self.tabview.add("Movimentações")
        self.tab_categorias = self.tabview.add("Categorias")
        self.tab_fornecedores = self.tabview.add("Fornecedores")
        
        # Configura cada aba
        self.setup_tab_produtos()
        self.setup_tab_movimentacoes()
        self.setup_tab_categorias()
        self.setup_tab_fornecedores()
        
        # Seleciona a primeira aba
        self.tabview.set("Produtos")
    
    def setup_tab_produtos(self):
        """Configura a aba de produtos."""
        # Frame de filtros
        self.filtros_frame = ctk.CTkFrame(self.tab_produtos)
        self.filtros_frame.pack(fill="x", padx=10, pady=5)
        
        # Filtro por texto
        self.filtro_label = ctk.CTkLabel(self.filtros_frame, text="Buscar:")
        self.filtro_label.pack(side="left", padx=5)
        
        self.filtro_var = ctk.StringVar()
        self.filtro_entry = ctk.CTkEntry(self.filtros_frame, textvariable=self.filtro_var, width=200)
        self.filtro_entry.pack(side="left", padx=5)
        self.filtro_entry.bind("<Return>", lambda e: self.buscar_produtos())
        
        # Filtro por categoria
        self.categoria_label = ctk.CTkLabel(self.filtros_frame, text="Categoria:")
        self.categoria_label.pack(side="left", padx=5)
        
        self.categorias = self.controller.listar_categorias()
        self.categoria_options = ["Todas"] + [cat["nome"] for cat in self.categorias]
        self.categoria_var = ctk.StringVar(value="Todas")
        self.categoria_combobox = ctk.CTkComboBox(
            self.filtros_frame, 
            values=self.categoria_options,
            variable=self.categoria_var,
            width=150
        )
        self.categoria_combobox.pack(side="left", padx=5)
        
        # Botão de busca
        self.buscar_btn = ctk.CTkButton(
            self.filtros_frame, 
            text="Buscar", 
            command=self.buscar_produtos
        )
        self.buscar_btn.pack(side="left", padx=5)
        
        # Botão para adicionar produto
        self.adicionar_btn = ctk.CTkButton(
            self.filtros_frame, 
            text="Novo Produto", 
            command=self.abrir_form_produto
        )
        self.adicionar_btn.pack(side="right", padx=5)
        
        # Frame para a tabela de produtos
        self.produtos_frame = ctk.CTkFrame(self.tab_produtos)
        self.produtos_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Tabela de produtos (usando ttk.Treeview)
        self.produtos_tree = ttk.Treeview(
            self.produtos_frame,
            columns=("codigo", "nome", "categoria", "preco", "estoque", "minimo"),
            show="headings"
        )
        
        # Define as colunas
        self.produtos_tree.heading("codigo", text="Código")
        self.produtos_tree.heading("nome", text="Nome")
        self.produtos_tree.heading("categoria", text="Categoria")
        self.produtos_tree.heading("preco", text="Preço")
        self.produtos_tree.heading("estoque", text="Estoque")
        self.produtos_tree.heading("minimo", text="Mínimo")
        
        self.produtos_tree.column("codigo", width=100)
        self.produtos_tree.column("nome", width=250)
        self.produtos_tree.column("categoria", width=150)
        self.produtos_tree.column("preco", width=100)
        self.produtos_tree.column("estoque", width=80)
        self.produtos_tree.column("minimo", width=80)
        
        # Adiciona barra de rolagem
        self.produtos_scrollbar = ctk.CTkScrollbar(self.produtos_frame, command=self.produtos_tree.yview)
        self.produtos_scrollbar.pack(side="right", fill="y")
        self.produtos_tree.configure(yscrollcommand=self.produtos_scrollbar.set)
        
        self.produtos_tree.pack(fill="both", expand=True)
        
        # Evento de duplo clique para editar
        self.produtos_tree.bind("<Double-1>", self.editar_produto_selecionado)
        
        # Botões de ação
        self.acoes_frame = ctk.CTkFrame(self.tab_produtos)
        self.acoes_frame.pack(fill="x", padx=10, pady=5)
        
        self.editar_btn = ctk.CTkButton(
            self.acoes_frame, 
            text="Editar", 
            command=self.editar_produto_selecionado
        )
        self.editar_btn.pack(side="left", padx=5, pady=5)
        
        self.excluir_btn = ctk.CTkButton(
            self.acoes_frame, 
            text="Excluir", 
            fg_color="red", 
            hover_color="darkred",
            command=self.excluir_produto_selecionado
        )
        self.excluir_btn.pack(side="left", padx=5, pady=5)
        
        self.movimentar_btn = ctk.CTkButton(
            self.acoes_frame, 
            text="Movimentar Estoque", 
            command=self.abrir_form_movimentacao
        )
        self.movimentar_btn.pack(side="left", padx=5, pady=5)
        
        self.relatorio_btn = ctk.CTkButton(
            self.acoes_frame, 
            text="Gerar Relatório", 
            command=self.gerar_relatorio_estoque
        )
        self.relatorio_btn.pack(side="right", padx=5, pady=5)
        
        # Carrega os produtos inicialmente
        self.buscar_produtos()
    
    def setup_tab_movimentacoes(self):
        """Configura a aba de movimentações de estoque."""
        # Frame de filtros
        self.mov_filtros_frame = ctk.CTkFrame(self.tab_movimentacoes)
        self.mov_filtros_frame.pack(fill="x", padx=10, pady=5)
        
        # Filtro por produto
        self.mov_produto_label = ctk.CTkLabel(self.mov_filtros_frame, text="Produto:")
        self.mov_produto_label.pack(side="left", padx=5)
        
        self.mov_produto_var = ctk.StringVar()
        self.mov_produto_entry = ctk.CTkEntry(self.mov_filtros_frame, textvariable=self.mov_produto_var, width=200)
        self.mov_produto_entry.pack(side="left", padx=5)
        
        # Filtro por tipo
        self.mov_tipo_label = ctk.CTkLabel(self.mov_filtros_frame, text="Tipo:")
        self.mov_tipo_label.pack(side="left", padx=5)
        
        self.mov_tipo_var = ctk.StringVar(value="Todos")
        self.mov_tipo_combobox = ctk.CTkComboBox(
            self.mov_filtros_frame, 
            values=["Todos", "Entrada", "Saída", "Ajuste"],
            variable=self.mov_tipo_var,
            width=120
        )
        self.mov_tipo_combobox.pack(side="left", padx=5)
        
        # Filtro por data
        self.mov_data_label = ctk.CTkLabel(self.mov_filtros_frame, text="Data:")
        self.mov_data_label.pack(side="left", padx=5)
        
        self.mov_data_inicio_var = ctk.StringVar(value=datetime.datetime.now().strftime("%d/%m/%Y"))
        self.mov_data_inicio_entry = ctk.CTkEntry(self.mov_filtros_frame, textvariable=self.mov_data_inicio_var, width=100)
        self.mov_data_inicio_entry.pack(side="left", padx=5)
        
        self.mov_data_fim_label = ctk.CTkLabel(self.mov_filtros_frame, text="até")
        self.mov_data_fim_label.pack(side="left")
        
        self.mov_data_fim_var = ctk.StringVar(value=datetime.datetime.now().strftime("%d/%m/%Y"))
        self.mov_data_fim_entry = ctk.CTkEntry(self.mov_filtros_frame, textvariable=self.mov_data_fim_var, width=100)
        self.mov_data_fim_entry.pack(side="left", padx=5)
        
        # Botão de busca
        self.mov_buscar_btn = ctk.CTkButton(
            self.mov_filtros_frame, 
            text="Buscar", 
            command=self.buscar_movimentacoes
        )
        self.mov_buscar_btn.pack(side="left", padx=5)
        
        # Botão para adicionar movimentação
        self.mov_adicionar_btn = ctk.CTkButton(
            self.mov_filtros_frame, 
            text="Nova Movimentação", 
            command=self.abrir_form_movimentacao
        )
        self.mov_adicionar_btn.pack(side="right", padx=5)
        
        # Frame para a tabela de movimentações
        self.movimentacoes_frame = ctk.CTkFrame(self.tab_movimentacoes)
        self.movimentacoes_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Tabela de movimentações
        self.movimentacoes_tree = ttk.Treeview(
            self.movimentacoes_frame,
            columns=("data", "produto", "tipo", "quantidade", "motivo", "usuario"),
            show="headings"
        )
        
        # Define as colunas
        self.movimentacoes_tree.heading("data", text="Data/Hora")
        self.movimentacoes_tree.heading("produto", text="Produto")
        self.movimentacoes_tree.heading("tipo", text="Tipo")
        self.movimentacoes_tree.heading("quantidade", text="Quantidade")
        self.movimentacoes_tree.heading("motivo", text="Motivo")
        self.movimentacoes_tree.heading("usuario", text="Usuário")
        
        self.movimentacoes_tree.column("data", width=150)
        self.movimentacoes_tree.column("produto", width=250)
        self.movimentacoes_tree.column("tipo", width=100)
        self.movimentacoes_tree.column("quantidade", width=100)
        self.movimentacoes_tree.column("motivo", width=200)
        self.movimentacoes_tree.column("usuario", width=150)
        
        # Adiciona barra de rolagem
        self.movimentacoes_scrollbar = ctk.CTkScrollbar(self.movimentacoes_frame, command=self.movimentacoes_tree.yview)
        self.movimentacoes_scrollbar.pack(side="right", fill="y")
        self.movimentacoes_tree.configure(yscrollcommand=self.movimentacoes_scrollbar.set)
        
        self.movimentacoes_tree.pack(fill="both", expand=True)
        
        # Carrega as movimentações inicialmente
        self.buscar_movimentacoes()
    
    def setup_tab_categorias(self):
        """Configura a aba de categorias."""
        # Frame esquerdo - lista de categorias
        self.cat_lista_frame = ctk.CTkFrame(self.tab_categorias)
        self.cat_lista_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Título
        self.cat_lista_label = ctk.CTkLabel(
            self.cat_lista_frame, 
            text="Categorias", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.cat_lista_label.pack(pady=5)
        
        # Lista de categorias
        self.categorias_tree = ttk.Treeview(
            self.cat_lista_frame,
            columns=("nome", "descricao"),
            show="headings"
        )
        
        self.categorias_tree.heading("nome", text="Nome")
        self.categorias_tree.heading("descricao", text="Descrição")
        
        self.categorias_tree.column("nome", width=150)
        self.categorias_tree.column("descricao", width=300)
        
        # Adiciona barra de rolagem
        self.categorias_scrollbar = ctk.CTkScrollbar(self.cat_lista_frame, command=self.categorias_tree.yview)
        self.categorias_scrollbar.pack(side="right", fill="y")
        self.categorias_tree.configure(yscrollcommand=self.categorias_scrollbar.set)
        
        self.categorias_tree.pack(fill="both", expand=True, pady=5)
        
        # Evento de seleção
        self.categorias_tree.bind("<<TreeviewSelect>>", self.selecionar_categoria)
        
        # Frame direito - formulário de categoria
        self.cat_form_frame = ctk.CTkFrame(self.tab_categorias)
        self.cat_form_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Título
        self.cat_form_label = ctk.CTkLabel(
            self.cat_form_frame, 
            text="Nova Categoria", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.cat_form_label.pack(pady=5)
        
        # Formulário
        self.cat_nome_label = ctk.CTkLabel(self.cat_form_frame, text="Nome:")
        self.cat_nome_label.pack(anchor="w", padx=10, pady=5)
        
        self.cat_nome_var = ctk.StringVar()
        self.cat_nome_entry = ctk.CTkEntry(self.cat_form_frame, textvariable=self.cat_nome_var, width=300)
        self.cat_nome_entry.pack(fill="x", padx=10, pady=5)
        
        self.cat_descricao_label = ctk.CTkLabel(self.cat_form_frame, text="Descrição:")
        self.cat_descricao_label.pack(anchor="w", padx=10, pady=5)
        
        self.cat_descricao_var = ctk.StringVar()
        self.cat_descricao_entry = ctk.CTkEntry(self.cat_form_frame, textvariable=self.cat_descricao_var, width=300)
        self.cat_descricao_entry.pack(fill="x", padx=10, pady=5)
        
        # Botões
        self.cat_botoes_frame = ctk.CTkFrame(self.cat_form_frame, fg_color="transparent")
        self.cat_botoes_frame.pack(fill="x", padx=10, pady=10)
        
        self.cat_novo_btn = ctk.CTkButton(
            self.cat_botoes_frame, 
            text="Nova", 
            command=self.nova_categoria
        )
        self.cat_novo_btn.pack(side="left", padx=5)
        
        self.cat_salvar_btn = ctk.CTkButton(
            self.cat_botoes_frame, 
            text="Salvar", 
            command=self.salvar_categoria
        )
        self.cat_salvar_btn.pack(side="left", padx=5)
        
        self.cat_excluir_btn = ctk.CTkButton(
            self.cat_botoes_frame, 
            text="Excluir", 
            fg_color="red", 
            hover_color="darkred",
            command=self.excluir_categoria
        )
        self.cat_excluir_btn.pack(side="right", padx=5)
        
        # Carrega as categorias
        self.carregar_categorias()
        
        # Inicializa o ID da categoria selecionada
        self.categoria_selecionada_id = None
    
    def setup_tab_fornecedores(self):
        """Configura a aba de fornecedores."""
        # Frame esquerdo - lista de fornecedores
        self.forn_lista_frame = ctk.CTkFrame(self.tab_fornecedores)
        self.forn_lista_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Título
        self.forn_lista_label = ctk.CTkLabel(
            self.forn_lista_frame, 
            text="Fornecedores", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.forn_lista_label.pack(pady=5)
        
        # Lista de fornecedores
        self.fornecedores_tree = ttk.Treeview(
            self.forn_lista_frame,
            columns=("nome", "cnpj", "telefone"),
            show="headings"
        )
        
        self.fornecedores_tree.heading("nome", text="Nome")
        self.fornecedores_tree.heading("cnpj", text="CNPJ")
        self.fornecedores_tree.heading("telefone", text="Telefone")
        
        self.fornecedores_tree.column("nome", width=200)
        self.fornecedores_tree.column("cnpj", width=150)
        self.fornecedores_tree.column("telefone", width=150)
        
        # Adiciona barra de rolagem
        self.fornecedores_scrollbar = ctk.CTkScrollbar(self.forn_lista_frame, command=self.fornecedores_tree.yview)
        self.fornecedores_scrollbar.pack(side="right", fill="y")
        self.fornecedores_tree.configure(yscrollcommand=self.fornecedores_scrollbar.set)
        
        self.fornecedores_tree.pack(fill="both", expand=True, pady=5)
        
        # Evento de seleção
        self.fornecedores_tree.bind("<<TreeviewSelect>>", self.selecionar_fornecedor)
        
        # Frame direito - formulário de fornecedor
        self.forn_form_frame = ctk.CTkFrame(self.tab_fornecedores)
        self.forn_form_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Título
        self.forn_form_label = ctk.CTkLabel(
            self.forn_form_frame, 
            text="Novo Fornecedor", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.forn_form_label.pack(pady=5)
        
        # Formulário
        self.forn_nome_label = ctk.CTkLabel(self.forn_form_frame, text="Nome:")
        self.forn_nome_label.pack(anchor="w", padx=10, pady=5)
        
        self.forn_nome_var = ctk.StringVar()
        self.forn_nome_entry = ctk.CTkEntry(self.forn_form_frame, textvariable=self.forn_nome_var, width=300)
        self.forn_nome_entry.pack(fill="x", padx=10, pady=5)
        
        self.forn_cnpj_label = ctk.CTkLabel(self.forn_form_frame, text="CNPJ:")
        self.forn_cnpj_label.pack(anchor="w", padx=10, pady=5)
        
        self.forn_cnpj_var = ctk.StringVar()
        self.forn_cnpj_entry = ctk.CTkEntry(self.forn_form_frame, textvariable=self.forn_cnpj_var, width=300)
        self.forn_cnpj_entry.pack(fill="x", padx=10, pady=5)
        
        self.forn_endereco_label = ctk.CTkLabel(self.forn_form_frame, text="Endereço:")
        self.forn_endereco_label.pack(anchor="w", padx=10, pady=5)
        
        self.forn_endereco_var = ctk.StringVar()
        self.forn_endereco_entry = ctk.CTkEntry(self.forn_form_frame, textvariable=self.forn_endereco_var, width=300)
        self.forn_endereco_entry.pack(fill="x", padx=10, pady=5)
        
        self.forn_telefone_label = ctk.CTkLabel(self.forn_form_frame, text="Telefone:")
        self.forn_telefone_label.pack(anchor="w", padx=10, pady=5)
        
        self.forn_telefone_var = ctk.StringVar()
        self.forn_telefone_entry = ctk.CTkEntry(self.forn_form_frame, textvariable=self.forn_telefone_var, width=300)
        self.forn_telefone_entry.pack(fill="x", padx=10, pady=5)
        
        self.forn_email_label = ctk.CTkLabel(self.forn_form_frame, text="Email:")
        self.forn_email_label.pack(anchor="w", padx=10, pady=5)
        
        self.forn_email_var = ctk.StringVar()
        self.forn_email_entry = ctk.CTkEntry(self.forn_form_frame, textvariable=self.forn_email_var, width=300)
        self.forn_email_entry.pack(fill="x", padx=10, pady=5)
        
        self.forn_contato_label = ctk.CTkLabel(self.forn_form_frame, text="Contato:")
        self.forn_contato_label.pack(anchor="w", padx=10, pady=5)
        
        self.forn_contato_var = ctk.StringVar()
        self.forn_contato_entry = ctk.CTkEntry(self.forn_form_frame, textvariable=self.forn_contato_var, width=300)
        self.forn_contato_entry.pack(fill="x", padx=10, pady=5)
        
        # Botões
        self.forn_botoes_frame = ctk.CTkFrame(self.forn_form_frame, fg_color="transparent")
        self.forn_botoes_frame.pack(fill="x", padx=10, pady=10)
        
        self.forn_novo_btn = ctk.CTkButton(
            self.forn_botoes_frame, 
            text="Novo", 
            command=self.novo_fornecedor
        )
        self.forn_novo_btn.pack(side="left", padx=5)
        
        self.forn_salvar_btn = ctk.CTkButton(
            self.forn_botoes_frame, 
            text="Salvar", 
            command=self.salvar_fornecedor
        )
        self.forn_salvar_btn.pack(side="left", padx=5)
        
        self.forn_excluir_btn = ctk.CTkButton(
            self.forn_botoes_frame, 
            text="Excluir", 
            fg_color="red", 
            hover_color="darkred",
            command=self.excluir_fornecedor
        )
        self.forn_excluir_btn.pack(side="right", padx=5)
        
        # Carrega os fornecedores
        self.carregar_fornecedores()
        
        # Inicializa o ID do fornecedor selecionado
        self.fornecedor_selecionado_id = None
    
    # Métodos para a aba de produtos
    def buscar_produtos(self):
        """Busca produtos com base nos filtros aplicados."""
        filtro = self.filtro_var.get()
        categoria = self.categoria_var.get()
        
        # Obtém o ID da categoria selecionada
        categoria_id = None
        if categoria != "Todas":
            for cat in self.categorias:
                if cat["nome"] == categoria:
                    categoria_id = cat["id"]
                    break
        
        # Busca os produtos
        produtos = self.controller.listar_produtos(filtro=filtro, categoria_id=categoria_id)
        
        # Limpa a tabela
        for item in self.produtos_tree.get_children():
            self.produtos_tree.delete(item)
        
        # Preenche a tabela com os produtos
        for produto in produtos:
            self.produtos_tree.insert(
                "", "end", 
                values=(
                    produto["codigo"],
                    produto["nome"],
                    produto["categoria_nome"] or "Sem categoria",
                    f"R$ {produto['preco_venda']:.2f}",
                    produto["estoque_atual"],
                    produto["estoque_minimo"]
                ),
                tags=(str(produto["id"]),)
            )
    
    def editar_produto_selecionado(self, event=None):
        """Abre o formulário para editar o produto selecionado."""
        selection = self.produtos_tree.selection()
        if not selection:
            messagebox.showinfo("Aviso", "Selecione um produto para editar.")
            return
        
        # Obtém o ID do produto a partir das tags
        produto_id = int(self.produtos_tree.item(selection[0], "tags")[0])
        self.abrir_form_produto(produto_id)
    
    def excluir_produto_selecionado(self):
        """Exclui o produto selecionado."""
        selection = self.produtos_tree.selection()
        if not selection:
            messagebox.showinfo("Aviso", "Selecione um produto para excluir.")
            return
        
        # Confirmação
        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este produto?"):
            return
        
        # Obtém o ID do produto a partir das tags
        produto_id = int(self.produtos_tree.item(selection[0], "tags")[0])
        
        # Tenta excluir o produto
        resultado = self.controller.excluir_produto(produto_id)
        
        if isinstance(resultado, dict) and "erro" in resultado:
            messagebox.showerror("Erro", resultado["erro"])
        elif resultado:
            messagebox.showinfo("Sucesso", "Produto excluído com sucesso.")
            self.buscar_produtos()
        else:
            messagebox.showerror("Erro", "Não foi possível excluir o produto.")
    
    def abrir_form_produto(self, produto_id=None):
        """Abre o formulário para adicionar ou editar um produto."""
        # Cria uma nova janela
        produto_window = ctk.CTkToplevel(self.parent)
        produto_window.title("Novo Produto" if not produto_id else "Editar Produto")
        produto_window.geometry("600x650")
        produto_window.grab_set()  # Torna a janela modal
        
        # Título
        title_label = ctk.CTkLabel(
            produto_window, 
            text="CADASTRO DE PRODUTO", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Frame principal
        main_frame = ctk.CTkScrollableFrame(produto_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Formulário
        # Código
        codigo_label = ctk.CTkLabel(main_frame, text="Código:")
        codigo_label.pack(anchor="w", padx=10, pady=5)
        
        codigo_var = ctk.StringVar()
        codigo_entry = ctk.CTkEntry(main_frame, textvariable=codigo_var, width=300)
        codigo_entry.pack(fill="x", padx=10, pady=5)
        
        # Nome
        nome_label = ctk.CTkLabel(main_frame, text="Nome:")
        nome_label.pack(anchor="w", padx=10, pady=5)
        
        nome_var = ctk.StringVar()
        nome_entry = ctk.CTkEntry(main_frame, textvariable=nome_var, width=300)
        nome_entry.pack(fill="x", padx=10, pady=5)
        
        # Descrição
        descricao_label = ctk.CTkLabel(main_frame, text="Descrição:")
        descricao_label.pack(anchor="w", padx=10, pady=5)
        
        descricao_var = ctk.StringVar()
        descricao_entry = ctk.CTkEntry(main_frame, textvariable=descricao_var, width=300)
        descricao_entry.pack(fill="x", padx=10, pady=5)
        
        # Categoria
        categoria_label = ctk.CTkLabel(main_frame, text="Categoria:")
        categoria_label.pack(anchor="w", padx=10, pady=5)
        
        categorias = self.controller.listar_categorias()
        categoria_options = [f"{cat['id']} - {cat['nome']}" for cat in categorias]
        
        categoria_var = ctk.StringVar()
        categoria_combobox = ctk.CTkComboBox(
            main_frame, 
            values=categoria_options,
            variable=categoria_var,
            width=300
        )
        categoria_combobox.pack(fill="x", padx=10, pady=5)
        
        # Fornecedor
        fornecedor_label = ctk.CTkLabel(main_frame, text="Fornecedor:")
        fornecedor_label.pack(anchor="w", padx=10, pady=5)
        
        fornecedores = self.controller.listar_fornecedores()
        fornecedor_options = [f"{forn['id']} - {forn['nome']}" for forn in fornecedores]
        
        fornecedor_var = ctk.StringVar()
        fornecedor_combobox = ctk.CTkComboBox(
            main_frame, 
            values=fornecedor_options,
            variable=fornecedor_var,
            width=300
        )
        fornecedor_combobox.pack(fill="x", padx=10, pady=5)
        
        # Preço de custo
        preco_custo_label = ctk.CTkLabel(main_frame, text="Preço de Custo (R$):")
        preco_custo_label.pack(anchor="w", padx=10, pady=5)
        
        preco_custo_var = ctk.StringVar()
        preco_custo_entry = NumericEntry(main_frame, decimal=True, textvariable=preco_custo_var, width=300)
        preco_custo_entry.pack(fill="x", padx=10, pady=5)
        
        # Preço de venda
        preco_venda_label = ctk.CTkLabel(main_frame, text="Preço de Venda (R$):")
        preco_venda_label.pack(anchor="w", padx=10, pady=5)
        
        preco_venda_var = ctk.StringVar()
        preco_venda_entry = NumericEntry(main_frame, decimal=True, textvariable=preco_venda_var, width=300)
        preco_venda_entry.pack(fill="x", padx=10, pady=5)
        
        # Estoque atual
        estoque_atual_label = ctk.CTkLabel(main_frame, text="Estoque Atual:")
        estoque_atual_label.pack(anchor="w", padx=10, pady=5)
        
        estoque_atual_var = ctk.StringVar()
        estoque_atual_entry = NumericEntry(main_frame, textvariable=estoque_atual_var, width=300)
        estoque_atual_entry.pack(fill="x", padx=10, pady=5)
        
        # Estoque mínimo
        estoque_minimo_label = ctk.CTkLabel(main_frame, text="Estoque Mínimo:")
        estoque_minimo_label.pack(anchor="w", padx=10, pady=5)
        
        estoque_minimo_var = ctk.StringVar()
        estoque_minimo_entry = NumericEntry(main_frame, textvariable=estoque_minimo_var, width=300)
        estoque_minimo_entry.pack(fill="x", padx=10, pady=5)
        
        # Unidade
        unidade_label = ctk.CTkLabel(main_frame, text="Unidade:")
        unidade_label.pack(anchor="w", padx=10, pady=5)
        
        unidade_var = ctk.StringVar(value="UN")
        unidade_entry = ctk.CTkEntry(main_frame, textvariable=unidade_var, width=300)
        unidade_entry.pack(fill="x", padx=10, pady=5)
        
        # Localização
        localizacao_label = ctk.CTkLabel(main_frame, text="Localização:")
        localizacao_label.pack(anchor="w", padx=10, pady=5)
        
        localizacao_var = ctk.StringVar()
        localizacao_entry = ctk.CTkEntry(main_frame, textvariable=localizacao_var, width=300)
        localizacao_entry.pack(fill="x", padx=10, pady=5)
        
        # Código de barras
        codigo_barras_label = ctk.CTkLabel(main_frame, text="Código de Barras:")
        codigo_barras_label.pack(anchor="w", padx=10, pady=5)
        
        codigo_barras_var = ctk.StringVar()
        codigo_barras_entry = ctk.CTkEntry(main_frame, textvariable=codigo_barras_var, width=300)
        codigo_barras_entry.pack(fill="x", padx=10, pady=5)
        
        # Frame de botões
        botoes_frame = ctk.CTkFrame(produto_window, fg_color="transparent")
        botoes_frame.pack(fill="x", padx=20, pady=20)
        
        # Se estiver editando, carrega os dados do produto
        if produto_id:
            produto = self.controller.obter_produto(produto_id)
            if produto:
                codigo_var.set(produto["codigo"])
                nome_var.set(produto["nome"])
                descricao_var.set(produto["descricao"] or "")
                
                # Seleciona a categoria
                if produto["categoria_id"]:
                    for i, cat in enumerate(categorias):
                        if cat["id"] == produto["categoria_id"]:
                            categoria_combobox.set(categoria_options[i])
                            break
                
                # Seleciona o fornecedor
                if produto["fornecedor_id"]:
                    for i, forn in enumerate(fornecedores):
                        if forn["id"] == produto["fornecedor_id"]:
                            fornecedor_combobox.set(fornecedor_options[i])
                            break
                
                preco_custo_var.set(str(produto["preco_custo"]))
                preco_venda_var.set(str(produto["preco_venda"]))
                estoque_atual_var.set(str(produto["estoque_atual"]))
                estoque_minimo_var.set(str(produto["estoque_minimo"]))
                unidade_var.set(produto["unidade"] or "UN")
                localizacao_var.set(produto["localizacao"] or "")
                codigo_barras_var.set(produto["codigo_barras"] or "")
        
        # Função para salvar o produto
        def salvar():
            # Validação básica
            if not codigo_var.get() or not nome_var.get():
                messagebox.showerror("Erro", "Código e Nome são campos obrigatórios.")
                return
            
            try:
                preco_custo = float(preco_custo_var.get() or 0)
                preco_venda = float(preco_venda_var.get() or 0)
                estoque_atual = int(estoque_atual_var.get() or 0)
                estoque_minimo = int(estoque_minimo_var.get() or 0)
            except ValueError:
                messagebox.showerror("Erro", "Valores numéricos inválidos.")
                return
            
            # Prepara os dados do produto
            produto_data = {
                "codigo": codigo_var.get(),
                "nome": nome_var.get(),
                "descricao": descricao_var.get(),
                "preco_custo": preco_custo,
                "preco_venda": preco_venda,
                "estoque_atual": estoque_atual,
                "estoque_minimo": estoque_minimo,
                "unidade": unidade_var.get(),
                "localizacao": localizacao_var.get(),
                "codigo_barras": codigo_barras_var.get()
            }
            
            # Extrai os IDs da categoria e fornecedor selecionados
            if categoria_var.get():
                try:
                    categoria_id = int(categoria_var.get().split(" - ")[0])
                    produto_data["categoria_id"] = categoria_id
                except (ValueError, IndexError):
                    pass
            
            if fornecedor_var.get():
                try:
                    fornecedor_id = int(fornecedor_var.get().split(" - ")[0])
                    produto_data["fornecedor_id"] = fornecedor_id
                except (ValueError, IndexError):
                    pass
            
            # Salva o produto
            if produto_id:
                produto_data["id"] = produto_id
                resultado = self.controller.atualizar_produto(produto_data)
                mensagem = "Produto atualizado com sucesso!"
            else:
                resultado = self.controller.adicionar_produto(produto_data)
                mensagem = "Produto adicionado com sucesso!"
            
            if isinstance(resultado, dict) and "erro" in resultado:
                messagebox.showerror("Erro", resultado["erro"])
            elif resultado:
                messagebox.showinfo("Sucesso", mensagem)
                produto_window.destroy()
                self.buscar_produtos()
            else:
                messagebox.showerror("Erro", "Não foi possível salvar o produto.")
        
        # Botões de salvar e cancelar
        salvar_btn = ctk.CTkButton(
            botoes_frame, 
            text="Salvar", 
            command=salvar
        )
        salvar_btn.pack(side="left", padx=5)
        
        cancelar_btn = ctk.CTkButton(
            botoes_frame, 
            text="Cancelar", 
            command=produto_window.destroy
        )
        cancelar_btn.pack(side="right", padx=5)
    
    def abrir_form_movimentacao(self, produto_id=None):
        """Abre o formulário para adicionar uma movimentação de estoque."""
        # Cria uma nova janela
        mov_window = ctk.CTkToplevel(self.parent)
        mov_window.title("Movimentação de Estoque")
        mov_window.geometry("500x400")
        mov_window.grab_set()  # Torna a janela modal
        
        # Título
        title_label = ctk.CTkLabel(
            mov_window, 
            text="MOVIMENTAÇÃO DE ESTOQUE", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Frame principal
        main_frame = ctk.CTkFrame(mov_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Formulário
        # Produto
        produto_label = ctk.CTkLabel(main_frame, text="Produto:")
        produto_label.pack(anchor="w", padx=10, pady=5)
        
        produtos = self.controller.listar_produtos()
        produto_options = [f"{p['id']} - {p['codigo']} - {p['nome']}" for p in produtos]
        
        produto_var = ctk.StringVar()
        produto_combobox = SearchableComboBox(
            main_frame, 
            values=produto_options,
            variable=produto_var,
            width=300
        )
        produto_combobox.pack(fill="x", padx=10, pady=5)
        
        # Se um produto foi pré-selecionado
        if produto_id:
            for i, p in enumerate(produtos):
                if p["id"] == produto_id:
                    produto_combobox.set(produto_options[i])
                    break
        
        # Tipo de movimentação
        tipo_label = ctk.CTkLabel(main_frame, text="Tipo de Movimentação:")
        tipo_label.pack(anchor="w", padx=10, pady=5)
        
        tipo_var = ctk.StringVar(value="Entrada")
        tipo_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        tipo_frame.pack(fill="x", padx=10, pady=5)
        
        entrada_radio = ctk.CTkRadioButton(
            tipo_frame, 
            text="Entrada", 
            variable=tipo_var, 
            value="Entrada"
        )
        entrada_radio.pack(side="left", padx=10)
        
        saida_radio = ctk.CTkRadioButton(
            tipo_frame, 
            text="Saída", 
            variable=tipo_var, 
            value="Saída"
        )
        saida_radio.pack(side="left", padx=10)
        
        ajuste_radio = ctk.CTkRadioButton(
            tipo_frame, 
            text="Ajuste", 
            variable=tipo_var, 
            value="Ajuste"
        )
        ajuste_radio.pack(side="left", padx=10)
        # Quantidade
        quantidade_label = ctk.CTkLabel(main_frame, text="Quantidade:")
        quantidade_label.pack(anchor="w", padx=10, pady=5)
        
        quantidade_var = ctk.StringVar(value="1")
        quantidade_entry = NumericEntry(main_frame, textvariable=quantidade_var, width=300)
        quantidade_entry.pack(fill="x", padx=10, pady=5)
        
        # Motivo
        motivo_label = ctk.CTkLabel(main_frame, text="Motivo:")
        motivo_label.pack(anchor="w", padx=10, pady=5)
        
        motivo_var = ctk.StringVar()
        motivo_entry = ctk.CTkEntry(main_frame, textvariable=motivo_var, width=300)
        motivo_entry.pack(fill="x", padx=10, pady=5)
        
        # Frame de botões
        botoes_frame = ctk.CTkFrame(mov_window, fg_color="transparent")
        botoes_frame.pack(fill="x", padx=20, pady=20)
        
        # Função para salvar a movimentação
        def salvar():
            # Validação básica
            if not produto_var.get() or not quantidade_var.get():
                messagebox.showerror("Erro", "Produto e Quantidade são campos obrigatórios.")
                return
            
            try:
                # Extrai o ID do produto
                produto_id = int(produto_var.get().split(" - ")[0])
                quantidade = int(quantidade_var.get())
                
                if quantidade <= 0:
                    messagebox.showerror("Erro", "A quantidade deve ser maior que zero.")
                    return
                
                # Prepara os dados da movimentação
                movimentacao_data = {
                    "produto_id": produto_id,
                    "tipo": tipo_var.get(),
                    "quantidade": quantidade,
                    "motivo": motivo_var.get(),
                    "usuario_id": 1  # ID do usuário logado (a ser implementado)
                }
                
                # Salva a movimentação
                resultado = self.controller.adicionar_movimentacao(movimentacao_data)
                
                if isinstance(resultado, dict) and "erro" in resultado:
                    messagebox.showerror("Erro", resultado["erro"])
                elif resultado:
                    messagebox.showinfo("Sucesso", "Movimentação registrada com sucesso!")
                    mov_window.destroy()
                    self.buscar_movimentacoes()
                    self.buscar_produtos()  # Atualiza a lista de produtos
                else:
                    messagebox.showerror("Erro", "Não foi possível registrar a movimentação.")
                    
            except (ValueError, IndexError):
                messagebox.showerror("Erro", "Selecione um produto válido.")
        
        # Botões de salvar e cancelar
        salvar_btn = ctk.CTkButton(
            botoes_frame, 
            text="Salvar", 
            command=salvar
        )
        salvar_btn.pack(side="left", padx=5)
        
        cancelar_btn = ctk.CTkButton(
            botoes_frame, 
            text="Cancelar", 
            command=mov_window.destroy
        )
        cancelar_btn.pack(side="right", padx=5)
    
    def gerar_relatorio_estoque(self):
        """Gera um relatório de estoque."""
        # Cria uma nova janela
        relatorio_window = ctk.CTkToplevel(self.parent)
        relatorio_window.title("Relatório de Estoque")
        relatorio_window.geometry("800x600")
        relatorio_window.grab_set()  # Torna a janela modal
        
        # Título
        title_label = ctk.CTkLabel(
            relatorio_window, 
            text="RELATÓRIO DE ESTOQUE", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Frame de filtros
        filtros_frame = ctk.CTkFrame(relatorio_window)
        filtros_frame.pack(fill="x", padx=20, pady=10)
        
        # Filtro por categoria
        categoria_label = ctk.CTkLabel(filtros_frame, text="Categoria:")
        categoria_label.pack(side="left", padx=5)
        
        categorias = self.controller.listar_categorias()
        categoria_options = ["Todas"] + [cat["nome"] for cat in categorias]
        
        categoria_var = ctk.StringVar(value="Todas")
        categoria_combobox = ctk.CTkComboBox(
            filtros_frame, 
            values=categoria_options,
            variable=categoria_var,
            width=150
        )
        categoria_combobox.pack(side="left", padx=5)
        
        # Filtro por estoque baixo
        estoque_baixo_var = ctk.BooleanVar(value=False)
        estoque_baixo_check = ctk.CTkCheckBox(
            filtros_frame, 
            text="Apenas produtos com estoque baixo", 
            variable=estoque_baixo_var
        )
        estoque_baixo_check.pack(side="left", padx=20)
        
        # Botão para gerar relatório
        gerar_btn = ctk.CTkButton(
            filtros_frame, 
            text="Gerar Relatório", 
            command=lambda: gerar_relatorio()
        )
        gerar_btn.pack(side="right", padx=5)
        
        # Frame para o relatório
        relatorio_frame = ctk.CTkFrame(relatorio_window)
        relatorio_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Função para gerar o relatório
        def gerar_relatorio():
            # Limpa o frame do relatório
            for widget in relatorio_frame.winfo_children():
                widget.destroy()
            
            # Obtém o ID da categoria selecionada
            categoria_id = None
            if categoria_var.get() != "Todas":
                for cat in categorias:
                    if cat["nome"] == categoria_var.get():
                        categoria_id = cat["id"]
                        break
            
            # Gera o relatório
            relatorio = self.controller.gerar_relatorio_estoque(
                categoria_id=categoria_id,
                estoque_baixo=estoque_baixo_var.get()
            )
            
            # Exibe o relatório
            # Cabeçalho
            info_frame = ctk.CTkFrame(relatorio_frame)
            info_frame.pack(fill="x", pady=10)
            
            # Data do relatório
            data_label = ctk.CTkLabel(
                info_frame, 
                text=f"Data do Relatório: {relatorio['data_geracao']}"
            )
            data_label.pack(anchor="w", padx=10, pady=2)
            
            # Total de produtos
            total_label = ctk.CTkLabel(
                info_frame, 
                text=f"Total de Produtos: {relatorio['total_produtos']}"
            )
            total_label.pack(anchor="w", padx=10, pady=2)
            
            # Produtos com estoque baixo
            baixo_label = ctk.CTkLabel(
                info_frame, 
                text=f"Produtos com Estoque Baixo: {relatorio['produtos_baixo_estoque']}"
            )
            baixo_label.pack(anchor="w", padx=10, pady=2)
            
            # Valor total em estoque
            valor_label = ctk.CTkLabel(
                info_frame, 
                text=f"Valor Total em Estoque: R$ {relatorio['valor_total_estoque']:.2f}"
            )
            valor_label.pack(anchor="w", padx=10, pady=2)
            
            # Tabela de produtos
            tabela_frame = ctk.CTkFrame(relatorio_frame)
            tabela_frame.pack(fill="both", expand=True, pady=10)
            
            produtos_tree = ttk.Treeview(
                tabela_frame,
                columns=("codigo", "nome", "categoria", "estoque", "minimo", "custo", "valor"),
                show="headings"
            )
            
            produtos_tree.heading("codigo", text="Código")
            produtos_tree.heading("nome", text="Nome")
            produtos_tree.heading("categoria", text="Categoria")
            produtos_tree.heading("estoque", text="Estoque Atual")
            produtos_tree.heading("minimo", text="Estoque Mínimo")
            produtos_tree.heading("custo", text="Custo Unitário")
            produtos_tree.heading("valor", text="Valor Total")
            
            produtos_tree.column("codigo", width=80)
            produtos_tree.column("nome", width=200)
            produtos_tree.column("categoria", width=120)
            produtos_tree.column("estoque", width=100)
            produtos_tree.column("minimo", width=100)
            produtos_tree.column("custo", width=100)
            produtos_tree.column("valor", width=100)
            
            # Adiciona barra de rolagem
            produtos_scrollbar = ctk.CTkScrollbar(tabela_frame, command=produtos_tree.yview)
            produtos_scrollbar.pack(side="right", fill="y")
            produtos_tree.configure(yscrollcommand=produtos_scrollbar.set)
            
            produtos_tree.pack(fill="both", expand=True)
            
            # Preenche a tabela com os produtos
            for produto in relatorio["produtos"]:
                produtos_tree.insert(
                    "", "end", 
                    values=(
                        produto["codigo"],
                        produto["nome"],
                        produto["categoria_nome"] or "Sem categoria",
                        produto["estoque_atual"],
                        produto["estoque_minimo"],
                        f"R$ {produto['preco_custo']:.2f}",
                        f"R$ {produto['valor_total']:.2f}"
                    )
                )
            
            # Botões de ação
            botoes_frame = ctk.CTkFrame(relatorio_window, fg_color="transparent")
            botoes_frame.pack(fill="x", padx=20, pady=10)
            
            # Botão para exportar
            exportar_btn = ctk.CTkButton(
                botoes_frame, 
                text="Exportar para CSV", 
                command=lambda: self.exportar_relatorio_csv(relatorio)
            )
            exportar_btn.pack(side="left", padx=5)
            
            # Botão para imprimir
            imprimir_btn = ctk.CTkButton(
                botoes_frame, 
                text="Imprimir", 
                command=lambda: self.imprimir_relatorio(relatorio)
            )
            imprimir_btn.pack(side="left", padx=5)
            
            # Botão para fechar
            fechar_btn = ctk.CTkButton(
                botoes_frame, 
                text="Fechar", 
                command=relatorio_window.destroy
            )
            fechar_btn.pack(side="right", padx=5)
        
        # Gera o relatório inicial
        gerar_relatorio()
    
    def exportar_relatorio_csv(self, relatorio):
        """Exporta o relatório para um arquivo CSV."""
        try:
            from tkinter import filedialog
            import csv
            import os
            
            # Solicita o local para salvar o arquivo
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Salvar Relatório"
            )
            
            if not filename:
                return
            
            # Escreve o arquivo CSV
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Cabeçalho
                writer.writerow([
                    "Data do Relatório", relatorio["data_geracao"]
                ])
                writer.writerow([
                    "Total de Produtos", relatorio["total_produtos"]
                ])
                writer.writerow([
                    "Produtos com Estoque Baixo", relatorio["produtos_baixo_estoque"]
                ])
                writer.writerow([
                    "Valor Total em Estoque", f"R$ {relatorio['valor_total_estoque']:.2f}"
                ])
                writer.writerow([])  # Linha em branco
                
                # Cabeçalho da tabela
                writer.writerow([
                    "Código", "Nome", "Categoria", "Estoque Atual", 
                    "Estoque Mínimo", "Custo Unitário", "Valor Total"
                ])
                
                # Dados dos produtos
                for produto in relatorio["produtos"]:
                    writer.writerow([
                        produto["codigo"],
                        produto["nome"],
                        produto["categoria_nome"] or "Sem categoria",
                        produto["estoque_atual"],
                        produto["estoque_minimo"],
                        f"R$ {produto['preco_custo']:.2f}",
                        f"R$ {produto['valor_total']:.2f}"
                    ])
            
            messagebox.showinfo("Sucesso", f"Relatório exportado com sucesso para {os.path.basename(filename)}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar relatório: {str(e)}")
    
    def imprimir_relatorio(self, relatorio):
        """Prepara o relatório para impressão."""
        messagebox.showinfo("Informação", "Funcionalidade de impressão a ser implementada.")
        # Aqui seria implementada a lógica de impressão
    
    # Métodos para a aba de fornecedores
    def carregar_fornecedores(self):
        """Carrega a lista de fornecedores."""
        # Busca os fornecedores
        fornecedores = self.controller.listar_fornecedores()
        
        # Limpa a tabela
        for item in self.fornecedores_tree.get_children():
            self.fornecedores_tree.delete(item)
        
        # Preenche a tabela com os fornecedores
        for forn in fornecedores:
            self.fornecedores_tree.insert(
                "", "end", 
                values=(forn["nome"], forn["cnpj"] or "", forn["telefone"] or ""),
                tags=(str(forn["id"]),)
            )
    
    def selecionar_fornecedor(self, event=None):
        """Seleciona um fornecedor da lista."""
        selection = self.fornecedores_tree.selection()
        if not selection:
            return
        
        # Obtém o ID do fornecedor a partir das tags
        fornecedor_id = int(self.fornecedores_tree.item(selection[0], "tags")[0])
        
        # Busca os dados do fornecedor
        fornecedor = self.controller.obter_fornecedor(fornecedor_id)