import customtkinter as ctk
from tkinter import ttk, messagebox
import datetime
from PIL import Image, ImageTk
import os

class PDVView:
    def __init__(self, parent, controller=None):
        self.parent = parent
        self.controller = controller
        self.itens_venda = []
        self.total_venda = 0.0
        self.cliente_selecionado = None
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título com estilo
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="#e74c3c", corner_radius=10)
        title_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="PONTO DE VENDA", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=10)
        
        # Frame para o conteúdo principal
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Divide em duas colunas
        left_frame = ctk.CTkFrame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        # === COLUNA ESQUERDA ===
        # Frame para busca de produtos
        search_frame = ctk.CTkFrame(left_frame)
        search_frame.pack(fill="x", padx=10, pady=10)
        
        search_label = ctk.CTkLabel(search_frame, text="Código/Nome:")
        search_label.pack(side="left", padx=5)
        
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, width=200)
        search_entry.pack(side="left", padx=5)
        search_entry.bind("<Return>", lambda event: self.buscar_produto())
        
        search_btn = ctk.CTkButton(
            search_frame, 
            text="Buscar", 
            command=self.buscar_produto,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        search_btn.pack(side="left", padx=5)
        
        # Frame para quantidade
        qty_frame = ctk.CTkFrame(left_frame)
        qty_frame.pack(fill="x", padx=10, pady=5)
        
        qty_label = ctk.CTkLabel(qty_frame, text="Quantidade:")
        qty_label.pack(side="left", padx=5)
        
        self.qty_var = ctk.StringVar(value="1")
        qty_entry = ctk.CTkEntry(qty_frame, textvariable=self.qty_var, width=80)
        qty_entry.pack(side="left", padx=5)
        
        add_btn = ctk.CTkButton(
            qty_frame, 
            text="Adicionar", 
            command=self.adicionar_item,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        add_btn.pack(side="left", padx=5)
        
        # Frame para a tabela de itens
        table_frame = ctk.CTkFrame(left_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tabela de itens
        self.itens_tree = ttk.Treeview(
            table_frame,
            columns=("codigo", "nome", "quantidade", "preco", "subtotal"),
            show="headings"
        )
        
        self.itens_tree.heading("codigo", text="Código")
        self.itens_tree.heading("nome", text="Produto")
        self.itens_tree.heading("quantidade", text="Qtd")
        self.itens_tree.heading("preco", text="Preço")
        self.itens_tree.heading("subtotal", text="Subtotal")
        
        self.itens_tree.column("codigo", width=80)
        self.itens_tree.column("nome", width=200)
        self.itens_tree.column("quantidade", width=50)
        self.itens_tree.column("preco", width=80)
        self.itens_tree.column("subtotal", width=80)
        
        # Adiciona barra de rolagem
        scrollbar = ctk.CTkScrollbar(table_frame, command=self.itens_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.itens_tree.configure(yscrollcommand=scrollbar.set)
        
        self.itens_tree.pack(fill="both", expand=True)
        
        # Botões de ação para itens
        item_actions_frame = ctk.CTkFrame(left_frame)
        item_actions_frame.pack(fill="x", padx=10, pady=5)
        
        remover_btn = ctk.CTkButton(
            item_actions_frame, 
            text="Remover Item", 
            command=self.remover_item,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        remover_btn.pack(side="left", padx=5)
        
        editar_btn = ctk.CTkButton(
            item_actions_frame, 
            text="Editar Qtd", 
            command=self.editar_quantidade,
            fg_color="#f39c12",
            hover_color="#d35400"
        )
        editar_btn.pack(side="left", padx=5)
        
        limpar_btn = ctk.CTkButton(
            item_actions_frame, 
            text="Limpar Venda", 
            command=self.limpar_venda,
            fg_color="#7f8c8d",
            hover_color="#2c3e50"
        )
        limpar_btn.pack(side="right", padx=5)
        
        # === COLUNA DIREITA ===
        # Frame para informações do cliente
        cliente_frame = ctk.CTkFrame(right_frame)
        cliente_frame.pack(fill="x", padx=10, pady=10)
        
        cliente_label = ctk.CTkLabel(
            cliente_frame, 
            text="CLIENTE", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        cliente_label.pack(pady=5)
        
        self.cliente_info_var = ctk.StringVar(value="Cliente: Consumidor Final")
        cliente_info_label = ctk.CTkLabel(cliente_frame, textvariable=self.cliente_info_var)
        cliente_info_label.pack(pady=5)
        
        cliente_btn = ctk.CTkButton(
            cliente_frame, 
            text="Selecionar Cliente", 
            command=self.selecionar_cliente,
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        )
        cliente_btn.pack(pady=5)
        
        # Frame para total da venda
        total_frame = ctk.CTkFrame(right_frame)
        total_frame.pack(fill="x", padx=10, pady=10)
        
        total_label = ctk.CTkLabel(
            total_frame, 
            text="TOTAL DA VENDA", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        total_label.pack(pady=5)
        
        self.total_var = ctk.StringVar(value="R$ 0,00")
        total_value_label = ctk.CTkLabel(
            total_frame, 
            textvariable=self.total_var,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#2ecc71"
        )
        total_value_label.pack(pady=10)
        
        # Frame para forma de pagamento
        pagamento_frame = ctk.CTkFrame(right_frame)
        pagamento_frame.pack(fill="x", padx=10, pady=10)
        
        pagamento_label = ctk.CTkLabel(
            pagamento_frame, 
            text="FORMA DE PAGAMENTO", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        pagamento_label.pack(pady=5)
        
        self.pagamento_var = ctk.StringVar(value="Dinheiro")
        pagamento_options = ["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "PIX", "Transferência"]
        
        for option in pagamento_options:
            pagamento_radio = ctk.CTkRadioButton(
                pagamento_frame,
                text=option,
                variable=self.pagamento_var,
                value=option
            )
            pagamento_radio.pack(anchor="w", padx=20, pady=2)
        
        # Frame para observações
        obs_frame = ctk.CTkFrame(right_frame)
        obs_frame.pack(fill="x", padx=10, pady=10)
        
        obs_label = ctk.CTkLabel(obs_frame, text="Observações:")
        obs_label.pack(anchor="w", padx=5, pady=2)
        
        self.obs_text = ctk.CTkTextbox(obs_frame, height=60)
        self.obs_text.pack(fill="x", padx=5, pady=2)
        
        # Frame para botões de finalização
        finish_frame = ctk.CTkFrame(right_frame)
        finish_frame.pack(fill="x", padx=10, pady=10)
        
        finalizar_btn = ctk.CTkButton(
            finish_frame, 
            text="FINALIZAR VENDA", 
            command=self.finalizar_venda,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        finalizar_btn.pack(fill="x", pady=5)
        
        cancelar_btn = ctk.CTkButton(
            finish_frame, 
            text="Cancelar Venda", 
            command=self.limpar_venda,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        cancelar_btn.pack(fill="x", pady=5)
    
    def buscar_produto(self):
        """Busca um produto pelo código ou nome."""
        termo = self.search_var.get().strip()
        if not termo:
            messagebox.showinfo("Aviso", "Digite um código ou nome de produto.")
            return
        
        # Busca o produto
        if self.controller:
            produtos = self.controller.buscar_produtos(termo)
        else:
            # Simulação para testes
            produtos = self.obter_produtos_exemplo()
            produtos = [p for p in produtos if termo.lower() in p["nome"].lower() or termo in p["codigo"]]
        
        if not produtos:
            messagebox.showinfo("Aviso", "Nenhum produto encontrado.")
            return
        
        # Se encontrou apenas um produto, adiciona diretamente
        if len(produtos) == 1:
            self.adicionar_produto(produtos[0])
        else:
            # Se encontrou vários, mostra uma janela para seleção
            self.mostrar_selecao_produtos(produtos)
    
    def mostrar_selecao_produtos(self, produtos):
        """Mostra uma janela para seleção de produtos."""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Selecionar Produto")
        dialog.geometry("600x400")
        dialog.grab_set()
        
        # Centraliza a janela
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Selecione um Produto", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Frame para a tabela
        table_frame = ctk.CTkFrame(main_frame)
        table_frame.pack(fill="both", expand=True, pady=10)
        
        # Tabela de produtos
        produtos_tree = ttk.Treeview(table_frame)
        produtos_tree["columns"] = ("codigo", "nome", "preco", "estoque")
        
        produtos_tree.heading("codigo", text="Código")
        produtos_tree.heading("nome", text="Produto")
        produtos_tree.heading("preco", text="Preço")
        produtos_tree.heading("estoque", text="Estoque")
        
        produtos_tree.column("codigo", width=100)
        produtos_tree.column("nome", width=250)
        produtos_tree.column("preco", width=100)
        produtos_tree.column("estoque", width=100)
        
        # Oculta a coluna de índice
        produtos_tree["show"] = "headings"
        
        # Adiciona barra de rolagem
        scrollbar = ctk.CTkScrollbar(table_frame, command=produtos_tree.yview)
        scrollbar.pack(side="right", fill="y")
        produtos_tree.configure(yscrollcommand=scrollbar.set)
        
        produtos_tree.pack(fill="both", expand=True)
        
        # Preenche a tabela
        for produto in produtos:
            produtos_tree.insert(
                "", "end", 
                values=(
                    produto["codigo"],
                    produto["nome"],
                    f"R$ {produto['preco']:.2f}",
                    produto["estoque"]
                ),
                tags=(str(produto["id"]),)
            )
        
        # Frame para botões
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", pady=10)
        
        def selecionar():
            selection = produtos_tree.selection()
            if not selection:
                messagebox.showinfo("Aviso", "Selecione um produto.")
                return
            
            # Obtém o ID do produto selecionado
            produto_id = produtos_tree.item(selection[0], "tags")[0]
            
            # Obtém o produto
            if self.controller:
                produto = self.controller.obter_produto(produto_id)
            else:
                # Simulação para testes
                produto = next((p for p in self.obter_produtos_exemplo() if str(p["id"]) == str(produto_id)), None)
            
            if produto:
                self.adicionar_produto(produto)
                dialog.destroy()
        
        selecionar_btn = ctk.CTkButton(
            buttons_frame, 
            text="Selecionar", 
            command=selecionar,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        selecionar_btn.pack(side="left", padx=5)
        
        cancelar_btn = ctk.CTkButton(
            buttons_frame, 
            text="Cancelar", 
            command=dialog.destroy,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        cancelar_btn.pack(side="right", padx=5)
        
        # Bind de duplo clique para selecionar
        produtos_tree.bind("<Double-1>", lambda event: selecionar())
    
    def adicionar_produto(self, produto):
        """Adiciona um produto à venda."""
        try:
            quantidade = float(self.qty_var.get().replace(',', '.'))
            if quantidade <= 0:
                messagebox.showinfo("Aviso", "A quantidade deve ser maior que zero.")
                return
            
            # Verifica se há estoque suficiente
            if produto["estoque"] < quantidade:
                messagebox.showwarning("Aviso", f"Estoque insuficiente. Disponível: {produto['estoque']}")
                return
            
            # Verifica se o produto já está no carrinho
            for i, item in enumerate(self.itens_venda):
                if item["produto_id"] == produto["id"]:
                    # Atualiza a quantidade
                    nova_quantidade = item["quantidade"] + quantidade
                    if produto["estoque"] < nova_quantidade:
                        messagebox.showwarning("Aviso", f"Estoque insuficiente. Disponível: {produto['estoque']}")
                        return
                    
                    self.itens_venda[i]["quantidade"] = nova_quantidade
                    self.itens_venda[i]["subtotal"] = nova_quantidade * produto["preco"]
                    
                    # Atualiza a tabela
                    self.atualizar_tabela_itens()
                    self.atualizar_total()
                    return
            
            # Adiciona o novo item
            novo_item = {
                "produto_id": produto["id"],
                "codigo": produto["codigo"],
                "nome": produto["nome"],
                "quantidade": quantidade,
                "preco": produto["preco"],
                "subtotal": quantidade * produto["preco"]
            }
            
            self.itens_venda.append(novo_item)
            
            # Atualiza a tabela
            self.atualizar_tabela_itens()
            self.atualizar_total()
            
            # Limpa o campo de busca e quantidade
            self.search_var.set("")
            self.qty_var.set("1")
            
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.")
    
    def adicionar_item(self):
        """Adiciona um item à venda a partir da busca."""
        termo = self.search_var.get().strip()
        if not termo:
            messagebox.showinfo("Aviso", "Digite um código ou nome de produto.")
            return
        
        self.buscar_produto()
    
    def remover_item(self):
        """Remove um item da venda."""
        selection = self.itens_tree.selection()
        if not selection:
            messagebox.showinfo("Aviso", "Selecione um item para remover.")
            return
        
        # Obtém o índice do item na lista
        item_id = self.itens_tree.index(selection[0])
        
        # Remove o item da lista
        if 0 <= item_id < len(self.itens_venda):
            self.itens_venda.pop(item_id)
            
            # Atualiza a tabela
            self.atualizar_tabela_itens()
            self.atualizar_total()
    
    def editar_quantidade(self):
        """Edita a quantidade de um item."""
        selection = self.itens_tree.selection()
        if not selection:
            messagebox.showinfo("Aviso", "Selecione um item para editar.")
            return
        
        # Obtém o índice do item na lista
        item_id = self.itens_tree.index(selection[0])
        
        if 0 <= item_id < len(self.itens_venda):
            item = self.itens_venda[item_id]
            
            # Solicita a nova quantidade
            nova_quantidade = ctk.CTkInputDialog(
                title="Editar Quantidade",
                text=f"Nova quantidade para {item['nome']}:"
            ).get_input()
            
            if nova_quantidade:
                try:
                    nova_quantidade = float(nova_quantidade.replace(',', '.'))
                    if nova_quantidade <= 0:
                        messagebox.showinfo("Aviso", "A quantidade deve ser maior que zero.")
                        return
                    
                    # Verifica estoque se tiver controller
                    if self.controller:
                        produto = self.controller.obter_produto(item["produto_id"])
                        if produto and produto["estoque"] < nova_quantidade:
                            messagebox.showwarning("Aviso", f"Estoque insuficiente. Disponível: {produto['estoque']}")
                            return
                    
                    # Atualiza o item
                    self.itens_venda[item_id]["quantidade"] = nova_quantidade
                    self.itens_venda[item_id]["subtotal"] = nova_quantidade * item["preco"]
                    
                    # Atualiza a tabela
                    self.atualizar_tabela_itens()
                    self.atualizar_total()
                    
                except ValueError:
                    messagebox.showerror("Erro", "Quantidade inválida.")
    
    def limpar_venda(self):
        """Limpa todos os itens da venda."""
        if self.itens_venda and not messagebox.askyesno("Confirmação", "Tem certeza que deseja limpar a venda?"):
            return
        
        self.itens_venda = []
        self.total_venda = 0.0
        self.cliente_selecionado = None
        self.cliente_info_var.set("Cliente: Consumidor Final")
        self.pagamento_var.set("Dinheiro")
        self.obs_text.delete("0.0", "end")
        
        # Atualiza a tabela
        self.atualizar_tabela_itens()
        self.atualizar_total()
    
    def atualizar_tabela_itens(self):
        """Atualiza a tabela de itens."""
        # Limpa a tabela
        for item in self.itens_tree.get_children():
            self.itens_tree.delete(item)
        
        # Preenche com os itens atuais
        for item in self.itens_venda:
            self.itens_tree.insert(
                "", "end", 
                values=(
                    item["codigo"],
                    item["nome"],
                    item["quantidade"],
                    f"R$ {item['preco']:.2f}",
                    f"R$ {item['subtotal']:.2f}"
                )
            )
    
    def atualizar_total(self):
        """Atualiza o total da venda."""
        self.total_venda = sum(item["subtotal"] for item in self.itens_venda)
        self.total_var.set(f"R$ {self.total_venda:.2f}")
    
    def selecionar_cliente(self):
        """Abre a janela para selecionar um cliente."""
        # Cria uma janela de diálogo modal
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Selecionar Cliente")
        dialog.geometry("600x400")
        dialog.grab_set()
        
        # Centraliza a janela
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Selecione um Cliente", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Frame para busca
        search_frame = ctk.CTkFrame(main_frame)
        search_frame.pack(fill="x", pady=10)
        
        search_label = ctk.CTkLabel(search_frame, text="Buscar:")
        search_label.pack(side="left", padx=5)
        
        search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, textvariable=search_var, width=300)
        search_entry.pack(side="left", padx=5)
        search_entry.bind("<Return>", lambda event: buscar_cliente())
```

<File before editing>
```python
import customtkinter as ctk
from tkinter import ttk, messagebox
import datetime
from PIL import Image, ImageTk
import os

class PDVView:
    def __init__(self, parent, controller=None):
        self.parent = parent
        self.controller = controller
        self.itens_venda = []
        self.total_venda = 0.0
        self.cliente_selecionado = None
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título com estilo
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="#e74c3c", corner_radius=10)
        title_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="PONTO DE VENDA", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=10)
        
        # Frame para o conteúdo principal
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Divide em duas colunas
        left_frame = ctk.CTkFrame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        # === COLUNA ESQUERDA ===
        # Frame para busca de produtos
        search_frame = ctk.CTkFrame(left_frame)
        search_frame.pack(fill="x", padx=10, pady=10)
        
        search_label = ctk.CTkLabel(search_frame, text="Código/Nome:")
        search_label.pack(side="left", padx=5)
        
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, width=200)
        search_entry.pack(side="left", padx=5)
        search_entry.bind("<Return>", lambda event: self.buscar_produto())
        
        search_btn = ctk.CTkButton(
            search_frame, 
            text="Buscar", 
            command=self.buscar_produto,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        search_btn.pack(side="left", padx=5)
        
        # Frame para quantidade
        qty_frame = ctk.CTkFrame(left_frame)
        qty_frame.pack(fill="x", padx=10, pady=5)
        
        qty_label = ctk.CTkLabel(qty_frame, text="Quantidade:")
        qty_label.pack(side="left", padx=5)
        
        self.qty_var = ctk.StringVar(value="1")
        qty_entry = ctk.CTkEntry(qty_frame, textvariable=self.qty_var, width=80)
        qty_entry.pack(side="left", padx=5)
        
        add_btn = ctk.CTkButton(
            qty_frame, 
            text="Adicionar", 
            command=self.adicionar_item,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        add_btn.pack(side="left", padx=5)
        
        # Frame para a tabela de itens
        table_frame = ctk.CTkFrame(left_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tabela de itens
        self.itens_tree = ttk.Treeview(
            table_frame,
            columns=("codigo", "nome", "quantidade", "preco", "subtotal"),
            show="headings"
        )
        
        self.itens_tree.heading("codigo", text="Código")
        self.itens_tree.heading("nome", text="Produto")
        self.itens_tree.heading("quantidade", text="Qtd")
        self.itens_tree.heading("preco", text="Preço")
        self.itens_tree.heading("subtotal", text="Subtotal")
        
        self.itens_tree.column("codigo", width=80)
        self.itens_tree.column("nome", width=200)
        self.itens_tree.column("quantidade", width=50)
        self.itens_tree.column("preco", width=80)
        self.itens_tree.column("subtotal", width=80)
        
        # Adiciona barra de rolagem
        scrollbar = ctk.CTkScrollbar(table_frame, command=self.itens_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.itens_tree.configure(yscrollcommand=scrollbar.set)
        
        self.itens_tree.pack(fill="both", expand=True)
        
        # Botões de ação para itens
        item_actions_frame = ctk.CTkFrame(left_frame)
        item_actions_frame.pack(fill="x", padx=10, pady=5)
        
        remover_btn = ctk.CTkButton(
            item_actions_frame, 
            text="Remover Item", 
            command=self.remover_item,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        remover_btn.pack(side="left", padx=5)
        
        editar_btn = ctk.CTkButton(
            item_actions_frame, 
            text="Editar Qtd", 
            command=self.editar_quantidade,
            fg_color="#f39c12",
            hover_color="#d35400"
        )
        editar_btn.pack(side="left", padx=5)
        
        limpar_btn = ctk.CTkButton(
            item_actions_frame, 
            text="Limpar Venda", 
            command=self.limpar_venda,
            fg_color="#7f8c8d",
            hover_color="#2c3e50"
        )
        limpar_btn.pack(side="right", padx=5)
        
        # === COLUNA DIREITA ===
        # Frame para informações do cliente
        cliente_frame = ctk.CTkFrame(right_frame)
        cliente_frame.pack(fill="x", padx=10, pady=10)
        
        cliente_label = ctk.CTkLabel(
            cliente_frame, 
            text="CLIENTE", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        cliente_label.pack(pady=5)
        
        self.cliente_info_var = ctk.StringVar(value="Cliente: Consumidor Final")
        cliente_info_label = ctk.CTkLabel(cliente_frame, textvariable=self.cliente_info_var)
        cliente_info_label.pack(pady=5)
        
        cliente_btn = ctk.CTkButton(
            cliente_frame, 
            text="Selecionar Cliente", 
            command=self.selecionar_cliente,
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        )
        cliente_btn.pack(pady=5)
        
        # Frame para total da venda
        total_frame = ctk.CTkFrame(right_frame)
        total_frame.pack(fill="x", padx=10, pady=10)
        
        total_label = ctk.CTkLabel(
            total_frame, 
            text="TOTAL DA VENDA", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        total_label.pack(pady=5)
        
        self.total_var = ctk.StringVar(value="R$ 0,00")
        total_value_label = ctk.CTkLabel(
            total_frame, 
            textvariable=self.total_var,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#2ecc71"
        )
        total_value_label.pack(pady=10)
        
        # Frame para forma de pagamento
        pagamento_frame = ctk.CTkFrame(right_frame)
        pagamento_frame.pack(fill="x", padx=10, pady=10)
        
        pagamento_label = ctk.CTkLabel(
            pagamento_frame, 
            text="FORMA DE PAGAMENTO", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        pagamento_label.pack(pady=5)
        
        self.pagamento_var = ctk.StringVar(value="Dinheiro")
        pagamento_options = ["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "PIX", "Transferência"]
        
        for option in pagamento_options:
            pagamento_radio = ctk.CTkRadioButton(
                pagamento_frame,
                text=option,
                variable=self.pagamento_var,
                value=option
            )
            pagamento_radio.pack(anchor="w", padx=20, pady=2)
        
        # Frame para observações
        obs_frame = ctk.CTkFrame(right_frame)
        obs_frame.pack(fill="x", padx=10, pady=10)
        
        obs_label = ctk.CTkLabel(obs_frame, text="Observações:")
        obs_label.pack(anchor="w", padx=5, pady=2)
        
        self.obs_text = ctk.CTkTextbox(obs_frame, height=60)
        self.obs_text.pack(fill="x", padx=5, pady=2)
        
        # Frame para botões de finalização
        finish_frame = ctk.CTkFrame(right_frame)
        finish_frame.pack(fill="x", padx=10, pady=10)
        
        finish_frame.pack(fill="x", padx=10, pady=10)
        
        finalizar_btn = ctk.CTkButton(
            finish_frame, 
            text="FINALIZAR VENDA", 
            command=self.finalizar_venda,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        finalizar_btn.pack(fill="x", pady=5)
        
        cancelar_btn = ctk.CTkButton(
            finish_frame, 
            text="Cancelar Venda", 
            command=self.limpar_venda,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        cancelar_btn.pack(fill="x", pady=5)
    
    def buscar_produto(self):
        """Busca um produto pelo código ou nome."""
        termo = self.search_var.get().strip()
        if not termo:
            messagebox.showinfo("Aviso", "Digite um código ou nome de produto.")
            return
        
        # Busca o produto
        if self.controller:
            produtos = self.controller.buscar_produtos(termo)
        else:
            # Simulação para testes
            produtos = self.obter_produtos_exemplo()
            produtos = [p for p in produtos if termo.lower() in p["nome"].lower() or termo in p["codigo"]]
        
        if not produtos:
            messagebox.showinfo("Aviso", "Nenhum produto encontrado.")
            return
        
        # Se encontrou apenas um produto, adiciona diretamente
        if len(produtos) == 1:
            self.adicionar_produto(produtos[0])
        else:
            # Se encontrou vários, mostra uma janela para seleção
            self.mostrar_selecao_produtos(produtos)
    
    def mostrar_selecao_produtos(self, produtos):
        """Mostra uma janela para seleção de produtos."""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Selecionar Produto")
        dialog.geometry("600x400")
        dialog.grab_set()
        
        # Centraliza a janela
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Selecione um Produto", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Frame para a tabela
        table_frame = ctk.CTkFrame(main_frame)
        table_frame.pack(fill="both", expand=True, pady=10)
        
        # Tabela de produtos
        produtos_tree = ttk.Treeview(table_frame)
        produtos_tree["columns"] = ("codigo", "nome", "preco", "estoque")
        
        produtos_tree.heading("codigo", text="Código")
        produtos_tree.heading("nome", text="Produto")
        produtos_tree.heading("preco", text="Preço")
        produtos_tree.heading("estoque", text="Estoque")
        
        produtos_tree.column("codigo", width=100)
        produtos_tree.column("nome", width=250)
        produtos_tree.column("preco", width=100)
        produtos_tree.column("estoque", width=100)
        
        # Oculta a coluna de índice
        produtos_tree["show"] = "headings"
        
        # Adiciona barra de rolagem
        scrollbar = ctk.CTkScrollbar(table_frame, command=produtos_tree.yview)
        scrollbar.pack(side="right", fill="y")
        produtos_tree.configure(yscrollcommand=scrollbar.set)
        
        produtos_tree.pack(fill="both", expand=True)
        
        # Preenche a tabela
        for produto in produtos:
            produtos_tree.insert(
                "", "end", 
                values=(
                    produto["codigo"],
                    produto["nome"],
                    f"R$ {produto['preco']:.2f}",
                    produto["estoque"]
                ),
                tags=(str(produto["id"]),)
            )
        
        # Frame para botões
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", pady=10)
        
        def selecionar():
            selection = produtos_tree.selection()
            if not selection:
                messagebox.showinfo("Aviso", "Selecione um produto.")
                return
            
            # Obtém o ID do produto selecionado
            produto_id = produtos_tree.item(selection[0], "tags")[0]
            
            # Obtém o produto
            if self.controller:
                produto = self.controller.obter_produto(produto_id)
            else:
                # Simulação para testes
                produto = next((p for p in self.obter_produtos_exemplo() if str(p["id"]) == str(produto_id)), None)
            
            if produto:
                self.adicionar_produto(produto)
                dialog.destroy()
        
        selecionar_btn = ctk.CTkButton(
            buttons_frame, 
            text="Selecionar", 
            command=selecionar,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        selecionar_btn.pack(side="left", padx=5)
        
        cancelar_btn = ctk.CTkButton(
            buttons_frame, 
            text="Cancelar", 
            command=dialog.destroy,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        cancelar_btn.pack(side="right", padx=5)
        
        # Bind de duplo clique para selecionar
        produtos_tree.bind("<Double-1>", lambda event: selecionar())
    
    def adicionar_produto(self, produto):
        """Adiciona um produto à venda."""
        try:
            quantidade = float(self.qty_var.get().replace(',', '.'))
            if quantidade <= 0:
                messagebox.showinfo("Aviso", "A quantidade deve ser maior que zero.")
                return
            
            # Verifica se há estoque suficiente
            if produto["estoque"] < quantidade:
                messagebox.showwarning("Aviso", f"Estoque insuficiente. Disponível: {produto['estoque']}")
                return
            
            # Verifica se o produto já está no carrinho
            for i, item in enumerate(self.itens_venda):
                if item["produto_id"] == produto["id"]:
                    # Atualiza a quantidade
                    nova_quantidade = item["quantidade"] + quantidade
                    if produto["estoque"] < nova_quantidade:
                        messagebox.showwarning("Aviso", f"Estoque insuficiente. Disponível: {produto['estoque']}")
                        return
                    
                    self.itens_venda[i]["quantidade"] = nova_quantidade
                    self.itens_venda[i]["subtotal"] = nova_quantidade * produto["preco"]
                    
                    # Atualiza a tabela
                    self.atualizar_tabela_itens()
                    self.atualizar_total()
                    return
            
            # Adiciona o novo item
            novo_item = {
                "produto_id": produto["id"],
                "codigo": produto["codigo"],
                "nome": produto["nome"],
                "quantidade": quantidade,
                "preco": produto["preco"],
                "subtotal": quantidade * produto["preco"]
            }
            
            self.itens_venda.append(novo_item)
            
            # Atualiza a tabela
            self.atualizar_tabela_itens()
            self.atualizar_total()
            
            # Limpa o campo de busca e quantidade
            self.search_var.set("")
            self.qty_var.set("1")
            
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.")
    
    def adicionar_item(self):
        """Adiciona um item à venda a partir da busca."""
        termo = self.search_var.get().strip()
        if not termo:
            messagebox.showinfo("Aviso", "Digite um código ou nome de produto.")
            return
        
        self.buscar_produto()
    
    def remover_item(self):
        """Remove um item da venda."""
        selection = self.itens_tree.selection()
        if not selection:
            messagebox.showinfo("Aviso", "Selecione um item para remover.")
            return
        
        # Obtém o índice do item na lista
        item_id = self.itens_tree.index(selection[0])
        
        # Remove o item da lista
        if 0 <= item_id < len(self.itens_venda):
            self.itens_venda.pop(item_id)
            
            # Atualiza a tabela
            self.atualizar_tabela_itens()
            self.atualizar_total()
    
    def editar_quantidade(self):
        """Edita a quantidade de um item."""
        selection = self.itens_tree.selection()
        if not selection:
            messagebox.showinfo("Aviso", "Selecione um item para editar.")
            return
        
        # Obtém o índice do item na lista
        item_id = self.itens_tree.index(selection[0])
        
        if 0 <= item_id < len(self.itens_venda):
            item = self.itens_venda[item_id]
            
            # Solicita a nova quantidade
            nova_quantidade = ctk.CTkInputDialog(
                title="Editar Quantidade",
                text=f"Nova quantidade para {item['nome']}:"
            ).get_input()
            
            if nova_quantidade:
                try:
                    nova_quantidade = float(nova_quantidade.replace(',', '.'))
                    if nova_quantidade <= 0:
                        messagebox.showinfo("Aviso", "A quantidade deve ser maior que zero.")
                        return
                    
                    # Verifica estoque se tiver controller
                    if self.controller:
                        produto = self.controller.obter_produto(item["produto_id"])
                        if produto and produto["estoque"] < nova_quantidade:
                            messagebox.showwarning("Aviso", f"Estoque insuficiente. Disponível: {produto['estoque']}")
                            return
                    
                    # Atualiza o item
                    self.itens_venda[item_id]["quantidade"] = nova_quantidade
                    self.itens_venda[item_id]["subtotal"] = nova_quantidade * item["preco"]
                    
                    # Atualiza a tabela
                    self.atualizar_tabela_itens()
                    self.atualizar_total()
                    
                except ValueError:
                    messagebox.showerror("Erro", "Quantidade inválida.")
    
    def limpar_venda(self):
        """Limpa todos os itens da venda."""
        if self.itens_venda and not messagebox.askyesno("Confirmação", "Tem certeza que deseja limpar a venda?"):
            return
        
        self.itens_venda = []
        self.total_venda = 0.0
        self.cliente_selecionado = None
        self.cliente_info_var.set("Cliente: Consumidor Final")
        self.pagamento_var.set("Dinheiro")
        self.obs_text.delete("0.0", "end")
        
        # Atualiza a tabela
        self.atualizar_tabela_itens()
        self.atualizar_total()
    
    def atualizar_tabela_itens(self):
        """Atualiza a tabela de itens."""
        # Limpa a tabela
        for item in self.itens_tree.get_children():
            self.itens_tree.delete(item)
        
        # Preenche com os itens atuais
        for item in self.itens_venda:
            self.itens_tree.insert(
                "", "end", 
                values=(
                    item["codigo"],
                    item["nome"],
                    item["quantidade"],
                    f"R$ {item['preco']:.2f}",
                    f"R$ {item['subtotal']:.2f}"
                )
            )
    
    def atualizar_total(self):
        """Atualiza o total da venda."""
        self.total_venda = sum(item["subtotal"] for item in self.itens_venda)
        self.total_var.set(f"R$ {self.total_venda:.2f}")
    
    def selecionar_cliente(self):
        """Abre a janela para selecionar um cliente."""
        # Cria uma janela de diálogo modal
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Selecionar Cliente")
        dialog.geometry("600x400")
        dialog.grab_set()
        
        # Centraliza a janela
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Selecione um Cliente", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Frame para busca
        search_frame = ctk.CTkFrame(main_frame)
        search_frame.pack(fill="x", pady=10)
        
        search_label = ctk.CTkLabel(search_frame, text="Buscar:")
        search_label.pack(side="left", padx=5)
        
        search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, textvariable=search_var, width=300)
        search_entry.pack(side="left", padx=5)
        search_entry.bind("<Return>", lambda event: buscar_cliente())
```

<File before editing>
```python
import customtkinter as ctk
from tkinter import ttk, messagebox
import datetime
from PIL import Image, ImageTk
import os

class PDVView:
    def __init__(self, parent, controller=None):
        self.parent = parent
        self.controller = controller
        self.itens_venda = []
        self.total_venda = 0.0
        self.cliente_selecionado = None
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título com estilo
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="#e74c3c", corner_radius=10)
        title_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="PONTO DE VENDA", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=10)
        
        # Frame para o conteúdo principal
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Divide em duas colunas
        left_frame = ctk.CTkFrame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        # === COLUNA ESQUERDA ===
        # Frame para busca de produtos
        search_frame = ctk.CTkFrame(left_frame)
        search_frame.pack(fill="x", padx=10, pady=10)
        
        search_label = ctk.CTkLabel(search_frame, text="Código/Nome:")
        search_label.pack(side="left", padx=5)
        
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, width=200)
        search_entry.pack(side="left", padx=5)
        search_entry.bind("<Return>", lambda event: self.buscar_produto())
        
        search_btn = ctk.CTkButton(
            search_frame, 
            text="Buscar", 
            command=self.buscar_produto,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        search_btn.pack(side="left", padx=5)
        
        # Frame para quantidade
        qty_frame = ctk.CTkFrame(left_frame)
        qty_frame.pack(fill="x", padx=10, pady=5)
        
        qty_label = ctk.CTkLabel(qty_frame, text="Quantidade:")
        qty_label.pack(side="left", padx=5)
        
        self.qty_var = ctk.StringVar(value="1")
        qty_entry = ctk.CTkEntry(qty_frame, textvariable=self.qty_var, width=80)
        qty_entry.pack(side="left", padx=5)
        
        add_btn = ctk.CTkButton(
            qty_frame, 
            text="Adicionar", 
            command=self.adicionar_item,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        add_btn.pack(side="left", padx=5)
        
        # Frame para a tabela de itens
        table_frame = ctk.CTkFrame(left_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tabela de itens
        self.itens_tree = ttk.Treeview(
            table_frame,
            columns=("codigo", "nome", "quantidade", "preco", "subtotal"),
            show="headings"
        )
        
        self.itens_tree.heading("codigo", text="Código")
        self.itens_tree.heading("nome", text="Produto")
        self.itens_tree.heading("quantidade", text="Qtd")
        self.itens_tree.heading("preco", text="Preço")
        self.itens_tree.heading("subtotal", text="Subtotal")
        
        self.itens_tree.column("codigo", width=80)
        self.itens_tree.column("nome", width=200)
        self.itens_tree.column("quantidade", width=50)
        self.itens_tree.column("preco", width=80)
        self.itens_tree.column("subtotal", width=80)
        
        # Adiciona barra de rolagem
        scrollbar = ctk.CTkScrollbar(table_frame, command=self.itens_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.itens_tree.configure(yscrollcommand=scrollbar.set)
        
        self.itens_tree.pack(fill="both", expand=True)
        
        # Botões de ação para itens
        item_actions_frame = ctk.CTkFrame(left_frame)
        item_actions_frame.pack(fill="x", padx=10, pady=5)
        
        remover_btn = ctk.CTkButton(
            item_actions_frame, 
            text="Remover Item", 
            command=self.remover_item,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        remover_btn.pack(side="left", padx=5)
        
        editar_btn = ctk.CTkButton(
            item_actions_frame, 
            text="Editar Qtd", 
            command=self.editar_quantidade,
            fg_color="#f39c12",
            hover_color="#d35400"
        )
        editar_btn.pack(side="left", padx=5)
        
        limpar_btn = ctk.CTkButton(
            item_actions_frame, 
            text="Limpar Venda", 
            command=self.limpar_venda,
            fg_color="#7f8c8d",
            hover_color="#2c3e50"
        )
        limpar_btn.pack(side="right", padx=5)
        
        # === COLUNA DIREITA ===
        # Frame para informações do cliente
        cliente_frame = ctk.CTkFrame(right_frame)
        cliente_frame.pack(fill="x", padx=10, pady=10)
        
        cliente_label = ctk.CTkLabel(
            cliente_frame, 
            text="CLIENTE", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        cliente_label.pack(pady=5)
        
        self.cliente_info_var = ctk.StringVar(value="Cliente: Consumidor Final")
        cliente_info_label = ctk.CTkLabel(cliente_frame, textvariable=self.cliente_info_var)
        cliente_info_label.pack(pady=5)
        
        cliente_btn = ctk.CTkButton(
            cliente_frame, 
            text="Selecionar Cliente", 
            command=self.selecionar_cliente,
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        )
        cliente_btn.pack(pady=5)
        
        # Frame para total da venda
        total_frame = ctk.CTkFrame(right_frame)
        total_frame.pack(fill="x", padx=10, pady=10)
        
        total_label = ctk.CTkLabel(
            total_frame, 
            text="TOTAL DA VENDA", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        total_label.pack(pady=5)
        
        self.total_var = ctk.StringVar(value="R$ 0,00")
        total_value_label = ctk.CTkLabel(
            total_frame, 
            textvariable=self.total_var,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#2ecc71"
        )
        total_value_label.pack(pady=10)
        
        # Frame para forma de pagamento
        pagamento_frame = ctk.CTkFrame(right_frame)
        pagamento_frame.pack(fill="x", padx=10, pady=10)
        
        pagamento_label = ctk.CTkLabel(
            pagamento_frame, 
            text="FORMA DE PAGAMENTO", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        pagamento_label.pack(pady=5)
        
        self.pagamento_var = ctk.StringVar(value="Dinheiro")
        pagamento_options = ["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "PIX", "Transferência"]
        
        for option in pagamento_options:
            pagamento_radio = ctk.CTkRadioButton(
                pagamento_frame,
                text=option,
                variable=self.pagamento_var,
                value=option
            )
            pagamento_radio.pack(anchor="w", padx=20, pady=2)
        
        # Frame para observações
        obs_frame = ctk.CTkFrame(right_frame)
        obs_frame.pack(fill="x", padx=10, pady=10)
        
        obs_label = ctk.CTkLabel(obs_frame, text="Observações:")
        obs_label.pack(anchor="w", padx=5, pady=2)
        
        self.obs_text = ctk.CTkTextbox(obs_frame, height=60)
        self.obs_text.pack(fill="x", padx=5, pady=2)
        
        # Frame para botões de finalização
        finish_frame = ctk.CTkFrame(right_frame)
        finish_frame.pack(fill="x", padx=10, pady=10)
        
        finish_frame.pack(fill="x", padx=10, pady=10)
        
        finalizar_btn = ctk.CTkButton(
            finish_frame, 
            text="FINALIZAR VENDA", 
            command=self.finalizar_venda,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        finalizar_btn.pack(fill="x", pady=5)
        
        cancelar_btn = ctk.CTkButton(
            finish_frame, 
            text="Cancelar Venda", 
            command=self.limpar_venda,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        cancelar_btn.pack(fill="x", pady=5)
    
    def buscar_produto(self):
        """Busca um produto pelo código ou nome."""
        termo = self.search_var.get().strip()
        if not termo:
            messagebox.showinfo("Aviso", "Digite um código ou nome de produto.")
            return
        
        # Busca o produto
        if self.controller:
            produtos = self.controller.buscar_produtos(termo)
        else:
            # Simulação para testes
            produtos = self.obter_produtos_exemplo()
            produtos = [p for p in produtos if termo.lower() in p["nome"].lower() or termo in p["codigo"]]
        
        if not produtos:
            messagebox.showinfo("Aviso", "Nenhum produto encontrado.")
            return
        
        # Se encontrou apenas um produto, adiciona diretamente
        if len(produtos) == 1:
            self.adicionar_produto(produtos[0])
        else:
            # Se encontrou vários, mostra uma janela para seleção
            self.mostrar_selecao_produtos(produtos)
    
    def mostrar_selecao_produtos(self, produtos):
        """Mostra uma janela para seleção de produtos."""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Selecionar Produto")
        dialog.geometry("600x400")
        dialog.grab_set()
        
        # Centraliza a janela
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Selecione um Produto", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Frame para a tabela
        table_frame = ctk.CTkFrame(main_frame)
        table_frame.pack(fill="both", expand=True, pady=10)
        
        # Tabela de produtos
        produtos_tree = ttk.Treeview(table_frame)
        produtos_tree["columns"] = ("codigo", "nome", "preco", "estoque")
        
        produtos_tree.heading("codigo", text="Código")
        produtos_tree.heading("nome", text="Produto")
        produtos_tree.heading("preco", text="Preço")
        produtos_tree.heading("estoque", text="Estoque")
        
        produtos_tree.column("codigo", width=100)
        produtos_tree.column("nome", width=250)
        produtos_tree.column("preco", width=100)
        produtos_tree.column("estoque", width=100)
        
        # Oculta a coluna de índice
        produtos_tree["show"] = "headings"
        
        # Adiciona barra de rolagem
        scrollbar = ctk.CTkScrollbar(table_frame, command=produtos_tree.yview)
        scrollbar.pack(side="right", fill="y")
        produtos_tree.configure(yscrollcommand=scrollbar.set)
        
        produtos_tree.pack(fill="both", expand=True)
        
        # Preenche a tabela
        for produto in produtos:
            produtos_tree.insert(
                "", "end", 
                values=(
                    produto["codigo"],
                    produto["nome"],
                    f"R$ {produto['preco']:.2f}",
                    produto["estoque"]
                ),
                tags=(str(produto["id"]),)
            )
        
        # Frame para botões
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", pady=10)
        
        def selecionar():
            selection = produtos_tree.selection()
            if not selection:
                messagebox.showinfo("Aviso", "Selecione um produto.")
                return
            
            # Obtém o ID do produto selecionado
            produto_id = produtos_tree.item(selection[0], "tags")[0]
            
            # Obtém o produto
            if self.controller:
                produto = self.controller.obter_produto(produto_id)
            else:
                # Simulação para testes
                produto = next((p for p in self.obter_produtos_exemplo() if str(p["id"]) == str(produto_id)), None)
            
            if produto:
                self.adicionar_produto