import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import datetime
import csv
import os

class HistoricoVendasView:
    def __init__(self, parent, controller=None):
        self.parent = parent
        self.controller = controller
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface do usuário."""
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título com estilo
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="#2ecc71", corner_radius=10)
        title_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="HISTÓRICO DE VENDAS", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=10)
        
        # Frame de filtros
        filtros_frame = ctk.CTkFrame(self.main_frame)
        filtros_frame.pack(fill="x", padx=10, pady=10)
        
        # Período
        periodo_label = ctk.CTkLabel(filtros_frame, text="Período:")
        periodo_label.pack(side="left", padx=5)
        
        self.data_inicial_var = ctk.StringVar(value=(datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%d/%m/%Y"))
        data_inicial_entry = ctk.CTkEntry(
            filtros_frame, 
            textvariable=self.data_inicial_var,
            width=100
        )
        data_inicial_entry.pack(side="left", padx=5)
        
        ate_label = ctk.CTkLabel(filtros_frame, text="até")
        ate_label.pack(side="left", padx=5)
        
        self.data_final_var = ctk.StringVar(value=datetime.datetime.now().strftime("%d/%m/%Y"))
        data_final_entry = ctk.CTkEntry(
            filtros_frame, 
            textvariable=self.data_final_var,
            width=100
        )
        data_final_entry.pack(side="left", padx=5)
        
        # Status
        status_label = ctk.CTkLabel(filtros_frame, text="Status:")
        status_label.pack(side="left", padx=5)
        
        self.status_var = ctk.StringVar(value="Todos")
        status_options = ["Todos", "Concluída", "Cancelada", "Pendente"]
        
        status_combobox = ctk.CTkComboBox(
            filtros_frame, 
            values=status_options,
            variable=self.status_var,
            width=150
        )
        status_combobox.pack(side="left", padx=5)
        
        # Cliente
        cliente_label = ctk.CTkLabel(filtros_frame, text="Cliente:")
        cliente_label.pack(side="left", padx=5)
        
        self.cliente_var = ctk.StringVar()
        cliente_entry = ctk.CTkEntry(
            filtros_frame, 
            textvariable=self.cliente_var,
            width=150,
            placeholder_text="Nome ou CPF"
        )
        cliente_entry.pack(side="left", padx=5)
        
        # Botão de filtrar
        filtrar_btn = ctk.CTkButton(
            filtros_frame, 
            text="Filtrar", 
            command=self.filtrar_vendas,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        filtrar_btn.pack(side="right", padx=5)
        
        # Tabela de vendas
        self.vendas_tree = ttk.Treeview(
            self.main_frame,
            columns=("id", "data", "cliente", "itens", "total", "pagamento", "status"),
            show="headings"
        )
        
        self.vendas_tree.heading("id", text="ID")
        self.vendas_tree.heading("data", text="Data")
        self.vendas_tree.heading("cliente", text="Cliente")
        self.vendas_tree.heading("itens", text="Itens")
        self.vendas_tree.heading("total", text="Total")
        self.vendas_tree.heading("pagamento", text="Pagamento")
        self.vendas_tree.heading("status", text="Status")
        
        self.vendas_tree.column("id", width=50)
        self.vendas_tree.column("data", width=150)
        self.vendas_tree.column("cliente", width=200)
        self.vendas_tree.column("itens", width=100)
        self.vendas_tree.column("total", width=100)
        self.vendas_tree.column("pagamento", width=150)
        self.vendas_tree.column("status", width=100)
        
        # Adiciona barra de rolagem
        vendas_scrollbar = ctk.CTkScrollbar(self.main_frame, command=self.vendas_tree.yview)
        vendas_scrollbar.pack(side="right", fill="y")
        self.vendas_tree.configure(yscrollcommand=vendas_scrollbar.set)
        
        self.vendas_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Resumo
        self.resumo_frame = ctk.CTkFrame(self.main_frame)
        self.resumo_frame.pack(fill="x", padx=10, pady=10)
        
        self.resumo_label = ctk.CTkLabel(
            self.resumo_frame, 
            text="Total: R$ 0,00 | Quantidade: 0",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.resumo_label.pack(side="left", padx=10)
        
        # Botões de ação
        actions_frame = ctk.CTkFrame(self.main_frame)
        actions_frame.pack(fill="x", padx=10, pady=10)
        
        visualizar_btn = ctk.CTkButton(
            actions_frame, 
            text="Visualizar Detalhes", 
            command=self.visualizar_venda,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        visualizar_btn.pack(side="left", padx=5)
        
        imprimir_btn = ctk.CTkButton(
            actions_frame, 
            text="Imprimir Comprovante", 
            command=self.imprimir_comprovante,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        imprimir_btn.pack(side="left", padx=5)
        
        cancelar_btn = ctk.CTkButton(
            actions_frame, 
            text="Cancelar Venda", 
            command=self.cancelar_venda,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        cancelar_btn.pack(side="left", padx=5)
        
        exportar_btn = ctk.CTkButton(
            actions_frame, 
            text="Exportar CSV", 
            command=self.exportar_csv,
            fg_color="#f39c12",
            hover_color="#d35400"
        )
        exportar_btn.pack(side="right", padx=5)
        
        # Carrega os dados iniciais
        self.carregar_vendas()
    
    def carregar_vendas(self):
        """Carrega as vendas na tabela."""
        # Limpa a tabela
        for item in self.vendas_tree.get_children():
            self.vendas_tree.delete(item)
        
        try:
            # Converte as datas para o formato do banco
            data_inicial = datetime.datetime.strptime(self.data_inicial_var.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
            data_final = datetime.datetime.strptime(self.data_final_var.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
            data_final += " 23:59:59"  # Inclui o último dia inteiro
            
            # Prepara os filtros
            filtros = {
                "data_inicial": data_inicial,
                "data_final": data_final
            }
            
            # Adiciona filtro de status se necessário
            if self.status_var.get() != "Todos":
                filtros["status"] = self.status_var.get()
            
            # Adiciona filtro de cliente se necessário
            if self.cliente_var.get():
                filtros["cliente"] = self.cliente_var.get()
            
            # Obtém as vendas do controller
            if self.controller:
                vendas = self.controller.listar_vendas(filtros)
            else:
                # Dados de exemplo para testes
                vendas = self.obter_vendas_exemplo()
            
            # Preenche a tabela
            total_geral = 0
            for venda in vendas:
                # Obtém o nome do cliente
                cliente_nome = venda.get("cliente_nome", "Consumidor Final")
                
                # Obtém a quantidade de itens
                itens_count = venda.get("itens_count", 0)
                
                # Formata o valor total
                total = venda.get("total", 0)
                total_geral += total
                
                # Define a cor conforme o status
                tag = venda.get("status", "").lower()
                
                self.vendas_tree.insert(
                    "", "end", 
                    values=(
                        venda.get("id", ""),
                        venda.get("data", "").split(" ")[0],  # Mostra apenas a data, sem a hora
                        cliente_nome,
                        itens_count,
                        f"R$ {total:.2f}",
                        venda.get("forma_pagamento", ""),
                        venda.get("status", "")
                    ),
                    tags=(tag,)
                )
            
            # Configura as cores dos status
            self.vendas_tree.tag_configure("concluída", background="#d5f5e3")
            self.vendas_tree.tag_configure("cancelada", background="#fadbd8")
            self.vendas_tree.tag_configure("pendente", background="#fef9e7")
            
            # Atualiza o resumo
            self.resumo_label.configure(text=f"Total: R$ {total_geral:.2f} | Quantidade: {len(vendas)}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar vendas: {str(e)}")
    
    def filtrar_vendas(self):
        """Filtra as vendas conforme os critérios selecionados."""
        self.carregar_vendas()
    
    def visualizar_venda(self):
        """Visualiza os detalhes da venda selecionada."""
        selection = self.vendas_tree.selection()
        if not selection:
            messagebox.showinfo("Aviso", "Selecione uma venda para visualizar.")
            return
        
        # Obtém o ID da venda selecionada
        venda_id = self.vendas_tree.item(selection[0], "values")[0]
        
        # Cria uma janela de detalhes
        detalhes_window = ctk.CTkToplevel(self.parent)
        detalhes_window.title(f"Detalhes da Venda #{venda_id}")
        detalhes_window.geometry("800x600")
        detalhes_window.grab_set()  # Torna a janela modal
        
        # Obtém os detalhes da venda
        if self.controller:
            venda = self.controller.obter_venda(venda_id)
        else:
            # Dados de exemplo para testes
            vendas = self.obter_vendas_exemplo()
            venda = next((v for v in vendas if str(v["id"]) == str(venda_id)), None)
        
        if not venda:
            messagebox.showerror("Erro", "Não foi possível obter os detalhes da venda.")
            detalhes_window.destroy()
            return
        
        # Frame de informações gerais
        info_frame = ctk.CTkFrame(detalhes_window)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        # Título
        titulo_label = ctk.CTkLabel(
            info_frame, 
            text=f"Venda #{venda_id}", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo_label.pack(pady=10)
        
        # Informações da venda
        info_grid = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_grid.pack(fill="x", padx=10, pady=10)
        
        # Data
        data_label = ctk.CTkLabel(info_grid, text="Data:", font=ctk.CTkFont(weight="bold"))
        data_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        data_valor = ctk.CTkLabel(info_grid, text=venda.get("data", ""))
        data_valor.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        # Cliente
        cliente_label = ctk.CTkLabel(info_grid, text="Cliente:", font=ctk.CTkFont(weight="bold"))
        cliente_label.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        
        cliente_valor = ctk.CTkLabel(info_grid, text=venda.get("cliente_nome", "Consumidor Final"))
        cliente_valor.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        # Status
        status_label = ctk.CTkLabel(info_grid, text="Status:", font=ctk.CTkFont(weight="bold"))
        status_label.grid(row=0, column=2, sticky="w", padx=5, pady=2)
        
        status_valor = ctk.CTkLabel(info_grid, text=venda.get("status", ""))
        status_valor.grid(row=0, column=3, sticky="w", padx=5, pady=2)
        
        # Forma de pagamento
        pagamento_label = ctk.CTkLabel(info_grid, text="Pagamento:", font=ctk.CTkFont(weight="bold"))
        pagamento_label.grid(row=1, column=2, sticky="w", padx=5, pady=2)
        
        pagamento_valor = ctk.CTkLabel(info_grid, text=venda.get("forma_pagamento", ""))
        pagamento_valor.grid(row=1, column=3, sticky="w", padx=5, pady=2)
        
        # Total
        total_label = ctk.CTkLabel(info_grid, text="Total:", font=ctk.CTkFont(weight="bold"))
        total_label.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        
        total_valor = ctk.CTkLabel(info_grid, text=f"R$ {venda.get('total', 0):.2f}")
        total_valor.grid(row=2, column=1, sticky="w", padx=5, pady=2)
        
        # Tabela de itens
        itens_frame = ctk.CTkFrame(detalhes_window)
        itens_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título da tabela
        itens_titulo = ctk.CTkLabel(
            itens_frame, 
            text="Itens da Venda", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        itens_titulo.pack(pady=5)
        
        # Tabela de itens
        itens_tree = ttk.Treeview(
            itens_frame,
            columns=("codigo", "produto", "quantidade", "preco", "subtotal"),
            show="headings"
        )
        
        itens_tree.heading("codigo", text="Código")
        itens_tree.heading("produto", text="Produto")
        itens_tree.heading("quantidade", text="Qtd")
        itens_tree.heading("preco", text="Preço Unit.")
        itens_tree.heading("subtotal", text="Subtotal")
        
        itens_tree.column("codigo", width=80)
        itens_tree.column("produto", width=250)
        itens_tree.column("quantidade", width=80)
        itens_tree.column("preco", width=100)
        itens_tree.column("subtotal", width=100)
        
        # Adiciona barra de rolagem
        itens_scrollbar = ctk.CTkScrollbar(itens_frame, command=itens_tree.yview)
        itens_scrollbar.pack(side="right", fill="y")
        itens_tree.configure(yscrollcommand=itens_scrollbar.set)
        
        itens_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Preenche a tabela de itens
        itens = venda.get("itens", [])
        for item in itens:
            itens_tree.insert(
                "", "end", 
                values=(
                    item.get("codigo", ""),
                    item.get("nome", ""),
                    item.get("quantidade", 0),
                    f"R$ {item.get('preco', 0):.2f}",
                    f"R$ {item.get('total', 0):.2f}"
                )
            )
        
        # Botões de ação
        botoes_frame = ctk.CTkFrame(detalhes_window)
        botoes_frame.pack(fill="x", padx=10, pady=10)
        
        fechar_btn = ctk.CTkButton(
            botoes_frame, 
            text="Fechar", 
            command=detalhes_window.destroy,
            fg_color="#95a5a6",
            hover_color="#7f8c8d"
        )
        fechar_btn.pack(side="right", padx=5)
        
        imprimir_btn = ctk.CTkButton(
            botoes_frame, 
            text="Imprimir Comprovante", 
            command=lambda: self.imprimir_comprovante(venda_id),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        imprimir_btn.pack(side="right", padx=5)
    
    def imprimir_comprovante(self, venda_id=None):
        """Imprime o comprovante da venda."""
        # Se não foi passado um ID, pega o da seleção atual
        if not venda_id:
            selection = self.vendas_tree.selection()
            if not selection:
                messagebox.showinfo("Aviso", "Selecione uma venda para imprimir o comprovante.")
                return
            venda_id = self.vendas_tree.item(selection[0], "values")[0]
        
        # Obtém os detalhes da venda
        if self.controller:
            venda = self.controller.obter_venda(venda_id)
        else:
            # Dados de exemplo para testes
            vendas = self.obter_vendas_exemplo()
            venda = next((v for v in vendas if str(v["id"]) == str(venda_id)), None)
        
        if not venda:
            messagebox.showerror("Erro", "Não foi possível obter os detalhes da venda.")
            return
        
        # Em um sistema real, aqui seria feita a impressão do comprovante
        messagebox.showinfo("Impressão", f"Imprimindo comprovante da venda #{venda_id}... (SIMULAÇÃO)")
    
    def cancelar_venda(self):
        """Cancela a venda selecionada."""
        selection = self.vendas_tree.selection()
        if not selection:
            messagebox.showinfo("Aviso", "Selecione uma venda para cancelar.")
            return
        
        # Obtém o ID da venda selecionada
        venda_id = self.vendas_tree.item(selection[0], "values")[0]
        
        # Obtém os detalhes da venda
        if self.controller:
            venda = self.controller.obter_venda(venda_id)
        else:
            # Dados de exemplo para testes
            vendas = self.obter_vendas_exemplo()
            venda = next((v for v in vendas if str(v["id"]) == str(venda_id)), None)
        
        if not venda:
            messagebox.showerror("Erro", "Não foi possível obter os detalhes da venda.")
            return
        
        # Verifica se a venda já está cancelada
        if venda.get("status", "").lower() == "cancelada":
            messagebox.showinfo("Aviso", "Esta venda já está cancelada.")
            return
        
        # Confirma o cancelamento
        if not messagebox.askyesno("Confirmação", "Tem certeza que deseja cancelar esta venda?"):
            return
        
        # Solicita o motivo do cancelamento
        motivo = ctk.CTkInputDialog(
            text="Informe o motivo do cancelamento:",
            title="Cancelamento de Venda"
        ).get_input()
        
        if not motivo:
            messagebox.showinfo("Aviso", "É necessário informar o motivo do cancelamento.")
            return
        
        # Cancela a venda
        if self.controller:
            resultado = self.controller.cancelar_venda(venda_id, motivo)
            if resultado.get("sucesso", False):
                messagebox.showinfo("Sucesso", "Venda cancelada com sucesso!")
                self.carregar_vendas()
            else:
                messagebox.showerror("Erro", resultado.get("mensagem", "Erro ao cancelar venda."))
        else:
            # Simulação para testes
            messagebox.showinfo("Sucesso", "Venda cancelada com sucesso! (SIMULAÇÃO)")
            self.carregar_vendas()
    
    def exportar_csv(self):
        """Exporta as vendas filtradas para um arquivo CSV."""
        # Solicita o local para salvar o arquivo
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv"), ("Todos os arquivos", "*.*")],
            title="Exportar vendas para CSV"
        )
        
        if not arquivo:
            return
        
        try:
            # Obtém as vendas filtradas
            if self.controller:
                # Prepara os filtros
                data_inicial = datetime.datetime.strptime(self.data_inicial_var.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
                data_final = datetime.datetime.strptime(self.data_final_var.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
                data_final += " 23:59:59"  # Inclui o último dia inteiro
                
                filtros = {
                    "data_inicial": data_inicial,
                    "data_final": data_final
                }
                
                # Adiciona filtro de status se necessário
                if self.status_var.get() != "Todos":
                    filtros["status"] = self.status_var.get()
                
                # Adiciona filtro de cliente se necessário
                if self.cliente_var.get():
                    filtros["cliente"] = self.cliente_var.get()
                
                vendas = self.controller.listar_vendas(filtros)
            else:
                # Dados de exemplo para testes
                vendas = self.obter_vendas_exemplo()
            
            # Escreve o arquivo CSV
            with open(arquivo, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Escreve o cabeçalho
                writer.writerow(['ID', 'Data', 'Cliente', 'Itens', 'Total', 'Pagamento', 'Status'])
                
                # Escreve os dados
                for venda in vendas:
                    writer.writerow([
                        venda.get("id", ""),
                        venda.get("data", ""),
                        venda.get("cliente_nome", "Consumidor Final"),
                        venda.get("itens_count", 0),
                        venda.get("total", 0),
                        venda.get("forma_pagamento", ""),
                        venda.get("status", "")
                    ])
            
            messagebox.showinfo("Sucesso", f"Vendas exportadas com sucesso para {arquivo}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar vendas: {str(e)}")
    
    def obter_vendas_exemplo(self):
        """Retorna dados de exemplo para as vendas."""
        data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_anterior = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        data_antiga = (datetime.datetime.now() - datetime.timedelta(days=15)).strftime("%Y-%m-%d %H:%M:%S")
        
        return [
            {
                "id": "1",
                "data": data_atual,
                "cliente_nome": "Consumidor Final",
                "cliente_id": None,
                "itens_count": 2,
                "total": 100.00,
                "forma_pagamento": "Dinheiro",
                "status": "Concluída",
                "itens": [
                    {
                        "codigo": "P001",
                        "nome": "Produto 1",
                        "quantidade": 2,
                        "preco": 25.00,
                        "total": 50.00
                    },
                    {
                        "codigo": "P002",
                        "nome": "Produto 2",
                        "quantidade": 1,
                        "preco": 50.00,
                        "total": 50.00
                    }
                ]
            },
            {
                "id": "2",
                "data": data_anterior,
                "cliente_nome": "João Silva",
                "cliente_id": "1",
                "itens_count": 3,
                "total": 75.50,
                "forma_pagamento": "Cartão de Crédito",
                "status": "Concluída",
                "itens": [
                    {
                        "codigo": "P003",
                        "nome": "Produto 3",
                        "quantidade": 1,
                        "preco": 45.00,
                        "total": 45.00
                    },
                    {
                        "codigo": "P004",
                        "nome": "Produto 4",
                        "quantidade": 3,
                        "preco": 10.00,
                        "total": 30.00
                    },
                    {
                        "codigo": "P005",
                        "nome": "Produto 5",
                        "quantidade": 1,
                        "preco": 0.50,
                        "total": 0.50
                    }
                ]
            },
            {
                "id": "3",
                "data": data_antiga,
                "cliente_nome": "Maria Oliveira",
                "cliente_id": "2",
                "itens_count": 1,
                "total": 150.00,
                "forma_pagamento": "PIX",
                "status": "Cancelada",
                "itens": [
                    {
                        "codigo": "P006",
                        "nome": "Produto 6",
                        "quantidade": 1,
                        "preco": 150.00,
                        "total": 150.00
                    }
                ]
            }
        ]