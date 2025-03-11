import customtkinter as ctk
from tkinter import ttk, messagebox
import datetime

class NFCeForm:
    def __init__(self, parent, controller, venda_id):
        self.parent = parent
        self.controller = controller
        self.venda_id = venda_id
        self.setup_ui()
    
    def setup_ui(self):
        # Cria uma nova janela
        self.nfce_window = ctk.CTkToplevel(self.parent)
        self.nfce_window.title("Emissão de NFC-e")
        self.nfce_window.geometry("600x500")
        self.nfce_window.grab_set()  # Torna a janela modal
        
        # Título
        title_label = ctk.CTkLabel(
            self.nfce_window, 
            text="EMISSÃO DE NFC-e", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.nfce_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Dados da venda
        venda_frame = ctk.CTkFrame(main_frame)
        venda_frame.pack(fill="x", padx=10, pady=10)
        
        venda_label = ctk.CTkLabel(
            venda_frame, 
            text="Dados da Venda", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        venda_label.pack(pady=5)
        
        # Carrega os dados da venda
        if self.controller:
            venda = self.controller.obter_venda(self.venda_id)
        else:
            # Dados de exemplo para testes
            venda = self.obter_venda_exemplo()
        
        if not venda:
            messagebox.showerror("Erro", "Venda não encontrada.")
            self.nfce_window.destroy()
            return
        
        # Número da venda
        venda_id_frame = ctk.CTkFrame(venda_frame)
        venda_id_frame.pack(fill="x", pady=5)
        
        venda_id_label = ctk.CTkLabel(venda_id_frame, text="Número da Venda:")
        venda_id_label.pack(side="left", padx=5)
        
        venda_id_value = ctk.CTkLabel(
            venda_id_frame, 
            text=str(venda["id"]),
            font=ctk.CTkFont(weight="bold")
        )
        venda_id_value.pack(side="left", padx=5)
        
        # Data da venda
        data_frame = ctk.CTkFrame(venda_frame)
        data_frame.pack(fill="x", pady=5)
        
        data_label = ctk.CTkLabel(data_frame, text="Data da Venda:")
        data_label.pack(side="left", padx=5)
        
        data_value = ctk.CTkLabel(
            data_frame, 
            text=venda["data"],
            font=ctk.CTkFont(weight="bold")
        )
        data_value.pack(side="left", padx=5)
        
        # Total da venda
        total_frame = ctk.CTkFrame(venda_frame)
        total_frame.pack(fill="x", pady=5)
        
        total_label = ctk.CTkLabel(total_frame, text="Total da Venda:")
        total_label.pack(side="left", padx=5)
        
        total_value = ctk.CTkLabel(
            total_frame, 
            text=f"R$ {venda['total']:.2f}",
            font=ctk.CTkFont(weight="bold")
        )
        total_value.pack(side="left", padx=5)
        
        # Cliente
        cliente_frame = ctk.CTkFrame(venda_frame)
        cliente_frame.pack(fill="x", pady=5)
        
        cliente_label = ctk.CTkLabel(cliente_frame, text="Cliente:")
        cliente_label.pack(side="left", padx=5)
        
        self.cliente_var = ctk.StringVar(value=venda.get("cliente", "Consumidor Final"))
        cliente_entry = ctk.CTkEntry(
            cliente_frame, 
            textvariable=self.cliente_var,
            width=300
        )
        cliente_entry.pack(side="left", padx=5)
        
        # CPF/CNPJ
        cpf_frame = ctk.CTkFrame(venda_frame)
        cpf_frame.pack(fill="x", pady=5)
        
        cpf_label = ctk.CTkLabel(cpf_frame, text="CPF/CNPJ:")
        cpf_label.pack(side="left", padx=5)
        
        self.cpf_var = ctk.StringVar()
        cpf_entry = ctk.CTkEntry(
            cpf_frame, 
            textvariable=self.cpf_var,
            width=150
        )
        cpf_entry.pack(side="left", padx=5)
        
        # Itens da venda
        itens_frame = ctk.CTkFrame(main_frame)
        itens_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        itens_label = ctk.CTkLabel(
            itens_frame, 
            text="Itens da Venda", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        itens_label.pack(pady=5)
        
        # Tabela de itens
        self.itens_tree = ttk.Treeview(
            itens_frame,
            columns=("codigo", "nome", "qtd", "preco", "total"),
            show="headings",
            height=5
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
        itens_scrollbar = ctk.CTkScrollbar(itens_frame, command=self.itens_tree.yview)
        itens_scrollbar.pack(side="right", fill="y")
        self.itens_tree.configure(yscrollcommand=itens_scrollbar.set)
        
        self.itens_tree.pack(fill="both", expand=True, pady=5)
        
        # Preenche a tabela de itens
        for item in venda.get("itens", []):
            self.itens_tree.insert(
                "", "end", 
                values=(
                    item["codigo"],
                    item["nome"],
                    item["quantidade"],
                    f"R$ {item['preco']:.2f}",
                    f"R$ {item['total']:.2f}"
                )
            )
        
        # Botões
        buttons_frame = ctk.CTkFrame(self.nfce_window, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        emitir_btn = ctk.CTkButton(
            buttons_frame, 
            text="Emitir NFC-e", 
            command=self.emitir_nfce,
            fg_color="#27ae60",
            hover_color="#2ecc71",
            width=150
        )
        emitir_btn.pack(side="left", padx=5)
        
        cancelar_btn = ctk.CTkButton(
            buttons_frame, 
            text="Cancelar", 
            command=self.nfce_window.destroy,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            width=150
        )
        cancelar_btn.pack(side="right", padx=5)
    
    def emitir_nfce(self):
        """Emite a NFC-e."""
        # Valida o CPF/CNPJ
        cpf_cnpj = self.cpf_var.get().strip()
        if cpf_cnpj and not self.validar_cpf_cnpj(cpf_cnpj):
            messagebox.showerror("Erro", "CPF/CNPJ inválido.")
            return
        
        # Confirma a emissão
        if not messagebox.askyesno("Confirmação", "Deseja emitir a NFC-e?"):
            return
        
        # Carrega os dados da venda
        if self.controller:
            venda = self.controller.obter_venda(self.venda_id)
        else:
            # Simulação para testes
            resultado = {
                "sucesso": True,
                "numero": f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                "chave_acesso": f"NFCe{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{'0' * 34}",
                "protocolo": f"PROT{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            }
            
            messagebox.showinfo(
                "Sucesso", 
                f"NFC-e emitida com sucesso! (SIMULAÇÃO)\n\n"
                f"Número: {resultado['numero']}\n"
                f"Chave de Acesso: {resultado['chave_acesso']}\n"
                f"Protocolo: {resultado['protocolo']}"
            )
            self.nfce_window.destroy()
        
        def validar_cpf_cnpj(self, cpf_cnpj):
            """Valida um CPF ou CNPJ."""
            # Remove caracteres não numéricos
            cpf_cnpj = ''.join(filter(str.isdigit, cpf_cnpj))
            
            # Verifica se é um CPF (11 dígitos)
            if len(cpf_cnpj) == 11:
                return self.validar_cpf(cpf_cnpj)
            
            # Verifica se é um CNPJ (14 dígitos)
            elif len(cpf_cnpj) == 14:
                return self.validar_cnpj(cpf_cnpj)
            
            return False
        
        def validar_cpf(self, cpf):
            """Valida um CPF."""
            # Verifica se todos os dígitos são iguais
            if len(set(cpf)) == 1:
                return False
            
            # Calcula o primeiro dígito verificador
            soma = 0
            for i in range(9):
                soma += int(cpf[i]) * (10 - i)
            
            resto = soma % 11
            digito1 = 0 if resto < 2 else 11 - resto
            
            # Verifica o primeiro dígito verificador
            if digito1 != int(cpf[9]):
                return False
            
            # Calcula o segundo dígito verificador
            soma = 0
            for i in range(10):
                soma += int(cpf[i]) * (11 - i)
            
            resto = soma % 11
            digito2 = 0 if resto < 2 else 11 - resto
            
            # Verifica o segundo dígito verificador
            return digito2 == int(cpf[10])
        
        def validar_cnpj(self, cnpj):
            """Valida um CNPJ."""
            # Verifica se todos os dígitos são iguais
            if len(set(cnpj)) == 1:
                return False
            
            # Calcula o primeiro dígito verificador
            pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            soma = 0
            for i in range(12):
                soma += int(cnpj[i]) * pesos[i]
            
            resto = soma % 11
            digito1 = 0 if resto < 2 else 11 - resto
            
            # Verifica o primeiro dígito verificador
            if digito1 != int(cnpj[12]):
                return False
            
            # Calcula o segundo dígito verificador
            pesos = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            soma = 0
            for i in range(13):
                soma += int(cnpj[i]) * pesos[i]
            
            resto = soma % 11
            digito2 = 0 if resto < 2 else 11 - resto
            
            # Verifica o segundo dígito verificador
            return digito2 == int(cnpj[13])
        
        def obter_venda_exemplo(self):
            """Retorna dados de exemplo para uma venda."""
            return {
                "id": 1,
                "data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "cliente": "Consumidor Final",
                "forma_pagamento": "Dinheiro",
                "subtotal": 100.00,
                "desconto": 0.00,
                "total": 100.00,
                "itens": [
                    {
                        "id": 1,
                        "codigo": "P001",
                        "nome": "Produto 1",
                        "quantidade": 2,
                        "preco": 25.00,
                        "total": 50.00
                    },
                    {
                        "id": 2,
                        "codigo": "P002",
                        "nome": "Produto 2",
                        "quantidade": 1,
                        "preco": 50.00,
                        "total": 50.00
                    }
                ]
            }