import customtkinter as ctk
from tkinter import ttk, messagebox
import datetime

class FiscalView:
    def __init__(self, parent, controller=None):
        self.parent = parent
        self.controller = controller
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título com estilo
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="#9b59b6", corner_radius=10)
        title_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="MÓDULO FISCAL", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=10)
        
        # Tabs
        self.tab_view = ctk.CTkTabview(self.main_frame)
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab NFC-e
        self.tab_nfce = self.tab_view.add("NFC-e")
        self.setup_tab_nfce()
        
        # Tab Configurações Fiscais
        self.tab_config = self.tab_view.add("Configurações")
        self.setup_tab_config()
    
    def setup_tab_nfce(self):
        """Configura a tab de NFC-e."""
        # Frame de filtros
        filtros_frame = ctk.CTkFrame(self.tab_nfce)
        filtros_frame.pack(fill="x", padx=10, pady=10)
        
        # Período
        periodo_label = ctk.CTkLabel(filtros_frame, text="Período:")
        periodo_label.pack(side="left", padx=5)
        
        self.data_inicio_var = ctk.StringVar(value=datetime.datetime.now().strftime("%d/%m/%Y"))
        data_inicio_entry = ctk.CTkEntry(
            filtros_frame, 
            textvariable=self.data_inicio_var,
            width=100
        )
        data_inicio_entry.pack(side="left", padx=5)
        
        ate_label = ctk.CTkLabel(filtros_frame, text="até")
        ate_label.pack(side="left", padx=5)
        
        self.data_fim_var = ctk.StringVar(value=datetime.datetime.now().strftime("%d/%m/%Y"))
        data_fim_entry = ctk.CTkEntry(
            filtros_frame, 
            textvariable=self.data_fim_var,
            width=100
        )
        data_fim_entry.pack(side="left", padx=5)
        
        # Status
        status_label = ctk.CTkLabel(filtros_frame, text="Status:")
        status_label.pack(side="left", padx=5)
        
        self.status_var = ctk.StringVar(value="Todos")
        status_options = ["Todos", "Autorizada", "Cancelada", "Rejeitada"]
        
        status_combobox = ctk.CTkComboBox(
            filtros_frame, 
            values=status_options,
            variable=self.status_var,
            width=150
        )
        status_combobox.pack(side="left", padx=5)
        
        # Botão de filtrar
        filtrar_btn = ctk.CTkButton(
            filtros_frame, 
            text="Filtrar", 
            command=self.filtrar_nfce,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        filtrar_btn.pack(side="right", padx=5)
        
        # Tabela de NFC-e
        self.nfce_tree = ttk.Treeview(
            self.tab_nfce,
            columns=("numero", "data", "cliente", "total", "status"),
            show="headings"
        )
        
        self.nfce_tree.heading("numero", text="Número")
        self.nfce_tree.heading("data", text="Data Emissão")
        self.nfce_tree.heading("cliente", text="Cliente")
        self.nfce_tree.heading("total", text="Total")
        self.nfce_tree.heading("status", text="Status")
        
        self.nfce_tree.column("numero", width=150)
        self.nfce_tree.column("data", width=150)
        self.nfce_tree.column("cliente", width=200)
        self.nfce_tree.column("total", width=100)
        self.nfce_tree.column("status", width=100)
        
        # Adiciona barra de rolagem
        nfce_scrollbar = ctk.CTkScrollbar(self.tab_nfce, command=self.nfce_tree.yview)
        nfce_scrollbar.pack(side="right", fill="y")
        self.nfce_tree.configure(yscrollcommand=nfce_scrollbar.set)
        
        self.nfce_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botões de ação
        actions_frame = ctk.CTkFrame(self.tab_nfce)
        actions_frame.pack(fill="x", padx=10, pady=10)
        
        visualizar_btn = ctk.CTkButton(
            actions_frame, 
            text="Visualizar", 
            command=self.visualizar_nfce,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        visualizar_btn.pack(side="left", padx=5)
        
        cancelar_btn = ctk.CTkButton(
            actions_frame, 
            text="Cancelar NFC-e", 
            # Remove the duplicate command parameter
            command=self.cancelar_nfce,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        cancelar_btn.pack(side="left", padx=5)
        
        imprimir_btn = ctk.CTkButton(
            actions_frame, 
            text="Imprimir DANFE", 
            command=self.imprimir_danfe,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        imprimir_btn.pack(side="left", padx=5)
        
        # Carrega os dados iniciais
        self.carregar_nfce()
    
    def setup_tab_config(self):
        """Configura a tab de configurações fiscais."""
        # Frame de configurações
        config_frame = ctk.CTkFrame(self.tab_config)
        config_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        config_label = ctk.CTkLabel(
            config_frame, 
            text="Configurações Fiscais", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        config_label.pack(pady=10)
        
        # Certificado Digital
        cert_frame = ctk.CTkFrame(config_frame)
        cert_frame.pack(fill="x", padx=10, pady=10)
        
        cert_label = ctk.CTkLabel(
            cert_frame, 
            text="Certificado Digital", 
            font=ctk.CTkFont(weight="bold")
        )
        cert_label.pack(pady=5)
        
        # Caminho do certificado
        cert_path_frame = ctk.CTkFrame(cert_frame)
        cert_path_frame.pack(fill="x", pady=5)
        
        cert_path_label = ctk.CTkLabel(cert_path_frame, text="Caminho:")
        cert_path_label.pack(side="left", padx=5)
        
        self.cert_path_var = ctk.StringVar()
        cert_path_entry = ctk.CTkEntry(
            cert_path_frame, 
            textvariable=self.cert_path_var,
            width=300
        )
        cert_path_entry.pack(side="left", padx=5)
        
        cert_path_btn = ctk.CTkButton(
            cert_path_frame, 
            text="Selecionar", 
            command=self.selecionar_certificado,
            fg_color="#3498db",
            hover_color="#2980b9",
            width=100
        )
        cert_path_btn.pack(side="left", padx=5)
        
        # Senha do certificado
        cert_senha_frame = ctk.CTkFrame(cert_frame)
        cert_senha_frame.pack(fill="x", pady=5)
        
        cert_senha_label = ctk.CTkLabel(cert_senha_frame, text="Senha:")
        cert_senha_label.pack(side="left", padx=5)
        
        self.cert_senha_var = ctk.StringVar()
        cert_senha_entry = ctk.CTkEntry(
            cert_senha_frame, 
            textvariable=self.cert_senha_var,
            width=200,
            show="*"
        )
        cert_senha_entry.pack(side="left", padx=5)
        
        # Ambiente
        ambiente_frame = ctk.CTkFrame(config_frame)
        ambiente_frame.pack(fill="x", padx=10, pady=10)
        
        ambiente_label = ctk.CTkLabel(
            ambiente_frame, 
            text="Ambiente", 
            font=ctk.CTkFont(weight="bold")
        )
        ambiente_label.pack(pady=5)
        
        self.ambiente_var = ctk.StringVar(value="Homologação")
        
        homologacao_radio = ctk.CTkRadioButton(
            ambiente_frame, 
            text="Homologação (Testes)",
            variable=self.ambiente_var,
            value="Homologação"
        )
        homologacao_radio.pack(anchor="w", padx=20, pady=5)
        
        producao_radio = ctk.CTkRadioButton(
            ambiente_frame, 
            text="Produção",
            variable=self.ambiente_var,
            value="Produção"
        )
        producao_radio.pack(anchor="w", padx=20, pady=5)
        
        # Dados da Empresa
        empresa_frame = ctk.CTkFrame(config_frame)
        empresa_frame.pack(fill="x", padx=10, pady=10)
        
        empresa_label = ctk.CTkLabel(
            empresa_frame, 
            text="Dados da Empresa", 
            font=ctk.CTkFont(weight="bold")
        )
        empresa_label.pack(pady=5)
        
        # CNPJ
        cnpj_frame = ctk.CTkFrame(empresa_frame)
        cnpj_frame.pack(fill="x", pady=5)
        
        cnpj_label = ctk.CTkLabel(cnpj_frame, text="CNPJ:")
        cnpj_label.pack(side="left", padx=5)
        
        self.cnpj_var = ctk.StringVar()
        cnpj_entry = ctk.CTkEntry(
            cnpj_frame, 
            textvariable=self.cnpj_var,
            width=200
        )
        cnpj_entry.pack(side="left", padx=5)
        
        # Razão Social
        razao_frame = ctk.CTkFrame(empresa_frame)
        razao_frame.pack(fill="x", pady=5)
        
        razao_label = ctk.CTkLabel(razao_frame, text="Razão Social:")
        razao_label.pack(side="left", padx=5)
        
        self.razao_var = ctk.StringVar()
        razao_entry = ctk.CTkEntry(
            razao_frame, 
            textvariable=self.razao_var,
            width=300
        )
        razao_entry.pack(side="left", padx=5)
        # Botões de ação
        buttons_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=10, pady=20)
        
        salvar_btn = ctk.CTkButton(
            buttons_frame, 
            text="Salvar Configurações", 
            command=self.salvar_configuracoes,
            fg_color="#27ae60",
            hover_color="#2ecc71",
            width=200
        )
        salvar_btn.pack(side="left", padx=5)
        
        testar_btn = ctk.CTkButton(
            buttons_frame, 
            text="Testar Conexão", 
            command=self.testar_conexao,
            fg_color="#3498db",
            hover_color="#2980b9",
            width=200
        )
        testar_btn.pack(side="right", padx=5)
        
        # Add the advanced config button
        config_avancado_btn = ctk.CTkButton(
            buttons_frame, 
            text="Configurações Avançadas",
            command=self.mostrar_configuracoes,
            fg_color="#9b59b6",
            hover_color="#8e44ad",
            width=200
        )
        config_avancado_btn.pack(side="left", padx=5)
    
        # Carrega as configurações
        self.carregar_configuracoes()
    def carregar_nfce(self):
        """Carrega as NFC-e na tabela."""
        # Limpa a tabela
        for item in self.nfce_tree.get_children():
            self.nfce_tree.delete(item)
        
        # Obtém as NFC-e do controller
        if self.controller:
            nfces = self.controller.listar_nfces()
        else:
            # Dados de exemplo para testes
            nfces = self.obter_nfces_exemplo()
        
        # Filtra pelo status, se necessário
        status = self.status_var.get()
        if status != "Todos":
            nfces = [n for n in nfces if n["status"] == status]
        
        # Preenche a tabela
        for nfce in nfces:
            self.nfce_tree.insert(
                "", "end", 
                values=(
                    nfce["numero"],
                    nfce["data_emissao"],
                    nfce["cliente"],
                    f"R$ {nfce['total']:.2f}",
                    nfce["status"]
                ),
                tags=(nfce["numero"],)
            )
    
    def filtrar_nfce(self):
        """Filtra as NFC-e conforme os critérios selecionados."""
        # Implementação futura: filtrar por data
        self.carregar_nfce()
    
    def visualizar_nfce(self):
        """Visualiza os detalhes da NFC-e selecionada."""
        selection = self.nfce_tree.selection()
        if not selection:
            messagebox.showinfo("Aviso", "Selecione uma NFC-e para visualizar.")
            return
        
        # Obtém o número da NFC-e selecionada
        nfce_numero = self.nfce_tree.item(selection[0], "tags")[0]
        
        # Obtém os dados da NFC-e
        if self.controller:
            nfce = self.controller.obter_nfce(nfce_numero)
        else:
            # Dados de exemplo para testes
            nfces = self.obter_nfces_exemplo()
            nfce = next((n for n in nfces if n["numero"] == nfce_numero), None)
        
        if not nfce:
            messagebox.showerror("Erro", "NFC-e não encontrada.")
            return
            
        # Aqui implementar a visualização dos detalhes da NFC-e
        # Por exemplo, abrir uma nova janela com os detalhes
        messagebox.showinfo("Detalhes da NFC-e", f"Visualizando detalhes da NFC-e {nfce_numero}")

    def cancelar_nfce(self):
        """Cancela a NFC-e selecionada."""
        selection = self.nfce_tree.selection()
        if not selection:
            messagebox.showinfo("Aviso", "Selecione uma NFC-e para cancelar.")
            return
        
        # Obtém o número da NFC-e selecionada
        nfce_numero = self.nfce_tree.item(selection[0], "tags")[0]
        
        # Obtém os dados da NFC-e
        if self.controller:
            nfce = self.controller.obter_nfce(nfce_numero)
        else:
            # Dados de exemplo para testes
            nfces = self.obter_nfces_exemplo()
            nfce = next((n for n in nfces if n["numero"] == nfce_numero), None)
        
        if not nfce:
            messagebox.showerror("Erro", "NFC-e não encontrada.")
            return
            
        # Verifica se a NFC-e já está cancelada
        if nfce["status"] == "Cancelada":
            messagebox.showinfo("Aviso", "Esta NFC-e já está cancelada.")
            return
            
        # Confirma o cancelamento
        if not messagebox.askyesno("Confirmação", "Tem certeza que deseja cancelar esta NFC-e?"):
            return
            
        # Solicita o motivo do cancelamento
        motivo = ctk.CTkInputDialog(
            text="Informe o motivo do cancelamento:",
            title="Cancelamento de NFC-e"
        ).get_input()
            
        if not motivo:
            messagebox.showinfo("Aviso", "É necessário informar o motivo do cancelamento.")
            return
            
        # Cancela a NFC-e
        if self.controller:
            resultado = self.controller.cancelar_nfce(nfce_numero, motivo)
            if resultado.get("sucesso", False):
                messagebox.showinfo("Sucesso", "NFC-e cancelada com sucesso!")
                self.carregar_nfce()
            else:
                messagebox.showerror("Erro", resultado.get("mensagem", "Erro ao cancelar NFC-e."))
        else:
            # Simulação para testes
            messagebox.showinfo("Sucesso", "NFC-e cancelada com sucesso! (SIMULAÇÃO)")
            self.carregar_nfce()
    
    def imprimir_danfe(self):
        """Imprime o DANFE da NFC-e."""
        selection = self.nfce_tree.selection()
        if not selection:
            messagebox.showinfo("Aviso", "Selecione uma NFC-e para imprimir o DANFE.")
            return
            
        # Obtém o número da NFC-e selecionada
        nfce_numero = self.nfce_tree.item(selection[0], "tags")[0]
        
        # Em um sistema real, aqui seria feita a geração e impressão do DANFE
        messagebox.showinfo("Impressão", f"Imprimindo DANFE da NFC-e {nfce_numero}... (SIMULAÇÃO)")
    
    def selecionar_certificado(self):
        """Abre um diálogo para selecionar o arquivo do certificado digital."""
        from tkinter import filedialog
        
        arquivo = filedialog.askopenfilename(
            title="Selecionar Certificado Digital",
            filetypes=[("Certificado PFX", "*.pfx"), ("Todos os arquivos", "*.*")]
        )
        
        if arquivo:
            self.cert_path_var.set(arquivo)

    def mostrar_configuracoes(self):
        """Mostra a tela de configurações fiscais avançadas."""
        # Importa a view de configurações
        from modules.fiscal.configuracoes_view import ConfiguracoesFiscaisView
        
        # Cria uma nova janela para as configurações
        config_window = ctk.CTkToplevel(self.parent)
        config_window.title("Configurações Fiscais Avançadas")
        config_window.geometry("800x600")
        config_window.minsize(800, 600)
        config_window.grab_set()  # Torna a janela modal
        
        # Cria a view de configurações
        ConfiguracoesFiscaisView(config_window, self.controller)
    
    def salvar_configuracoes(self):
        """Salva as configurações fiscais."""
        if not self.controller:
            messagebox.showinfo("Simulação", "Configurações salvas com sucesso! (SIMULAÇÃO)")
            return
            
        # Coleta os dados dos campos
        config = {
            'cnpj': self.cnpj_var.get(),
            'razao_social': self.razao_var.get(),
            'certificado_caminho': self.cert_path_var.get(),
            'certificado_senha': self.cert_senha_var.get(),
            'ambiente_nfe': self.ambiente_var.get()
        }
        
        # Validações básicas
        if not config['cnpj']:
            messagebox.showwarning("Aviso", "Informe o CNPJ da empresa.")
            return
            
        if not config['razao_social']:
            messagebox.showwarning("Aviso", "Informe a Razão Social da empresa.")
            return
        
        # Salva as configurações
        resultado = self.controller.salvar_configuracoes(config)
        
        if resultado.get('sucesso', False):
            messagebox.showinfo("Sucesso", resultado.get('mensagem', "Configurações salvas com sucesso!"))
        else:
            messagebox.showerror("Erro", resultado.get('mensagem', "Erro ao salvar configurações."))
    
    def testar_conexao(self):
        """Testa a conexão com o serviço da SEFAZ."""
        if not self.cert_path_var.get():
            messagebox.showwarning("Aviso", "Selecione um certificado digital.")
            return
            
        if not self.cert_senha_var.get():
            messagebox.showwarning("Aviso", "Informe a senha do certificado.")
            return
            
        # Em um sistema real, aqui seria feita a conexão com o serviço da SEFAZ
        # Para fins de demonstração, vamos apenas simular o teste
        
        messagebox.showinfo(
            "Teste de Conexão", 
            "Conexão com o serviço da SEFAZ realizada com sucesso! (SIMULAÇÃO)\n\n"
            "Em um sistema real, seria feita a conexão com o serviço da SEFAZ."
        )
    
    def carregar_configuracoes(self):
        """Carrega as configurações fiscais do banco de dados."""
        if not self.controller:
            # Dados de exemplo para testes
            self.cnpj_var.set("00.000.000/0000-00")
            self.razao_var.set("Empresa de Exemplo LTDA")
            self.cert_path_var.set("C:/caminho/para/certificado.pfx")
            self.cert_senha_var.set("senha123")
            self.ambiente_var.set("Homologação")
            return
            
        # Obtém as configurações do controller
        config = self.controller.obter_configuracoes()
        
        # Preenche os campos com os valores obtidos
        self.cnpj_var.set(config.get('cnpj', ''))
        self.razao_var.set(config.get('razao_social', ''))
        self.cert_path_var.set(config.get('certificado_caminho', ''))
        self.cert_senha_var.set(config.get('certificado_senha', ''))
        self.ambiente_var.set(config.get('ambiente_nfe', 'Homologação'))
    
    def obter_nfces_exemplo(self):
        """Retorna dados de exemplo para testes."""
        return [
            {
                "numero": "000000001",
                "chave_acesso": "35220500000000000100650010000000011000000015",
                "data_emissao": "01/05/2023 14:30:45",
                "cliente": "Consumidor Final",
                "total": 156.78,
                "status": "Autorizada"
            },
            {
                "numero": "000000002",
                "chave_acesso": "35220500000000000100650010000000021000000025",
                "data_emissao": "02/05/2023 10:15:22",
                "cliente": "João Silva",
                "total": 89.90,
                "status": "Autorizada"
            },
            {
                "numero": "000000003",
                "chave_acesso": "35220500000000000100650010000000031000000035",
                "data_emissao": "03/05/2023 16:45:10",
                "cliente": "Maria Oliveira",
                "total": 245.30,
                "status": "Cancelada"
            }
        ]