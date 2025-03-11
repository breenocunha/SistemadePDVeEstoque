import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import os
from PIL import Image, ImageTk
import datetime

class ProdutoForm:
    def __init__(self, parent, produtos_view, produto_id=None):
        self.parent = parent
        self.produtos_view = produtos_view
        self.controller = produtos_view.controller
        self.produto_id = produto_id
        self.imagem_path = None
        
        # Cria a janela do formulário
        self.setup_ui()
        
        # Carrega os dados do produto se estiver editando
        if produto_id:
            print(f"Carregando produto com ID: {produto_id}")
            self.carregar_produto(produto_id)

    def setup_ui(self):
        """Configura a interface do formulário."""
        # Frame principal com scrollbar
        self.outer_frame = ctk.CTkFrame(self.parent)
        self.outer_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Canvas para permitir rolagem
        self.canvas = ctk.CTkCanvas(self.outer_frame, highlightthickness=0, bg=self.outer_frame._fg_color[1])
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        self.scrollbar = ctk.CTkScrollbar(self.outer_frame, command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        
        # Configura o canvas para usar a scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Frame dentro do canvas para conter o conteúdo
        self.frame = ctk.CTkFrame(self.canvas, fg_color="transparent")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        
        # Ajusta a largura do frame interno para preencher o canvas
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Título
        titulo = "Editar Produto" if self.produto_id else "Novo Produto"
        titulo_label = ctk.CTkLabel(
            self.frame, 
            text=titulo, 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo_label.pack(pady=10)
        
        # Frame para os campos
        form_frame = ctk.CTkFrame(self.frame)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Código
        codigo_frame = ctk.CTkFrame(form_frame)
        codigo_frame.pack(fill="x", padx=10, pady=5)
        
        codigo_label = ctk.CTkLabel(codigo_frame, text="Código:", width=100, anchor="w")
        codigo_label.pack(side="left", padx=5)
        
        self.codigo_var = ctk.StringVar()
        codigo_entry = ctk.CTkEntry(codigo_frame, textvariable=self.codigo_var, width=200)
        codigo_entry.pack(side="left", padx=5)
        
        # Nome
        nome_frame = ctk.CTkFrame(form_frame)
        nome_frame.pack(fill="x", padx=10, pady=5)
        
        nome_label = ctk.CTkLabel(nome_frame, text="Nome:", width=100, anchor="w")
        nome_label.pack(side="left", padx=5)
        
        self.nome_var = ctk.StringVar()
        nome_entry = ctk.CTkEntry(nome_frame, textvariable=self.nome_var, width=400)
        nome_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Categoria
        categoria_frame = ctk.CTkFrame(form_frame)
        categoria_frame.pack(fill="x", padx=10, pady=5)
        
        categoria_label = ctk.CTkLabel(categoria_frame, text="Categoria:", width=100, anchor="w")
        categoria_label.pack(side="left", padx=5)
        
        self.categoria_var = ctk.StringVar()
        categorias = ["Eletrônicos", "Informática", "Acessórios", "Áudio", "Outros"]
        categoria_combo = ctk.CTkComboBox(
            categoria_frame, 
            values=categorias,
            variable=self.categoria_var,
            width=200
        )
        categoria_combo.pack(side="left", padx=5)
        
        # Preço
        preco_frame = ctk.CTkFrame(form_frame)
        preco_frame.pack(fill="x", padx=10, pady=5)
        
        preco_label = ctk.CTkLabel(preco_frame, text="Preço (R$):", width=100, anchor="w")
        preco_label.pack(side="left", padx=5)
        
        self.preco_var = ctk.StringVar()
        preco_entry = ctk.CTkEntry(preco_frame, textvariable=self.preco_var, width=150)
        preco_entry.pack(side="left", padx=5)
        
        # Estoque - Reorganizado para melhor visualização
        estoque_frame = ctk.CTkFrame(form_frame)
        estoque_frame.pack(fill="x", padx=10, pady=5)
        
        estoque_label = ctk.CTkLabel(estoque_frame, text="Estoque:", width=100, anchor="w")
        estoque_label.pack(side="left", padx=5)
        
        self.estoque_var = ctk.StringVar()
        estoque_entry = ctk.CTkEntry(estoque_frame, textvariable=self.estoque_var, width=100)
        estoque_entry.pack(side="left", padx=5)
        
        # Estoque mínimo - Agora em um frame separado para melhor visualização
        minimo_frame = ctk.CTkFrame(form_frame)
        minimo_frame.pack(fill="x", padx=10, pady=5)
        
        minimo_label = ctk.CTkLabel(minimo_frame, text="Estoque Mínimo:", width=100, anchor="w")
        minimo_label.pack(side="left", padx=5)
        
        self.minimo_var = ctk.StringVar()
        minimo_entry = ctk.CTkEntry(minimo_frame, textvariable=self.minimo_var, width=100)
        minimo_entry.pack(side="left", padx=5)
        
        # Fornecedor
        fornecedor_frame = ctk.CTkFrame(form_frame)
        fornecedor_frame.pack(fill="x", padx=10, pady=5)
        
        fornecedor_label = ctk.CTkLabel(fornecedor_frame, text="Fornecedor:", width=100, anchor="w")
        fornecedor_label.pack(side="left", padx=5)
        
        self.fornecedor_var = ctk.StringVar()
        fornecedor_entry = ctk.CTkEntry(fornecedor_frame, textvariable=self.fornecedor_var, width=300)
        fornecedor_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Descrição
        descricao_frame = ctk.CTkFrame(form_frame)
        descricao_frame.pack(fill="x", padx=10, pady=5)
        
        descricao_label = ctk.CTkLabel(descricao_frame, text="Descrição:", width=100, anchor="w")
        descricao_label.pack(side="left", padx=5, anchor="n")
        
        self.descricao_text = ctk.CTkTextbox(descricao_frame, height=100, width=400)
        self.descricao_text.pack(side="left", padx=5, fill="both", expand=True)
        
        # Imagem
        imagem_frame = ctk.CTkFrame(form_frame)
        imagem_frame.pack(fill="x", padx=10, pady=5)
        
        imagem_label = ctk.CTkLabel(imagem_frame, text="Imagem:", width=100, anchor="w")
        imagem_label.pack(side="left", padx=5)
        
        self.imagem_btn = ctk.CTkButton(
            imagem_frame, 
            text="Selecionar Imagem", 
            command=self.selecionar_imagem,
            width=150
        )
        self.imagem_btn.pack(side="left", padx=5)
        
        self.imagem_nome_var = ctk.StringVar(value="Nenhuma imagem selecionada")
        imagem_nome_label = ctk.CTkLabel(imagem_frame, textvariable=self.imagem_nome_var)
        imagem_nome_label.pack(side="left", padx=5)
        
        # Botões - Colocados em um frame fixo na parte inferior
        botoes_frame = ctk.CTkFrame(self.frame)
        botoes_frame.pack(fill="x", padx=10, pady=10)
        
        cancelar_btn = ctk.CTkButton(
            botoes_frame, 
            text="Cancelar", 
            command=self.cancelar,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            width=100
        )
        cancelar_btn.pack(side="right", padx=5)
        
        salvar_btn = ctk.CTkButton(
            botoes_frame, 
            text="Salvar", 
            command=self.salvar,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=100
        )
        salvar_btn.pack(side="right", padx=5)
        
        # Ajusta o tamanho do canvas após adicionar todos os widgets
        self.frame.update_idletasks()
        self.canvas.config(width=600, height=500)  # Tamanho fixo mais adequado
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    # Adicione este novo método para ajustar a largura do frame interno
    def _on_canvas_configure(self, event):
        """Ajusta a largura do frame interno quando o canvas é redimensionado."""
        # Atualiza a largura da janela do canvas para corresponder à largura do canvas
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def carregar_produto(self, produto_id):
        """Carrega os dados do produto para edição."""
        try:
            produto = self.produtos_view.obter_produto(produto_id)
            
            if not produto:
                messagebox.showerror("Erro", f"Produto com ID {produto_id} não encontrado.")
                self.cancelar()
                return
            
            print(f"Produto carregado: {produto}")
            
            # Preenche os campos com os dados do produto
            self.codigo_var.set(produto["codigo"])
            self.nome_var.set(produto["nome"])
            self.categoria_var.set(produto["categoria"])
            self.preco_var.set(str(produto["preco"]))
            self.estoque_var.set(str(produto["estoque"]))
            self.minimo_var.set(str(produto.get("minimo", 0)))
            self.fornecedor_var.set(produto.get("fornecedor", ""))
            
            # Descrição
            self.descricao_text.delete("0.0", "end")
            self.descricao_text.insert("0.0", produto.get("descricao", ""))
            
            # Imagem
            if produto.get("imagem"):
                self.imagem_path = produto["imagem"]
                self.imagem_nome_var.set(os.path.basename(produto["imagem"]))
        except Exception as e:
            print(f"Erro ao carregar produto: {str(e)}")
            messagebox.showerror("Erro", f"Erro ao carregar produto: {str(e)}")
            self.cancelar()
    
    def selecionar_imagem(self):
        """Abre um diálogo para selecionar uma imagem."""
        imagem_path = filedialog.askopenfilename(
            title="Selecionar Imagem",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif"), ("Todos os arquivos", "*.*")]
        )
        
        if imagem_path:
            self.imagem_path = imagem_path
            self.imagem_nome_var.set(os.path.basename(imagem_path))
    
    def salvar(self):
        """Salva os dados do produto."""
        try:
            # Valida os campos obrigatórios
            if not self.codigo_var.get() or not self.nome_var.get() or not self.preco_var.get() or not self.estoque_var.get():
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
                return
            
            # Valida o preço
            try:
                preco = float(self.preco_var.get().replace(",", "."))
            except ValueError:
                messagebox.showerror("Erro", "Preço inválido.")
                return
            
            # Valida o estoque
            try:
                estoque = int(self.estoque_var.get())
            except ValueError:
                messagebox.showerror("Erro", "Estoque inválido.")
                return
            
            # Valida o estoque mínimo
            try:
                minimo = int(self.minimo_var.get()) if self.minimo_var.get() else 0
            except ValueError:
                messagebox.showerror("Erro", "Estoque mínimo inválido.")
                return
            
            # Prepara os dados do produto
            produto_data = {
                "codigo": self.codigo_var.get(),
                "nome": self.nome_var.get(),
                "categoria": self.categoria_var.get(),
                "preco": preco,
                "estoque": estoque,
                "minimo": minimo,
                "fornecedor": self.fornecedor_var.get(),
                "descricao": self.descricao_text.get("0.0", "end").strip(),
                "imagem": self.imagem_path
            }
            
            # Adiciona a data de cadastro para novos produtos
            if not self.produto_id:
                produto_data["data_cadastro"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                produto_data["id"] = self.produto_id
            
            print(f"Salvando produto: {produto_data}")
            
            # Salva o produto usando o método da view
            resultado = self.produtos_view.salvar_produto(produto_data)
            
            if resultado:
                self.cancelar()
        except Exception as e:
            print(f"Erro ao salvar produto: {str(e)}")
            messagebox.showerror("Erro", f"Erro ao salvar produto: {str(e)}")
    
    def cancelar(self):
        """Fecha o formulário."""
        # Obtém a janela pai (dialog) e a destrói