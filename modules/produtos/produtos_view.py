import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import os
from PIL import Image, ImageTk
import datetime
from .produto_form import ProdutoForm

class ProdutosView:
    def __init__(self, parent, controller=None):
        self.parent = parent
        self.controller = controller
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título com estilo
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="#1abc9c", corner_radius=10)
        title_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="GERENCIAMENTO DE PRODUTOS", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=10)
        
        # Frame de pesquisa
        search_frame = ctk.CTkFrame(self.main_frame)
        search_frame.pack(fill="x", padx=10, pady=10)
        
        search_label = ctk.CTkLabel(search_frame, text="Pesquisar:")
        search_label.pack(side="left", padx=5)
        
        self.pesquisa_var = ctk.StringVar()  # Renamed from search_var to pesquisa_var
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.pesquisa_var, width=300)
        search_entry.pack(side="left", padx=5)
        
        # Add categoria dropdown
        categoria_label = ctk.CTkLabel(search_frame, text="Categoria:")
        categoria_label.pack(side="left", padx=5)
        
        self.categoria_var = ctk.StringVar(value="Todas")
        categorias = ["Todas", "Eletrônicos", "Informática", "Acessórios", "Eletrodomésticos", "Móveis"]
        categoria_dropdown = ctk.CTkOptionMenu(search_frame, variable=self.categoria_var, values=categorias)
        categoria_dropdown.pack(side="left", padx=5)
        
        search_btn = ctk.CTkButton(
            search_frame, 
            text="Buscar", 
            command=self.buscar_produtos,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        search_btn.pack(side="left", padx=5)
        
        # Botões de ação
        actions_frame = ctk.CTkFrame(self.main_frame)
        actions_frame.pack(fill="x", padx=10, pady=10)
        
        novo_btn = ctk.CTkButton(
            actions_frame, 
            text="Novo Produto", 
            command=lambda: self.abrir_form_produto(),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        novo_btn.pack(side="left", padx=5)
        
        editar_btn = ctk.CTkButton(
            actions_frame, 
            text="Editar", 
            command=self.editar_produto,
            fg_color="#f39c12",
            hover_color="#d35400"
        )
        editar_btn.pack(side="left", padx=5)
        
        excluir_btn = ctk.CTkButton(
            actions_frame, 
            text="Excluir", 
            command=self.excluir_produto,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        excluir_btn.pack(side="left", padx=5)
        
        importar_btn = ctk.CTkButton(
            actions_frame, 
            text="Importar", 
            command=self.importar_produtos,
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        )
        importar_btn.pack(side="right", padx=5)
        
        exportar_btn = ctk.CTkButton(
            actions_frame, 
            text="Exportar", 
            command=self.exportar_produtos,
            fg_color="#34495e",
            hover_color="#2c3e50"
        )
        exportar_btn.pack(side="right", padx=5)
        
        # Frame para a tabela
        table_frame = ctk.CTkFrame(self.main_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tabela de produtos
        self.produtos_tree = ttk.Treeview(
            table_frame,
            columns=("codigo", "nome", "categoria", "preco", "estoque", "minimo"),
            show="headings"
        )
        
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
        scrollbar = ctk.CTkScrollbar(table_frame, command=self.produtos_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.produtos_tree.configure(yscrollcommand=scrollbar.set)
        
        self.produtos_tree.pack(fill="both", expand=True)
        
        # Bind para duplo clique na tabela
        self.produtos_tree.bind("<Double-1>", lambda event: self.editar_produto())
        
        # Carrega os produtos iniciais
        self.carregar_produtos()
    
    def carregar_produtos(self):
        """Carrega os produtos na tabela."""
        # Limpa a tabela
        for item in self.produtos_tree.get_children():
            self.produtos_tree.delete(item)
        
        # Obtém os filtros
        filtro = self.pesquisa_var.get() if hasattr(self, 'pesquisa_var') and self.pesquisa_var.get() else None
        categoria = self.categoria_var.get() if hasattr(self, 'categoria_var') and self.categoria_var.get() != "Todas" else None
        
        # Obtém os produtos do controller
        if self.controller:
            produtos = self.controller.listar_produtos(filtro, categoria)
            print(f"Carregando {len(produtos)} produtos na tabela.")
        else:
            # Dados de exemplo para testes
            produtos = self.obter_produtos_exemplo()
            print("Controlador não disponível, usando dados de exemplo.")
        
        # Preenche a tabela
        for produto in produtos:
            # Trata os valores para evitar erros
            codigo = produto.get('codigo', produto.get('codigo_barras', ''))
            nome = produto.get('nome', '')
            categoria = produto.get('categoria', '')
            
            # Trata o preço com mais cuidado
            try:
                preco_valor = produto.get('preco_venda', produto.get('preco', 0))
                preco = float(preco_valor) if preco_valor is not None else 0
            except (ValueError, TypeError):
                preco = 0
                
            # Trata o estoque com mais cuidado
            try:
                estoque_valor = produto.get('estoque_atual', produto.get('estoque', 0))
                estoque = int(estoque_valor) if estoque_valor is not None else 0
            except (ValueError, TypeError):
                estoque = 0
                
            # Trata o estoque mínimo
            try:
                estoque_min = int(produto.get('estoque_minimo', produto.get('minimo', 5)))
            except (ValueError, TypeError):
                estoque_min = 5
            
            # Insere na tabela
            self.produtos_tree.insert(
                "", "end", 
                values=(
                    codigo,
                    nome,
                    categoria,
                    f"R$ {preco:.2f}",
                    estoque,
                    estoque_min
                ),
                tags=(str(produto.get('id', '')),)
            )
    
    def buscar_produtos(self):
        """Busca produtos pelo termo de pesquisa."""
        termo = self.pesquisa_var.get().strip()  # Changed from search_var to pesquisa_var
        categoria = self.categoria_var.get() if self.categoria_var.get() != "Todas" else None
        
        # Limpa a tabela
        for item in self.produtos_tree.get_children():
            self.produtos_tree.delete(item)
        
        # Se não houver termo de busca, carrega todos os produtos
        if not termo and not categoria:
            self.carregar_produtos()
            return
        
        # Obtém os produtos filtrados
        if self.controller:
            produtos = self.controller.listar_produtos(termo, categoria)
        else:
            # Dados de exemplo para testes
            produtos = [p for p in self.obter_produtos_exemplo() 
                       if (not termo or termo.lower() in p["nome"].lower() or 
                          termo.lower() in p["codigo"].lower()) and
                          (not categoria or p["categoria"] == categoria)]
        
        # Preenche a tabela
        for produto in produtos:
            self.produtos_tree.insert(
                "", "end", 
                values=(
                    produto.get("codigo", ""),
                    produto.get("nome", ""),
                    produto.get("categoria", ""),
                    f"R$ {produto.get('preco', 0):.2f}",
                    produto.get("estoque", 0),
                    produto.get("minimo", 0)
                ),
                tags=(str(produto.get("id", "")),)
            )
    def buscar_produto_por_codigo(self, codigo):
        """Busca um produto pelo código."""
        if self.controller:
            return self.controller.buscar_produto_por_codigo(codigo)
        return None
    
    def abrir_form_produto(self, produto_id=None):
        """Abre o formulário para adicionar ou editar um produto."""
        # Cria uma janela de diálogo modal
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Novo Produto" if not produto_id else "Editar Produto")
        dialog.geometry("650x550")  # Tamanho adequado para mostrar todos os campos
        dialog.minsize(650, 550)    # Tamanho mínimo para garantir que todos os campos sejam visíveis
        dialog.grab_set()           # Torna a janela modal
        dialog.focus_set()
        
        # Centraliza a janela
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Cria o formulário dentro da janela de diálogo
        ProdutoForm(dialog, self, produto_id)
    
    def editar_produto(self):
        """Edita o produto selecionado."""
        selection = self.produtos_tree.selection()
        if not selection:
            messagebox.showinfo("Aviso", "Selecione um produto para editar.")
            return
        
        # Obtém o ID do produto selecionado
        produto_id = self.produtos_tree.item(selection[0], "tags")[0]
        
        # Verifica se o ID é válido
        if not produto_id:
            messagebox.showerror("Erro", "ID do produto inválido.")
            return
            
        print(f"Editando produto com ID: {produto_id}")
        
        # Abre o formulário para edição
        self.abrir_form_produto(produto_id)
    
    def excluir_produto(self):
        """Exclui o produto selecionado."""
        selection = self.produtos_tree.selection()
        if not selection:
            messagebox.showinfo("Aviso", "Selecione um produto para excluir.")
            return
        
        # Confirmação
        if not messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este produto?"):
            return
        
        # Obtém o ID do produto selecionado
        produto_id = self.produtos_tree.item(selection[0], "tags")[0]
        
        # Exclui o produto
        if self.controller:
            resultado = self.controller.excluir_produto(produto_id)
            if resultado.get("sucesso", False):
                messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
                self.carregar_produtos()
            else:
                messagebox.showerror("Erro", resultado.get("mensagem", "Erro ao excluir produto."))
        else:
            # Simulação para testes
            messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
            self.carregar_produtos()
    
    def importar_produtos(self):
        """Importa produtos de um arquivo CSV."""
        arquivo = filedialog.askopenfilename(
            title="Importar Produtos",
            filetypes=[("CSV", "*.csv"), ("Todos os arquivos", "*.*")]
        )
        
        if not arquivo:
            return
        
        if self.controller:
            resultado = self.controller.importar_produtos(arquivo)
            if resultado.get("sucesso", False):
                messagebox.showinfo("Sucesso", resultado.get("mensagem", "Produtos importados com sucesso!"))
                self.carregar_produtos()
            else:
                messagebox.showerror("Erro", resultado.get("mensagem", "Erro ao importar produtos."))
        else:
            messagebox.showinfo("Informação", "Funcionalidade em desenvolvimento.")
    
    def exportar_produtos(self):
        """Exporta produtos para um arquivo CSV."""
        arquivo = filedialog.asksaveasfilename(
            title="Exportar Produtos",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv"), ("Todos os arquivos", "*.*")]
        )
        
        if not arquivo:
            return
        
        if self.controller:
            resultado = self.controller.exportar_produtos(arquivo)
            if resultado.get("sucesso", False):
                messagebox.showinfo("Sucesso", resultado.get("mensagem", "Produtos exportados com sucesso!"))
            else:
                messagebox.showerror("Erro", resultado.get("mensagem", "Erro ao exportar produtos."))
        else:
            messagebox.showinfo("Informação", "Funcionalidade em desenvolvimento.")
    
    def salvar_produto(self, produto_data):
        """Salva um produto (novo ou editado)."""
        if self.controller:
            if produto_data.get("id"):
                resultado = self.controller.atualizar_produto(produto_data)
            else:
                resultado = self.controller.inserir_produto(produto_data)
            
            if resultado.get("sucesso", False):
                messagebox.showinfo("Sucesso", "Produto salvo com sucesso!")
                self.carregar_produtos()
                return True
            else:
                messagebox.showerror("Erro", resultado.get("mensagem", "Erro ao salvar produto."))
                return False
        else:
            # Simulação para testes
            messagebox.showinfo("Sucesso", "Produto salvo com sucesso!")
            self.carregar_produtos()
            return True
    
    def obter_produto(self, produto_id):
        """Obtém os dados de um produto pelo ID."""
        if self.controller:
            return self.controller.obter_produto(produto_id)
        else:
            # Dados de exemplo para testes
            produtos = self.obter_produtos_exemplo()
            for produto in produtos:
                if str(produto["id"]) == str(produto_id):
                    return produto
            return None
    
    def obter_produtos_exemplo(self):
        """Retorna dados de exemplo para os produtos."""
        return [
            {
                "id": 1,
                "codigo": "P001",
                "nome": "Produto 1",
                "categoria": "Categoria 1",
                "preco": 25.50,
                "estoque": 15,
                "minimo": 5,
                "descricao": "Descrição do Produto 1",
                "fornecedor": "Fornecedor A",
                "data_cadastro": "01/01/2023",
                "imagem": None
            },
            {
                "id": 2,
                "codigo": "P002",
                "nome": "Produto 2",
                "categoria": "Categoria 1",
                "preco": 18.75,
                "estoque": 8,
                "minimo": 10,
                "descricao": "Descrição do Produto 2",
                "fornecedor": "Fornecedor B",
                "data_cadastro": "15/01/2023",
                "imagem": None
            },
            {
                "id": 3,
                "codigo": "P003",
                "nome": "Produto 3",
                "categoria": "Categoria 2",
                "preco": 45.00,
                "estoque": 0,
                "minimo": 3,
                "descricao": "Descrição do Produto 3",
                "fornecedor": "Fornecedor A",
                "data_cadastro": "20/01/2023",
                "imagem": None
            },
            {
                "id": 4,
                "codigo": "P004",
                "nome": "Produto 4",
                "categoria": "Categoria 2",
                "preco": 12.90,
                "estoque": 20,
                "minimo": 5,
                "descricao": "Descrição do Produto 4",
                "fornecedor": "Fornecedor C",
                "data_cadastro": "25/01/2023",
                "imagem": None
            },
            {
                "id": 5,
                "codigo": "P005",
                "nome": "Produto 5",
                "categoria": "Categoria 3",
                "preco": 32.50,
                "estoque": 3,
                "minimo": 5,
                "descricao": "Descrição do Produto 5",
                "fornecedor": "Fornecedor B",
                "data_cadastro": "01/02/2023",
                "imagem": None
            }
        ]