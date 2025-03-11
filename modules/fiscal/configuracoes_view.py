import customtkinter as ctk
from tkinter import messagebox, filedialog
import os

class ConfiguracoesFiscaisView:
    def __init__(self, parent, controller=None):
        self.parent = parent
        self.controller = controller
        
        # Variáveis para armazenar os valores dos campos
        self.razao_var = ctk.StringVar()
        self.fantasia_var = ctk.StringVar()
        self.cnpj_var = ctk.StringVar()
        self.ie_var = ctk.StringVar()
        self.im_var = ctk.StringVar()
        self.endereco_var = ctk.StringVar()
        self.cidade_var = ctk.StringVar()
        self.estado_var = ctk.StringVar()
        self.cep_var = ctk.StringVar()
        self.telefone_var = ctk.StringVar()
        self.email_var = ctk.StringVar()
        self.regime_var = ctk.StringVar(value="Simples Nacional")
        self.ambiente_var = ctk.StringVar(value="Homologação")
        self.certificado_var = ctk.StringVar()
        self.senha_var = ctk.StringVar()
        self.serie_var = ctk.StringVar(value="1")
        self.numeracao_var = ctk.StringVar(value="1")
        
        self.setup_ui()
        self.carregar_configuracoes()
    
    def setup_ui(self):
        """Configura a interface de usuário."""
        # Frame principal com scroll
        main_frame = ctk.CTkFrame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Configurações Fiscais", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Frame com scroll para os campos
        scroll_frame = ctk.CTkScrollableFrame(main_frame)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Dados da Empresa
        empresa_frame = ctk.CTkFrame(scroll_frame)
        empresa_frame.pack(fill="x", padx=10, pady=10)
        
        empresa_label = ctk.CTkLabel(
            empresa_frame, 
            text="Dados da Empresa", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        empresa_label.pack(pady=5)
        
        # Razão Social
        self._criar_campo(empresa_frame, "Razão Social:", self.razao_var, width=400)
        
        # Nome Fantasia
        self._criar_campo(empresa_frame, "Nome Fantasia:", self.fantasia_var, width=400)
        
        # CNPJ
        self._criar_campo(empresa_frame, "CNPJ:", self.cnpj_var, width=200)
        
        # Inscrição Estadual
        self._criar_campo(empresa_frame, "Inscrição Estadual:", self.ie_var, width=200)
        
        # Inscrição Municipal
        self._criar_campo(empresa_frame, "Inscrição Municipal:", self.im_var, width=200)
        
        # Endereço
        self._criar_campo(empresa_frame, "Endereço:", self.endereco_var, width=400)
        
        # Cidade
        self._criar_campo(empresa_frame, "Cidade:", self.cidade_var, width=200)
        
        # Estado
        self._criar_campo(empresa_frame, "Estado:", self.estado_var, width=100)
        
        # CEP
        self._criar_campo(empresa_frame, "CEP:", self.cep_var, width=150)
        
        # Telefone
        self._criar_campo(empresa_frame, "Telefone:", self.telefone_var, width=200)
        
        # Email
        self._criar_campo(empresa_frame, "Email:", self.email_var, width=300)
        
        # Regime Tributário
        regime_frame = ctk.CTkFrame(empresa_frame)
        regime_frame.pack(fill="x", pady=5)
        
        regime_label = ctk.CTkLabel(regime_frame, text="Regime Tributário:")
        regime_label.pack(side="left", padx=5)
        
        regimes = ["Simples Nacional", "Lucro Presumido", "Lucro Real"]
        regime_combo = ctk.CTkComboBox(
            regime_frame, 
            values=regimes,
            variable=self.regime_var,
            width=200
        )
        regime_combo.pack(side="left", padx=5)
        
        # Certificado Digital
        cert_frame = ctk.CTkFrame(scroll_frame)
        cert_frame.pack(fill="x", padx=10, pady=10)
        
        cert_label = ctk.CTkLabel(
            cert_frame, 
            text="Certificado Digital", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        cert_label.pack(pady=5)
        
        # Caminho do Certificado
        cert_path_frame = ctk.CTkFrame(cert_frame)
        cert_path_frame.pack(fill="x", pady=5)
        
        cert_path_label = ctk.CTkLabel(cert_path_frame, text="Arquivo:")
        cert_path_label.pack(side="left", padx=5)
        
        cert_path_entry = ctk.CTkEntry(
            cert_path_frame, 
            textvariable=self.certificado_var,
            width=300
        )
        cert_path_entry.pack(side="left", padx=5)
        
        cert_path_btn = ctk.CTkButton(
            cert_path_frame, 
            text="Selecionar",
            command=self.selecionar_certificado,
            width=100
        )
        cert_path_btn.pack(side="left", padx=5)
        
        # Senha do Certificado
        cert_senha_frame = ctk.CTkFrame(cert_frame)
        cert_senha_frame.pack(fill="x", pady=5)
        
        cert_senha_label = ctk.CTkLabel(cert_senha_frame, text="Senha:")
        cert_senha_label.pack(side="left", padx=5)
        
        cert_senha_entry = ctk.CTkEntry(
            cert_senha_frame, 
            textvariable=self.senha_var,
            width=200,
            show="*"
        )
        cert_senha_entry.pack(side="left", padx=5)
        
        # Ambiente
        ambiente_frame = ctk.CTkFrame(scroll_frame)
        ambiente_frame.pack(fill="x", padx=10, pady=10)
        
        ambiente_label = ctk.CTkLabel(
            ambiente_frame, 
            text="Ambiente de Emissão", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        ambiente_label.pack(pady=5)
        
        # Opções de Ambiente
        ambiente_options_frame = ctk.CTkFrame(ambiente_frame)
        ambiente_options_frame.pack(fill="x", pady=5)
        
        homologacao_radio = ctk.CTkRadioButton(
            ambiente_options_frame, 
            text="Homologação (Testes)",
            variable=self.ambiente_var,
            value="Homologação"
        )
        homologacao_radio.pack(anchor="w", padx=20, pady=5)
        
        producao_radio = ctk.CTkRadioButton(
            ambiente_options_frame, 
            text="Produção",
            variable=self.ambiente_var,
            value="Produção"
        )
        producao_radio.pack(anchor="w", padx=20, pady=5)
        
        # Numeração
        numeracao_frame = ctk.CTkFrame(scroll_frame)
        numeracao_frame.pack(fill="x", padx=10, pady=10)
        
        numeracao_label = ctk.CTkLabel(
            numeracao_frame, 
            text="Numeração de Documentos", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        numeracao_label.pack(pady=5)
        
        # Série
        serie_frame = ctk.CTkFrame(numeracao_frame)
        serie_frame.pack(fill="x", pady=5)
        
        serie_label = ctk.CTkLabel(serie_frame, text="Série NF-e:")
        serie_label.pack(side="left", padx=5)
        
        serie_entry = ctk.CTkEntry(
            serie_frame, 
            textvariable=self.serie_var,
            width=100
        )
        serie_entry.pack(side="left", padx=5)
        
        # Próxima Numeração
        numeracao_next_frame = ctk.CTkFrame(numeracao_frame)
        numeracao_next_frame.pack(fill="x", pady=5)
        
        numeracao_next_label = ctk.CTkLabel(numeracao_next_frame, text="Próxima Numeração:")
        numeracao_next_label.pack(side="left", padx=5)
        
        numeracao_next_entry = ctk.CTkEntry(
            numeracao_next_frame, 
            textvariable=self.numeracao_var,
            width=100
        )
        numeracao_next_entry.pack(side="left", padx=5)
        
        # Botões de ação
        botoes_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        botoes_frame.pack(fill="x", padx=10, pady=20)
        
        salvar_btn = ctk.CTkButton(
            botoes_frame, 
            text="Salvar Configurações",
            command=self.salvar_configuracoes,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=200
        )
        salvar_btn.pack(side="right", padx=10)
        
        testar_btn = ctk.CTkButton(
            botoes_frame, 
            text="Testar Certificado",
            command=self.testar_certificado,
            fg_color="#3498db",
            hover_color="#2980b9",
            width=150
        )
        testar_btn.pack(side="right", padx=10)
    
    def _criar_campo(self, parent, label_text, variable, width=200):
        """Cria um campo de entrada com label."""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=5)
        
        label = ctk.CTkLabel(frame, text=label_text)
        label.pack(side="left", padx=5)
        
        entry = ctk.CTkEntry(
            frame, 
            textvariable=variable,
            width=width
        )
        entry.pack(side="left", padx=5)
        
        return entry
    
    def carregar_configuracoes(self):
        """Carrega as configurações fiscais do banco de dados."""
        if self.controller:
            config = self.controller.obter_configuracoes()
            
            # Preenche os campos com os valores obtidos
            self.razao_var.set(config.get('razao_social', ''))
            self.fantasia_var.set(config.get('nome_fantasia', ''))
            self.cnpj_var.set(config.get('cnpj', ''))
            self.ie_var.set(config.get('inscricao_estadual', ''))
            self.im_var.set(config.get('inscricao_municipal', ''))
            self.endereco_var.set(config.get('endereco', ''))
            self.cidade_var.set(config.get('cidade', ''))
            self.estado_var.set(config.get('estado', ''))
            self.cep_var.set(config.get('cep', ''))
            self.telefone_var.set(config.get('telefone', ''))
            self.email_var.set(config.get('email', ''))
            self.regime_var.set(config.get('regime_tributario', 'Simples Nacional'))
            self.ambiente_var.set(config.get('ambiente_nfe', 'Homologação'))
            self.certificado_var.set(config.get('certificado_caminho', ''))
            self.senha_var.set(config.get('certificado_senha', ''))
            self.serie_var.set(str(config.get('serie_nfe', 1)))
            self.numeracao_var.set(str(config.get('proxima_numeracao', 1)))
    
    def selecionar_certificado(self):
        """Abre o diálogo para selecionar o arquivo de certificado digital."""
        arquivo = filedialog.askopenfilename(
            title="Selecionar Certificado Digital",
            filetypes=[
                ("Certificados", "*.pfx;*.p12"), 
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if arquivo:
            self.certificado_var.set(arquivo)
    
    def testar_certificado(self):
        """Testa se o certificado digital é válido."""
        caminho = self.certificado_var.get()
        senha = self.senha_var.get()
        
        if not caminho:
            messagebox.showwarning("Aviso", "Selecione um certificado digital.")
            return
        
        if not senha:
            messagebox.showwarning("Aviso", "Informe a senha do certificado.")
            return
        
        if not os.path.exists(caminho):
            messagebox.showerror("Erro", "Arquivo de certificado não encontrado.")
            return
        
        # Em um sistema real, aqui seria feita a validação do certificado
        # Para fins de demonstração, vamos apenas simular o teste
        
        messagebox.showinfo(
            "Teste de Certificado", 
            "Certificado validado com sucesso! (SIMULAÇÃO)\n\n"
            "Em um sistema real, seria feita a validação do certificado junto à SEFAZ."
        )
    
    def salvar_configuracoes(self):
        """Salva as configurações fiscais no banco de dados."""
        # Coleta os dados dos campos
        config = {
            'razao_social': self.razao_var.get(),
            'nome_fantasia': self.fantasia_var.get(),
            'cnpj': self.cnpj_var.get(),
            'inscricao_estadual': self.ie_var.get(),
            'inscricao_municipal': self.im_var.get(),
            'endereco': self.endereco_var.get(),
            'cidade': self.cidade_var.get(),
            'estado': self.estado_var.get(),
            'cep': self.cep_var.get(),
            'telefone': self.telefone_var.get(),
            'email': self.email_var.get(),
            'regime_tributario': self.regime_var.get(),
            'ambiente_nfe': self.ambiente_var.get(),
            'certificado_caminho': self.certificado_var.get(),
            'certificado_senha': self.senha_var.get(),
            'serie_nfe': int(self.serie_var.get() or 1),
            'proxima_numeracao': int(self.numeracao_var.get() or 1)
        }
        
        # Validações básicas
        if not config['razao_social']:
            messagebox.showwarning("Aviso", "Informe a Razão Social da empresa.")
            return
            
        if not config['cnpj']:
            messagebox.showwarning("Aviso", "Informe o CNPJ da empresa.")
            return
            
        # Validação do CNPJ
        if not self.validar_cnpj(config['cnpj']):
            messagebox.showerror("Erro", "CNPJ inválido. Verifique o número informado.")
            return
        
        # Salva as configurações
        if self.controller:
            resultado = self.controller.salvar_configuracoes(config)
            
            if resultado.get('sucesso', False):
                messagebox.showinfo("Sucesso", resultado.get('mensagem', "Configurações salvas com sucesso!"))
            else:
                messagebox.showerror("Erro", resultado.get('mensagem', "Erro ao salvar configurações."))
        else:
            # Simulação para testes
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso! (SIMULAÇÃO)")
    
    def validar_cnpj(self, cnpj):
        """Valida um CNPJ."""
        # Remove caracteres não numéricos
        cnpj = ''.join(filter(str.isdigit, cnpj))
        
        # Verifica se tem 14 dígitos
        if len(cnpj) != 14:
            return False
        
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