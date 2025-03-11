import customtkinter as ctk
from tkinter import messagebox
from ..utils.widgets import NumericEntry

class ProdutoForm:
    def __init__(self, parent, controller, produto_id=None, callback=None):
        self.parent = parent
        self.controller = controller
        self.produto_id = produto_id
        self.callback = callback
        self.setup_ui()
    
    def setup_ui(self):
        # Cria uma nova janela
        self.produto_window = ctk.CTkToplevel(self.parent)
        self.produto_window.title("Novo Produto" if not self.produto_id else "Editar Produto")
        self.produto_window.geometry("600x650")
        self.produto_window.grab_set()  # Torna a janela modal
        
        # Título
        title_label = ctk.CTkLabel(
            self.produto_window, 
            text="CADASTRO DE PRODUTO", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Frame principal
        main_frame = ctk.CTkScrollableFrame(self.produto_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Formulário
        # Código
        codigo_label = ctk.CTkLabel(main_frame, text="Código:")
        codigo_label.pack(anchor="w", padx=10, pady=5)
        
        self.codigo_var = ctk.StringVar()
        codigo_entry = ctk.CTkEntry(main_frame, textvariable=self.codigo_var, width=300)
        codigo_entry.pack(fill="x", padx=10, pady=5)
        
        # Nome
        nome_label = ctk.CTkLabel(main_frame, text="Nome:")
        nome_label.pack(anchor="w", padx=10, pady=5)
        
        self.nome_var = ctk.StringVar()
        nome_entry = ctk.CTkEntry(main_frame, textvariable=self.nome_var, width=300)
        nome_entry.pack(fill="x", padx=10, pady=5)
        
        # Descrição
        descricao_label = ctk.CTkLabel(main_frame, text="Descrição:")
        descricao_label.pack(anchor="w", padx=10, pady=5)
        
        self.descricao_var = ctk.StringVar()
        descricao_entry = ctk.CTkEntry(main_frame, textvariable=self.descricao_var, width=300)
        descricao_entry.pack(fill="x", padx=10, pady=5)
        
        # Categoria
        categoria_label = ctk.CTkLabel(main_frame, text="Categoria:")
        categoria_label.pack(anchor="w", padx=10, pady=5)
        
        categorias = self.controller.listar_categorias()
        self.categoria_options = [f"{cat['id']} - {cat['nome']}" for cat in categorias]
        
        self.categoria_var = ctk.StringVar()
        categoria_combobox = ctk.CTkComboBox(
            main_frame, 
            values=self.categoria_options,
            variable=self.categoria_var,
            width=300
        )
        categoria_combobox.pack(fill="x", padx=10, pady=5)
        
        # Fornecedor
        fornecedor_label = ctk.CTkLabel(main_frame, text="Fornecedor:")
        fornecedor_label.pack(anchor="w", padx=10, pady=5)
        
        fornecedores = self.controller.listar_fornecedores()
        self.fornecedor_options = [f"{forn['id']} - {forn['nome']}" for forn in fornecedores]
        
        self.fornecedor_var = ctk.StringVar()
        fornecedor_combobox = ctk.CTkComboBox(
            main_frame, 
            values=self.fornecedor_options,
            variable=self.fornecedor_var,
            width=300
        )
        fornecedor_combobox.pack(fill="x", padx=10, pady=5)
        
        # Preço de custo
        preco_custo_label = ctk.CTkLabel(main_frame, text="Preço de Custo (R$):")
        preco_custo_label.pack(anchor="w", padx=10, pady=5)
        
        self.preco_custo_var = ctk.StringVar()
        preco_custo_entry = NumericEntry(main_frame, decimal=True, textvariable=self.preco_custo_var, width=300)
        preco_custo_entry.pack(fill="x", padx=10, pady=5)
        
        # Preço de venda
        preco_venda_label = ctk.CTkLabel(main_frame, text="Preço de Venda (R$):")
        preco_venda_label.pack(anchor="w", padx=10, pady=5)
        
        self.preco_venda_var = ctk.StringVar()
        preco_venda_entry = NumericEntry(main_frame, decimal=True, textvariable=self.preco_venda_var, width=300)
        preco_venda_entry.pack(fill="x", padx=10, pady=5)
        
        # Estoque atual
        estoque_atual_label = ctk.CTkLabel(main_frame, text="Estoque Atual:")
        estoque_atual_label.pack(anchor="w", padx=10, pady=5)
        
        self.estoque_atual_var = ctk.StringVar()
        estoque_atual_entry = NumericEntry(main_frame, textvariable=self.estoque_atual_var, width=300)
        estoque_atual_entry.pack(fill="x", padx=10, pady=5)
        
        # Estoque mínimo
        estoque_minimo_label = ctk.CTkLabel(main_frame, text="Estoque Mínimo:")
        estoque_minimo_label.pack(anchor="w", padx=10, pady=5)
        
        self.estoque_minimo_var = ctk.StringVar()
        estoque_minimo_entry = NumericEntry(main_frame, textvariable=self.estoque_minimo_var, width=300)
        estoque_minimo_entry.pack(fill="x", padx=10, pady=5)
        
        # Unidade
        unidade_label = ctk.CTkLabel(main_frame, text="Unidade:")
        unidade_label.pack(anchor="w", padx=10, pady=5)
        
        self.unidade_var = ctk.StringVar(value="UN")
        unidade_entry = ctk.CTkEntry(main_frame, textvariable=self.unidade_var, width=300)
        unidade_entry.pack(fill="x", padx=10, pady=5)
        
        # Localização
        localizacao_label = ctk.CTkLabel(main_frame, text="Localização:")
        localizacao_label.pack(anchor="w", padx=10, pady=5)
        
        self.localizacao_var = ctk.StringVar()
        localizacao_entry = ctk.CTkEntry(main_frame, textvariable=self.localizacao_var, width=300)
        localizacao_entry.pack(fill="x", padx=10, pady=5)
        
        # Código de barras
        codigo_barras_label = ctk.CTkLabel(main_frame, text="Código de Barras:")
        codigo_barras_label.pack(anchor="w", padx=10, pady=5)
        
        self.codigo_barras_var = ctk.StringVar()
        codigo_barras_entry = ctk.CTkEntry(main_frame, textvariable=self.codigo_barras_var, width=300)
        codigo_barras_entry.pack(fill="x", padx=10, pady=5)
        
        # Frame de botões
        botoes_frame = ctk.CTkFrame(self.produto_window, fg_color="transparent")
        botoes_frame.pack(fill="x", padx=20, pady=20)
        
        # Botões de salvar e cancelar
        salvar_btn = ctk.CTkButton(
            botoes_frame, 
            text="Salvar", 
            command=self.salvar,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        salvar_btn.pack(side="left", padx=5)
        
        cancelar_btn = ctk.CTkButton(
            botoes_frame, 
            text="Cancelar", 
            command=self.produto_window.destroy,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        cancelar_btn.pack(side="right", padx=5)
        
        # Se estiver editando, carrega os dados do produto
        if self.produto_id:
            self.carregar_produto()
    
    def carregar_produto(self):
        """Carrega os dados do produto para edição."""
        produto = self.controller.obter_produto(self.produto_id)
        if produto:
            self.codigo_var.set(produto["codigo"])
            self.nome_var.set(produto["nome"])
            self.descricao_var.set(produto["descricao"] or "")
            
            # Seleciona a categoria
            if produto["categoria_id"]:
                for option in self.categoria_options:
                    if option.startswith(str(produto["categoria_id"])):
                        self.categoria_var.set(option)
                        break
            
            # Seleciona o fornecedor
            if produto["fornecedor_id"]:
                for option in self.fornecedor_options:
                    if option.startswith(str(produto["fornecedor_id"])):
                        self.fornecedor_var.set(option)
                        break
            
            self.preco_custo_var.set(str(produto["preco_custo"]))
            self.preco_venda_var.set(str(produto["preco_venda"]))
            self.estoque_atual_var.set(str(produto["estoque_atual"]))
            self.estoque_minimo_var.set(str(produto["estoque_minimo"]))
            self.unidade_var.set(produto["unidade"] or "UN")
            self.localizacao_var.set(produto["localizacao"] or "")
            self.codigo_barras_var.set(produto["codigo_barras"] or "")
    
    def salvar(self):
        """Salva o produto."""
        # Validação básica
        if not self.codigo_var.get() or not self.nome_var.get():
            messagebox.showerror("Erro", "Código e Nome são campos obrigatórios.")
            return
        
        try:
            preco_custo = float(self.preco_custo_var.get() or 0)
            preco_venda = float(self.preco_venda_var.get() or 0)
            estoque_atual = int(self.estoque_atual_var.get() or 0)
            estoque_minimo = int(self.estoque_minimo_var.get() or 0)
        except ValueError:
            messagebox.showerror("Erro", "Valores numéricos inválidos.")
            return
        
        # Prepara os dados do produto
        produto_data = {
            "codigo": self.codigo_var.get(),
            "nome": self.nome_var.get(),
            "descricao": self.descricao_var.get(),
            "preco_custo": preco_custo,
            "preco_venda": preco_venda,
            "estoque_atual": estoque_atual,
            "estoque_minimo": estoque_minimo,
            "unidade": self.unidade_var.get(),
            "localizacao": self.localizacao_var.get(),
            "codigo_barras": self.codigo_barras_var.get()
        }
        
        # Extrai os IDs da categoria e fornecedor selecionados
        if self.categoria_var.get():
            try:
                categoria_id = int(self.categoria_var.get().split(" - ")[0])
                produto_data["categoria_id"] = categoria_id
            except (ValueError, IndexError):
                pass
        
        if self.fornecedor_var.get():
            try:
                fornecedor_id = int(self.fornecedor_var.get().split(" - ")[0])
                produto_data["fornecedor_id"] = fornecedor_id
            except (ValueError, IndexError):
                pass
        
        # Salva o produto
        if self.produto_id:
            produto_data["id"] = self.produto_id
            resultado = self.controller.atualizar_produto(produto_data)
            mensagem = "Produto atualizado com sucesso!"
        else:
            resultado = self.controller.adicionar_produto(produto_data)
            mensagem = "Produto adicionado com sucesso!"
        
        if isinstance(resultado, dict) and "erro" in resultado:
            messagebox.showerror("Erro", resultado["erro"])
        elif resultado:
            messagebox.showinfo("Sucesso", mensagem)
            if self.callback:
                self.callback()
            self.produto_window.destroy()
        else:
            messagebox.showerror("Erro", "Não foi possível salvar o produto.")