import customtkinter as ctk
from tkinter import ttk, messagebox
import datetime

class ClientesView:
    def __init__(self, parent, controller=None):
        self.parent = parent
        self.controller = controller
        self.setup_ui()
        self.carregar_clientes()
    
    def setup_ui(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título com estilo
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="#2ecc71", corner_radius=10)
        title_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="CADASTRO DE CLIENTES", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=10)
        
        # Frame para pesquisa e botões
        actions_frame = ctk.CTkFrame(self.main_frame)
        actions_frame.pack(fill="x", padx=10, pady=10)
        
        # Campo de pesquisa
        search_frame = ctk.CTkFrame(actions_frame)
        search_frame.pack(side="left", fill="x", expand=True)
        
        search_label = ctk.CTkLabel(search_frame, text="Buscar cliente:")
        search_label.pack(side="left", padx=5)
        
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, width=300)
        search_entry.pack(side="left", padx=5)
        
        search_button = ctk.CTkButton(
            search_frame, 
            text="Buscar", 
            command=self.buscar_clientes,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        search_button.pack(side="left", padx=5)
        
        # Botões de ação
        buttons_frame = ctk.CTkFrame(actions_frame)
        buttons_frame.pack(side="right")
        
        novo_btn = ctk.CTkButton(
            buttons_frame, 
            text="Novo Cliente", 
            command=lambda: self.abrir_form_cliente(),
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=120
        )
        novo_btn.pack(side="left", padx=5)
        
        editar_btn = ctk.CTkButton(
            buttons_frame, 
            text="Editar", 
            command=self.editar_cliente,
            fg_color="#3498db",
            hover_color="#2980b9",
            width=120
        )
        editar_btn.pack(side="left", padx=5)
        
        excluir_btn = ctk.CTkButton(
            buttons_frame, 
            text="Excluir", 
            command=self.excluir_cliente,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            width=120
        )
        excluir_btn.pack(side="left", padx=5)
        
        # Frame para a tabela de clientes
        table_frame = ctk.CTkFrame(self.main_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tabela de clientes
        self.clientes_tree = ttk.Treeview(table_frame)
        self.clientes_tree["columns"] = ("id", "nome", "cpf", "telefone", "email")
        
        self.clientes_tree.heading("id", text="ID")
        self.clientes_tree.heading("nome", text="Nome")
        self.clientes_tree.heading("cpf", text="CPF")
        self.clientes_tree.heading("telefone", text="Telefone")
        self.clientes_tree.heading("email", text="Email")
        
        self.clientes_tree.column("id", width=50)
        self.clientes_tree.column("nome", width=250)
        self.clientes_tree.column("cpf", width=150)
        self.clientes_tree.column("telefone", width=150)
        self.clientes_tree.column("email", width=200)
        
        # Oculta a coluna de índice
        self.clientes_tree["show"] = "headings"
        
        # Adiciona barra de rolagem
        scrollbar = ctk.CTkScrollbar(table_frame, command=self.clientes_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.clientes_tree.configure(yscrollcommand=scrollbar.set)
        
        self.clientes_tree.pack(fill="both", expand=True)
        
        # Bind de duplo clique para editar
        self.clientes_tree.bind("<Double-1>", lambda event: self.editar_cliente())
    
    def carregar_clientes(self):
        """Carrega todos os clientes na tabela."""
        # Limpa a tabela
        for item in self.clientes_tree.get_children():
            self.clientes_tree.delete(item)
        
        if self.controller:
            clientes = self.controller.listar_clientes()
        else:
            # Dados de exemplo para testes
            clientes = self.obter_clientes_exemplo()
        
        # Preenche a tabela
        for cliente in clientes:
            self.clientes_tree.insert(
                "", "end", 
                values=(
                    cliente["id"],
                    cliente["nome"],
                    cliente.get("cpf", ""),
                    cliente.get("telefone", ""),
                    cliente.get("email", "")
                ),
                tags=(str(cliente["id"]),)
            )
    
    def buscar_clientes(self):
        """Busca clientes pelo termo de pesquisa."""
        termo = self.search_var.get()
        
        # Limpa a tabela
        for item in self.clientes_tree.get_children():
            self.clientes_tree.delete(item)
        
        if not termo:
            self.carregar_clientes()
            return
        
        if self.controller:
            clientes = self.controller.buscar_clientes(termo)
        else:
            # Simulação para testes
            clientes = [c for c in self.obter_clientes_exemplo() 
                       if termo.lower() in c["nome"].lower() 
                       or (c.get("cpf") and termo in c["cpf"])
                       or (c.get("telefone") and termo in c["telefone"])
                       or (c.get("email") and termo.lower() in c["email"].lower())]
        
        # Preenche a tabela
        for cliente in clientes:
            self.clientes_tree.insert(
                "", "end", 
                values=(
                    cliente["id"],
                    cliente["nome"],
                    cliente.get("cpf", ""),
                    cliente.get("telefone", ""),
                    cliente.get("email", "")
                ),
                tags=(str(cliente["id"]),)
            )
    
    def abrir_form_cliente(self, cliente_id=None):
        """Abre o formulário para adicionar ou editar um cliente."""
        # Cria uma janela de diálogo modal
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Novo Cliente" if not cliente_id else "Editar Cliente")
        dialog.geometry("500x400")  # Tamanho adequado para mostrar todos os campos
        dialog.minsize(500, 400)    # Tamanho mínimo para garantir que todos os campos sejam visíveis
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
        ClienteForm(dialog, self, cliente_id)
    
    def editar_cliente(self):
        """Edita o cliente selecionado."""
        selection = self.clientes_tree.selection()
        if not selection:
            messagebox.showinfo("Aviso", "Selecione um cliente para editar.")
            return
        
        # Obtém o ID do cliente selecionado
        cliente_id = self.clientes_tree.item(selection[0], "tags")[0]
        
        # Verifica se o ID é válido
        if not cliente_id:
            messagebox.showerror("Erro", "ID do cliente inválido.")
            return
            
        print(f"Editando cliente com ID: {cliente_id}")
        
        # Abre o formulário para edição
        self.abrir_form_cliente(cliente_id)
    
    def excluir_cliente(self):
        """Exclui o cliente selecionado."""
        selection = self.clientes_tree.selection()
        if not selection:
            messagebox.showinfo("Aviso", "Selecione um cliente para excluir.")
            return
        
        # Confirmação
        if not messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este cliente?"):
            return
        
        # Obtém o ID do cliente selecionado
        cliente_id = self.clientes_tree.item(selection[0], "tags")[0]
        
        # Exclui o cliente
        if self.controller:
            resultado = self.controller.excluir_cliente(cliente_id)
            if resultado.get("sucesso", False):
                messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
                self.carregar_clientes()
            else:
                messagebox.showerror("Erro", resultado.get("mensagem", "Erro ao excluir cliente."))
        else:
            # Simulação para testes
            messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
            self.carregar_clientes()
    
    def salvar_cliente(self, cliente_data):
        """Salva um cliente (novo ou editado)."""
        if self.controller:
            if cliente_data.get("id"):
                resultado = self.controller.atualizar_cliente(cliente_data)
            else:
                resultado = self.controller.inserir_cliente(cliente_data)
            
            if resultado.get("sucesso", False):
                messagebox.showinfo("Sucesso", "Cliente salvo com sucesso!")
                self.carregar_clientes()
                return True
            else:
                messagebox.showerror("Erro", resultado.get("mensagem", "Erro ao salvar cliente."))
                return False
        else:
            # Simulação para testes
            messagebox.showinfo("Sucesso", "Cliente salvo com sucesso!")
            self.carregar_clientes()
            return True
    
    def obter_cliente(self, cliente_id):
        """Obtém os dados de um cliente pelo ID."""
        if self.controller:
            return self.controller.obter_cliente(cliente_id)
        else:
            # Dados de exemplo para testes
            clientes = self.obter_clientes_exemplo()
            for cliente in clientes:
                if str(cliente["id"]) == str(cliente_id):
                    return cliente
            return None
    
    def obter_clientes_exemplo(self):
        """Retorna dados de exemplo para os clientes."""
        return [
            {
                "id": 1,
                "nome": "João Silva",
                "cpf": "123.456.789-00",
                "telefone": "(11) 98765-4321",
                "email": "joao.silva@email.com",
                "endereco": "Rua A, 123",
                "data_cadastro": "01/01/2023"
            },
            {
                "id": 2,
                "nome": "Maria Oliveira",
                "cpf": "987.654.321-00",
                "telefone": "(11) 91234-5678",
                "email": "maria.oliveira@email.com",
                "endereco": "Av. B, 456",
                "data_cadastro": "15/02/2023"
            },
            {
                "id": 3,
                "nome": "Pedro Santos",
                "cpf": "456.789.123-00",
                "telefone": "(11) 92345-6789",
                "email": "pedro.santos@email.com",
                "endereco": "Rua C, 789",
                "data_cadastro": "10/03/2023"
            }
        ]


class ClienteForm:
    def __init__(self, parent, view, cliente_id=None):
        self.parent = parent
        self.view = view
        self.cliente_id = cliente_id
        self.setup_ui()
        
        # Carrega os dados do cliente se for edição
        if cliente_id:
            self.carregar_dados_cliente()
    
    def setup_ui(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Dados do Cliente", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Campos do formulário
        # Nome
        nome_frame = ctk.CTkFrame(self.main_frame)
        nome_frame.pack(fill="x", pady=5)
        
        nome_label = ctk.CTkLabel(nome_frame, text="Nome:", width=100, anchor="w")
        nome_label.pack(side="left")
        
        self.nome_var = ctk.StringVar()
        nome_entry = ctk.CTkEntry(nome_frame, textvariable=self.nome_var, width=350)
        nome_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # CPF
        cpf_frame = ctk.CTkFrame(self.main_frame)
        cpf_frame.pack(fill="x", pady=5)
        
        cpf_label = ctk.CTkLabel(cpf_frame, text="CPF:", width=100, anchor="w")
        cpf_label.pack(side="left")
        
        self.cpf_var = ctk.StringVar()
        cpf_entry = ctk.CTkEntry(cpf_frame, textvariable=self.cpf_var, width=200)
        cpf_entry.pack(side="left", padx=5)
        
        # Telefone
        telefone_frame = ctk.CTkFrame(self.main_frame)
        telefone_frame.pack(fill="x", pady=5)
        
        telefone_label = ctk.CTkLabel(telefone_frame, text="Telefone:", width=100, anchor="w")
        telefone_label.pack(side="left")
        
        self.telefone_var = ctk.StringVar()
        telefone_entry = ctk.CTkEntry(telefone_frame, textvariable=self.telefone_var, width=200)
        telefone_entry.pack(side="left", padx=5)
        
        # Email
        email_frame = ctk.CTkFrame(self.main_frame)
        email_frame.pack(fill="x", pady=5)
        
        email_label = ctk.CTkLabel(email_frame, text="Email:", width=100, anchor="w")
        email_label.pack(side="left")
        
        self.email_var = ctk.StringVar()
        email_entry = ctk.CTkEntry(email_frame, textvariable=self.email_var, width=350)
        email_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Endereço
        endereco_frame = ctk.CTkFrame(self.main_frame)
        endereco_frame.pack(fill="x", pady=5)
        
        endereco_label = ctk.CTkLabel(endereco_frame, text="Endereço:", width=100, anchor="w")
        endereco_label.pack(side="left")
        
        self.endereco_var = ctk.StringVar()
        endereco_entry = ctk.CTkEntry(endereco_frame, textvariable=self.endereco_var, width=350)
        endereco_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Botões
        buttons_frame = ctk.CTkFrame(self.main_frame)
        buttons_frame.pack(fill="x", pady=20)
        
        cancelar_btn = ctk.CTkButton(
            buttons_frame, 
            text="Cancelar", 
            command=self.parent.destroy,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            width=120
        )
        cancelar_btn.pack(side="right", padx=5)
        
        salvar_btn = ctk.CTkButton(
            buttons_frame, 
            text="Salvar", 
            command=self.salvar_cliente,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=120
        )
        salvar_btn.pack(side="right", padx=5)
    
    def carregar_dados_cliente(self):
        """Carrega os dados do cliente para edição."""
        cliente = self.view.obter_cliente(self.cliente_id)
        if not cliente:
            messagebox.showerror("Erro", "Cliente não encontrado.")
            self.parent.destroy()
            return
        
        # Preenche os campos com os dados do cliente
        self.nome_var.set(cliente.get("nome", ""))
        self.cpf_var.set(cliente.get("cpf", ""))
        self.telefone_var.set(cliente.get("telefone", ""))
        self.email_var.set(cliente.get("email", ""))
        self.endereco_var.set(cliente.get("endereco", ""))
    
    def salvar_cliente(self):
        """Salva os dados do cliente."""
        # Validação básica
        nome = self.nome_var.get().strip()
        if not nome:
            messagebox.showerror("Erro", "O nome do cliente é obrigatório.")
            return
        
        # Monta os dados do cliente
        cliente_data = {
            "nome": nome,
            "cpf": self.cpf_var.get().strip(),
            "telefone": self.telefone_var.get().strip(),
            "email": self.email_var.get().strip(),
            "endereco": self.endereco_var.get().strip(),
        }
        
        # Adiciona o ID se for edição
        if self.cliente_id:
            cliente_data["id"] = self.cliente_id
        
        # Salva o cliente
        if self.view.salvar_cliente(cliente_data):
            self.parent.destroy()