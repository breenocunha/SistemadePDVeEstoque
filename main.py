import customtkinter as ctk
from tkinter import messagebox
import os
import sys

# Adiciona o diretório atual ao PATH para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importa os módulos
from modules.database.db_controller import DatabaseController
from modules.clientes.clientes_controller import ClientesController
from modules.produtos.produtos_view import ProdutosView
from modules.produtos.produtos_controller import ProdutosController
from modules.vendas.vendas_view import VendasView
from modules.vendas.vendas_controller import VendasController
from modules.fiscal.fiscal_view import FiscalView
from modules.fiscal.fiscal_controller import FiscalController
from modules.relatorios.relatorios_view import RelatoriosView
from modules.vendas.historico_vendas_view import HistoricoVendasView
from modules.vendas.historico_vendas_controller import HistoricoVendasController

class App:
    def __init__(self):
        self.setup_app()
        self.setup_controllers()
        self.setup_ui()
    
    def setup_app(self):
        """Configura a aplicação."""
        ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        
        self.app = ctk.CTk()
        self.app.title("PDV B1 Sistemas")  # Alterado para o novo nome
        self.app.geometry("1200x700")
        self.app.minsize(800, 600)
    
    def setup_controllers(self):
        """Configura os controladores da aplicação."""
        # Define o caminho do banco de dados
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "database.db")
        
        # Inicializa o controlador do banco de dados
        self.db_controller = DatabaseController(db_path)
        
        # Add cliente_id column to vendas table if needed
        self.db_controller.add_cliente_id_to_vendas()
        
        # Inicializa os demais controladores
        self.clientes_controller = ClientesController(self.db_controller)
        self.produtos_controller = ProdutosController(self.db_controller)
        self.vendas_controller = VendasController(self.db_controller, self.produtos_controller)
        self.fiscal_controller = FiscalController(self.db_controller)
    
    def setup_ui(self):
        """Configura a interface do usuário."""
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.app)
        self.main_frame.pack(fill="both", expand=True)
        
        # Cria o menu lateral
        self.sidebar_frame = ctk.CTkFrame(self.main_frame, width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y", padx=0, pady=0)
        
        # Logo
        logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="PDV B1 Sistemas",  # Alterado para o novo nome
            font=ctk.CTkFont(size=20, weight="bold")
        )
        logo_label.pack(pady=20)
        
        # Botões do menu
        self.pdv_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="Ponto de Venda",
            command=self.mostrar_pdv,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            height=40
        )
        self.pdv_btn.pack(fill="x", padx=10, pady=5)
        
        self.produtos_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="Produtos",
            command=self.mostrar_produtos,
            fg_color="#3498db",
            hover_color="#2980b9",
            height=40
        )
        self.produtos_btn.pack(fill="x", padx=10, pady=5)
        
        self.vendas_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="Histórico de Vendas",
            command=self.mostrar_historico_vendas,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            height=40
        )
        self.vendas_btn.pack(fill="x", padx=10, pady=5)
        
        self.fiscal_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="Fiscal",
            command=self.mostrar_fiscal,
            fg_color="#9b59b6",
            hover_color="#8e44ad",
            height=40
        )
        self.fiscal_btn.pack(fill="x", padx=10, pady=5)
        
        self.relatorios_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="Relatórios",
            command=self.mostrar_relatorios,
            fg_color="#f39c12",
            hover_color="#d35400",
            height=40
        )
        self.relatorios_btn.pack(fill="x", padx=10, pady=5)
        
        self.config_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="Configurações",
            command=self.mostrar_configuracoes,
            fg_color="#7f8c8d",
            hover_color="#95a5a6",
            height=40
        )
        self.config_btn.pack(fill="x", padx=10, pady=5)
        
        # Versão
        version_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="v1.0.0",
            font=ctk.CTkFont(size=12)
        )
        version_label.pack(side="bottom", pady=10)
        
        # Frame de conteúdo
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Inicializa com o PDV
        self.mostrar_pdv()
    
    def limpar_content_frame(self):
        """Limpa o frame de conteúdo."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def mostrar_pdv(self):
        """Mostra a tela de PDV."""
        self.limpar_content_frame()
        self.pdv_view = VendasView(self.content_frame, self.vendas_controller)
    
    def mostrar_produtos(self):
        """Mostra a tela de produtos."""
        self.limpar_content_frame()
        self.produtos_view = ProdutosView(self.content_frame, self.produtos_controller)
    
    def mostrar_historico_vendas(self):
        """Mostra a tela de histórico de vendas."""
        self.limpar_content_frame()
        
        # Cria o controller
        historico_controller = HistoricoVendasController(self.db_controller)
        
        # Cria a view
        historico_view = HistoricoVendasView(self.content_frame, historico_controller)
    
    def mostrar_fiscal(self):
        """Mostra a tela fiscal."""
        self.limpar_content_frame()
        self.fiscal_view = FiscalView(self.content_frame, self.fiscal_controller)
    
    def mostrar_relatorios(self):
        """Mostra a tela de relatórios."""
        self.limpar_content_frame()
        # RelatoriosView only takes 3 arguments, not 4
        self.relatorios_view = RelatoriosView(
            self.content_frame, 
            self.db_controller  # Pass the database controller instead of separate controllers
        )
    
    def mostrar_configuracoes(self):
        """Mostra a tela de configurações."""
        self.limpar_content_frame()
        # Implementação futura
        label = ctk.CTkLabel(
            self.content_frame, 
            text="Configurações\n\nEm desenvolvimento...", 
            font=ctk.CTkFont(size=20)
        )
        label.pack(pady=50)
    
    def run(self):
        """Inicia a aplicação."""
        self.app.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()