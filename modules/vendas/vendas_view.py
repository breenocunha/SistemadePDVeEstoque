import customtkinter as ctk
from tkinter import ttk, messagebox
import datetime

class VendasView:
    def __init__(self, parent, controller=None):
        self.parent = parent
        self.controller = controller
        self.itens_venda = []
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
        
        # Frame para pesquisa de produtos
        search_frame = ctk.CTkFrame(self.main_frame)
        search_frame.pack(fill="x", padx=10, pady=10)
        
        search_label = ctk.CTkLabel(search_frame, text="Código/Nome:")
        search_label.pack(side="left", padx=5)
        
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, width=300)
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
        
        # Frame para os detalhes da venda
        details_frame = ctk.CTkFrame(self.main_frame)
        details_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Divide em duas colunas
        left_frame = ctk.CTkFrame(details_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        right_frame = ctk.CTkFrame(details_frame)
        right_frame.pack(side="right", fill="y", padx=5, pady=5)
        
        # Tabela de itens da venda
        itens_label = ctk.CTkLabel(
            left_frame, 
            text="Itens da Venda", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        itens_label.pack(pady=5)
        
        self.itens_tree = ttk.Treeview(
            left_frame,
            columns=("codigo", "nome", "qtd", "preco", "total"),
            show="headings"
        )
        
        self.itens_tree.heading("codigo", text="Código")
        self.itens_tree.heading("nome", text="Produto")
        self.itens_tree.heading("qtd", text="Qtd")
        self.itens_tree.heading("preco", text="Preço Unit.")
        self.itens_tree.heading("total", text="Total")
        
        self.itens_tree.column("codigo", width=80)
        self.itens_tree.column("nome", width=200)
        self.itens_tree.column("qtd", width=50)
        self.itens_tree.column("preco", width=100)
        self.itens_tree.column("total", width=100)
        
        # Adiciona barra de rolagem
        itens_scrollbar = ctk.CTkScrollbar(left_frame, command=self.itens_tree.yview)
        itens_scrollbar.pack(side="right", fill="y")
        self.itens_tree.configure(yscrollcommand=itens_scrollbar.set)
        
        self.itens_tree.pack(fill="both", expand=True, pady=5)
        
        # Botões de ação para itens
        itens_actions_frame = ctk.CTkFrame(left_frame)
        itens_actions_frame.pack(fill="x", pady=5)
        
        add_item_btn = ctk.CTkButton(
            itens_actions_frame, 
            text="Adicionar Item", 
            command=self.adicionar_item_manual,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        add_item_btn.pack(side="left", padx=5)
        
        edit_item_btn = ctk.CTkButton(
            itens_actions_frame, 
            text="Editar Item", 
            command=self.editar_item,
            fg_color="#f39c12",
            hover_color="#d35400"
        )
        edit_item_btn.pack(side="left", padx=5)
        
        remove_item_btn = ctk.CTkButton(
            itens_actions_frame, 
            text="Remover Item", 
            command=self.remover_item,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        remove_item_btn.pack(side="left", padx=5)
        
        # Resumo da venda
        resumo_label = ctk.CTkLabel(
            right_frame, 
            text="Resumo da Venda", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        resumo_label.pack(pady=10)
        
        # Total de itens
        itens_count_frame = ctk.CTkFrame(right_frame)
        itens_count_frame.pack(fill="x", padx=10, pady=5)
        
        itens_count_label = ctk.CTkLabel(itens_count_frame, text="Total de Itens:")
        itens_count_label.pack(side="left", padx=5)
        
        self.itens_count_var = ctk.StringVar(value="0")
        itens_count_value = ctk.CTkLabel(
            itens_count_frame, 
            textvariable=self.itens_count_var,
            font=ctk.CTkFont(weight="bold")
        )
        itens_count_value.pack(side="right", padx=5)
        
        # Subtotal
        subtotal_frame = ctk.CTkFrame(right_frame)
        subtotal_frame.pack(fill="x", padx=10, pady=5)
        
        subtotal_label = ctk.CTkLabel(subtotal_frame, text="Subtotal:")
        subtotal_label.pack(side="left", padx=5)
        
        self.subtotal_var = ctk.StringVar(value="R$ 0,00")
        subtotal_value = ctk.CTkLabel(
            subtotal_frame, 
            textvariable=self.subtotal_var,
            font=ctk.CTkFont(weight="bold")
        )
        subtotal_value.pack(side="right", padx=5)
        
        # Desconto
        desconto_frame = ctk.CTkFrame(right_frame)
        desconto_frame.pack(fill="x", padx=10, pady=5)
        
        desconto_label = ctk.CTkLabel(desconto_frame, text="Desconto:")
        desconto_label.pack(side="left", padx=5)
        
        self.desconto_var = ctk.StringVar(value="0.00")
        desconto_entry = ctk.CTkEntry(
            desconto_frame, 
            textvariable=self.desconto_var,
            width=100
        )
        desconto_entry.pack(side="right", padx=5)
        desconto_entry.bind("<KeyRelease>", lambda event: self.atualizar_total())
        
        # Total
        total_frame = ctk.CTkFrame(right_frame, fg_color="#e74c3c")
        total_frame.pack(fill="x", padx=10, pady=10)
        
        total_label = ctk.CTkLabel(
            total_frame, 
            text="TOTAL:", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        )
        total_label.pack(side="left", padx=10, pady=10)
        
        self.total_var = ctk.StringVar(value="R$ 0,00")
        total_value = ctk.CTkLabel(
            total_frame, 
            textvariable=self.total_var,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        total_value.pack(side="right", padx=10, pady=10)
        
        # Forma de pagamento
        pagamento_frame = ctk.CTkFrame(right_frame)
        pagamento_frame.pack(fill="x", padx=10, pady=5)
        
        pagamento_label = ctk.CTkLabel(pagamento_frame, text="Forma de Pagamento:")
        pagamento_label.pack(side="left", padx=5)
        
        self.pagamento_var = ctk.StringVar(value="Dinheiro")
        pagamento_options = ["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "PIX", "Outros"]
        
        pagamento_combobox = ctk.CTkComboBox(
            pagamento_frame, 
            values=pagamento_options,
            variable=self.pagamento_var,
            width=150
        )
        pagamento_combobox.pack(side="right", padx=5)
        
        # Cliente
        cliente_frame = ctk.CTkFrame(right_frame)
        cliente_frame.pack(fill="x", padx=10, pady=5)
        
        cliente_label = ctk.CTkLabel(cliente_frame, text="Cliente:")
        cliente_label.pack(side="left", padx=5)
        
        self.cliente_var = ctk.StringVar(value="Consumidor Final")
        cliente_entry = ctk.CTkEntry(
            cliente_frame, 
            textvariable=self.cliente_var,
            width=150
        )
        cliente_entry.pack(side="right", padx=5)
        
        # Botões de finalização
        buttons_frame = ctk.CTkFrame(right_frame)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        finalizar_btn = ctk.CTkButton(
            buttons_frame, 
            text="Finalizar Venda", 
            command=self.finalizar_venda,
            fg_color="#27ae60",
            hover_color="#2ecc71",
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        finalizar_btn.pack(fill="x", pady=5)
        
        cancelar_btn = ctk.CTkButton(
            buttons_frame, 
            text="Cancelar Venda", 
            command=self.cancelar_venda,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        cancelar_btn.pack(fill="x", pady=5)
        
        nfce_btn = ctk.CTkButton(
            buttons_frame, 
            text="Emitir NFC-e", 
            command=self.emitir_nfce,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        nfce_btn.pack(fill="x", pady=5)
    
    def buscar_produto(self):
        """Busca um produto pelo código ou nome e adiciona à venda."""
        termo = self.search_var.get()
        if not termo:
            messagebox.showinfo("Aviso", "Digite um código ou nome de produto para buscar.")
            return
        
        # Busca o produto no controller
        if self.controller:
            produtos = self.controller.buscar_produtos(termo)
        else:
            # Dados de exemplo para testes
            produtos = self.obter_produtos_exemplo(termo)
        
        if not produtos:
            messagebox.showinfo("Aviso", "Produto não encontrado.")
            return
        
        # Se encontrou apenas um produto, adiciona diretamente
        if len(produtos) == 1:
            self.adicionar_item(produtos[0])
        else:
            # Se encontrou vários produtos, mostra uma lista para seleção
            self.mostrar_selecao_produtos(produtos)
        
        # Limpa o campo de busca
        self.search_var.set("")
    
    def mostrar_selecao_produtos(self, produtos):
        """Mostra uma janela para selecionar um produto da lista."""
        selecao_window = ctk.CTkToplevel(self.main_frame)
        selecao_window.title("Selecionar Produto")
        selecao_window.geometry("600x400")
        selecao_window.grab_set()  # Torna a janela modal
        
        # Título
        title_label = ctk.CTkLabel(
            selecao_window, 
            text="SELECIONE UM PRODUTO", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Tabela de produtos
        produtos_tree = ttk.Treeview(
            selecao_window,
            columns=("codigo", "nome", "preco", "estoque"),
            show="headings"
        )
        
        produtos_tree.heading("codigo", text="Código")
        produtos_tree.heading("nome", text="Nome")
        produtos_tree.heading("preco", text="Preço")
        produtos_tree.heading("estoque", text="Estoque")
        
        produtos_tree.column("codigo", width=80)
        produtos_tree.column("nome", width=250)
        produtos_tree.column("preco", width=100)
        produtos_tree.column("estoque", width=80)
        
        # Adiciona barra de rolagem
        scrollbar = ctk.CTkScrollbar(selecao_window, command=produtos_tree.yview)
        scrollbar.pack(side="right", fill="y")
        produtos_tree.configure(yscrollcommand=scrollbar.set)
        
        produtos_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
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
        
        # Botões
        buttons_frame = ctk.CTkFrame(selecao_window, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        selecionar_btn = ctk.CTkButton(
            buttons_frame, 
            text="Selecionar", 
            command=lambda: self.selecionar_produto(produtos_tree, produtos, selecao_window),
            fg_color="#27ae60",
            hover_color="#2ecc71"
        )
        selecionar_btn.pack(side="left", padx=5)
        
        cancelar_btn = ctk.CTkButton(
            buttons_frame, 
            text="Cancelar", 
            command=selecao_window.destroy,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        cancelar_btn.pack(side="right", padx=5)
        
        # Bind para duplo clique na tabela
        produtos_tree.bind("<Double-1>", lambda event: self.selecionar_produto(produtos_tree, produtos, selecao_window))
    
    def selecionar_produto(self, tree, produtos, window):
        """Seleciona um produto da lista e adiciona à venda."""
        selection = tree.selection()
        if not selection:
            messagebox.showinfo("Aviso", "Selecione um produto.")
            return
        
        # Obtém o ID do produto selecionado
        produto_id = tree.item(selection[0], "tags")[0]
        
        # Busca o produto na lista
        produto = None
        for p in produtos:
            if str(p["id"]) == str(produto_id):
                produto = p
                break
        
        if produto:
            window.destroy()
            self.adicionar_item(produto)
    
    def adicionar_item(self, produto):
        """Adiciona um item à venda."""
        # Verifica se o produto tem estoque
        if produto["estoque"] <= 0:
            messagebox.showinfo("Aviso", "Produto sem estoque disponível.")
            return
        
        # Pergunta a quantidade
        quantidade_dialog = ctk.CTkInputDialog(
            title="Quantidade", 
            text=f"Digite a quantidade de {produto['nome']}:"
        )
        quantidade = quantidade_dialog.get_input()
        
        if not quantidade:
            return
        
        try:
            quantidade = int(quantidade)
            if quantidade <= 0:
                raise ValueError("Quantidade deve ser maior que zero.")
            
            if quantidade > produto["estoque"]:
                messagebox.showinfo("Aviso", f"Estoque insuficiente. Disponível: {produto['estoque']}")
                return
            
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            return
        
        # Calcula o total do item
        total_item = quantidade * produto["preco"]
        
        # Verifica se o produto já está na lista
        for i, item in enumerate(self.itens_venda):
            if item["id"] == produto["id"]:
                # Atualiza a quantidade e o total
                nova_qtd = item["quantidade"] + quantidade
                if nova_qtd > produto["estoque"]:
                    messagebox.showinfo("Aviso", f"Estoque insuficiente. Disponível: {produto['estoque']}")
                    return
                
                self.itens_venda[i]["quantidade"] = nova_qtd
                self.itens_venda[i]["total"] = nova_qtd * produto["preco"]
                
                # Atualiza a tabela
                self.atualizar_tabela_itens()
                self.atualizar_total()
                return
        
        # Adiciona o item à lista
        item = {
            "id": produto["id"],
            "codigo": produto["codigo"],
            "nome": produto["nome"],
            "quantidade": quantidade,
            "preco": produto["preco"],
            "total": total_item
        }
        
        self.itens_venda.append(item)
        
        # Atualiza a tabela e o total
        self.atualizar_tabela_itens()
        self.atualizar_total()
    
    def atualizar_tabela_itens(self):
        """Atualiza a tabela de itens da venda."""
        # Limpa a tabela
        for item in self.itens_tree.get_children():
            self.itens_tree.delete(item)
        
        # Preenche a tabela
        for item in self.itens_venda:
            self.itens_tree.insert(
                "", "end", 
                values=(
                    item["codigo"],
                    item["nome"],
                    item["quantidade"],
                    f"R$ {item['preco']:.2f}",
                    f"R$ {item['total']:.2f}"
                ),
                tags=(str(item["id"]),)
            )
    
    def atualizar_total(self):
        """Atualiza os totais da venda."""
        # Calcula o subtotal
        subtotal = sum(item["total"] for item in self.itens_venda)
        
        # Calcula o desconto
        try:
            desconto = float(self.desconto_var.get().replace(",", "."))
        except ValueError:
            desconto = 0
        
        # Calcula o total
        total = subtotal - desconto
        if total < 0:
            total = 0
        
        # Atualiza os campos
        self.itens_count_var.set(str(sum(item["quantidade"] for item in self.itens_venda)))
        self.subtotal_var.set(f"R$ {subtotal:.2f}")
        self.total_var.set(f"R$ {total:.2f}")
    
    def adicionar_item_manual(self):
        """Abre uma janela para adicionar um item manualmente."""
        # Implementação futura
        messagebox.showinfo("Aviso", "Funcionalidade em desenvolvimento.")
    
    def editar_item(self):
        """Edita o item selecionado."""
        selection = self.itens_tree.selection()
        if not selection:
            messagebox.showinfo("Aviso", "Selecione um item para editar.")
            return
        
        # Obtém o ID do item selecionado
        item_id = self.itens_tree.item(selection[0], "tags")[0]
        
        # Busca o item na lista
        item_index = None
        for i, item in enumerate(self.itens_venda):
            if str(item["id"]) == str(item_id):
                item_index = i
                break
        
        if item_index is None:
            return
        
        # Pergunta a nova quantidade
        quantidade_dialog = ctk.CTkInputDialog(
            title="Editar Quantidade", 
            text=f"Digite a nova quantidade de {self.itens_venda[item_index]['nome']}:"
        )
        quantidade = quantidade_dialog.get_input()
        
        if not quantidade:
            return
        
        try:
            quantidade = int(quantidade)
            if quantidade <= 0:
                raise ValueError("Quantidade deve ser maior que zero.")
            
            # Verifica o estoque disponível
            if self.controller:
                produto = self.controller.obter_produto(item_id)
            else:
                # Dados de exemplo para testes
                produtos = self.obter_produtos_exemplo()
                produto = next((p for p in produtos if str(p["id"]) == str(item_id)), None)
            
            if produto and quantidade > produto["estoque"]:
                messagebox.showinfo("Aviso", f"Estoque insuficiente. Disponível: {produto['estoque']}")
                return
            
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            return
        
        # Atualiza o item
        self.itens_venda[item_index]["quantidade"] = quantidade
        self.itens_venda[item_index]["total"] = quantidade * self.itens_venda[item_index]["preco"]
        
        # Atualiza a tabela e o total
        self.atualizar_tabela_itens()
        self.atualizar_total()
    
    def remover_item(self):
        """Remove o item selecionado."""
        selection = self.itens_tree.selection()
        if not selection:
            messagebox.showinfo("Aviso", "Selecione um item para remover.")
            return
        
        # Obtém o ID do item selecionado
        item_id = self.itens_tree.item(selection[0], "tags")[0]
        
        # Remove o item da lista
        self.itens_venda = [item for item in self.itens_venda if str(item["id"]) != str(item_id)]
        
        # Atualiza a tabela e o total
        self.atualizar_tabela_itens()
        self.atualizar_total()
    
    def finalizar_venda(self):
        """Finaliza a venda atual."""
        if not self.itens_venda:
            messagebox.showinfo("Aviso", "Adicione pelo menos um item à venda.")
            return
        
        # Calcula o total
        subtotal = sum(item["total"] for item in self.itens_venda)
        
        try:
            desconto = float(self.desconto_var.get().replace(",", "."))
        except ValueError:
            desconto = 0
        
        total = subtotal - desconto
        if total < 0:
            total = 0
        
        # Confirma a finalização
        if not messagebox.askyesno("Confirmação", f"Deseja finalizar a venda no valor de R$ {total:.2f}?"):
            return
        
        # Prepara os dados da venda
        venda_data = {
            "data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cliente": self.cliente_var.get(),
            "forma_pagamento": self.pagamento_var.get(),
            "subtotal": subtotal,
            "desconto": desconto,
            "total": total,
            "itens": self.itens_venda
        }
        
        # Salva a venda no controller
        if self.controller:
            resultado = self.controller.salvar_venda(venda_data)
            if resultado.get("sucesso", False):
                venda_id = resultado.get("id")
                messagebox.showinfo("Sucesso", f"Venda #{venda_id} finalizada com sucesso!")
                
                # Pergunta se deseja emitir NFC-e
                if messagebox.askyesno("NFC-e", "Deseja emitir NFC-e para esta venda?"):
                    self.emitir_nfce(venda_id)
                
                # Limpa a venda atual
                self.nova_venda()
            else:
                messagebox.showerror("Erro", resultado.get("mensagem", "Erro ao finalizar venda."))
        else:
            # Simulação para testes
            messagebox.showinfo("Sucesso", "Venda finalizada com sucesso!")
            self.nova_venda()
    
    def cancelar_venda(self):
        """Cancela a venda atual."""
        if not self.itens_venda:
            messagebox.showinfo("Aviso", "Não há venda em andamento.")
            return
        
        # Confirma o cancelamento
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja cancelar esta venda?"):
            self.nova_venda()
    
    def nova_venda(self):
        """Inicia uma nova venda."""
        # Limpa os itens
        self.itens_venda = []
        
        # Limpa a tabela
        for item in self.itens_tree.get_children():
            self.itens_tree.delete(item)
        
        # Reseta os campos
        self.desconto_var.set("0.00")
        self.cliente_var.set("Consumidor Final")
        self.pagamento_var.set("Dinheiro")
        
        # Atualiza os totais
        self.atualizar_total()
    
    def emitir_nfce(self, venda_id=None):
        """Emite uma NFC-e para a venda atual ou para uma venda específica."""
        if not venda_id and not self.itens_venda:
            messagebox.showinfo("Aviso", "Não há venda em andamento.")
            return
        
        # Se não foi informado um ID de venda, usa a venda atual
        if not venda_id:
            # Finaliza a venda primeiro
            self.finalizar_venda()
            return
        
        # Abre o formulário de NFC-e
        try:
            from modules.fiscal.nfce_form import NFCeForm
            NFCeForm(self.parent, self.controller, venda_id)
        except ImportError:
            messagebox.showerror("Erro", "Módulo fiscal não encontrado.")
    
    def obter_produtos_exemplo(self, termo=None):
        """Retorna dados de exemplo para os produtos."""
        produtos = [
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
        
        if termo:
            termo = termo.lower()
            return [p for p in produtos 
                   if termo in p["nome"].lower() or 
                      termo in p["codigo"].lower() or
                      termo in p["categoria"].lower()]
        
        return produtos