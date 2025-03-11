import customtkinter as ctk
from tkinter import ttk, messagebox
from ..utils.widgets import NumericEntry, SearchableComboBox

class ProdutosView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.setup_ui()
    
    def setup_ui(self):
        self.tab_produtos = self.parent
        
        # Frame de filtros
        self.filtros_frame = ctk.CTkFrame(self.tab_produtos)
        self.filtros_frame.pack(fill="x", padx=10, pady=5)
        
        # Filtro por nome/código
        self.filtro_label = ctk.CTkLabel(self.filtros_frame, text="Filtro:")
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
        from .produto_form import ProdutoForm
        ProdutoForm(self.parent, self.controller, produto_id, self.buscar_produtos)
    
    def abrir_form_movimentacao(self, produto_id=None):
        """Abre o formulário para adicionar uma movimentação de estoque."""
        from .movimentacao_form import MovimentacaoForm
        MovimentacaoForm(self.parent, self.controller, produto_id, self.buscar_produtos)
    
    def gerar_relatorio_estoque(self):
        """Gera um relatório de estoque."""
        from .relatorio_estoque import RelatorioEstoqueView
        RelatorioEstoqueView(self.parent, self.controller)