import customtkinter as ctk
from tkinter import messagebox
import os
import sys

# Adiciona o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importa os módulos do sistema
from modules.database.db_controller import DatabaseController
from modules.produtos.produtos_view import ProdutosView
from modules.produtos.produtos_controller import ProdutosController
from modules.pdv.pdv_view import PDVView
from modules.pdv.pdv_controller import PDVController
from modules.relatorios.relatorios_view import RelatoriosView
from modules.clientes.clientes_view import ClientesView
from modules.clientes.clientes_controller import ClientesController

class App:
    def __init__(self):
        # Configuração do tema
        ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        
        # Cria a janela principal
        self.root = ctk.CTk()
        self.root.title("Sistema de PDV e Estoque")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Inicializa o banco de dados
        self.db_controller = DatabaseController("database.db")
        self.db_controller.criar_tabelas()
        
        # Inicializa os controllers
        self.produtos_controller = ProdutosController(self.db_controller)
        self.pdv_controller = PDVController(self.db_controller)
        self.clientes_controller = ClientesController(self.db_controller)
        
        # Cria o layout principal
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        
        # Frame para o menu lateral
        self.sidebar_frame = ctk.CTkFrame(self.main_frame, width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y", padx=0, pady=0)
        
        # Logo ou título do sistema
        logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="PDV & Estoque", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        logo_label.pack(padx=20, pady=20)
        
        # Botões do menu
        self.pdv_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="PDV", 
            command=self.mostrar_pdv,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            height=40
        )
        self.pdv_btn.pack(padx=20, pady=10, fill="x")
        
        self.produtos_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="Produtos", 
            command=self.mostrar_produtos,
            fg_color="#3498db",
            hover_color="#2980b9",
            height=40
        )
        self.produtos_btn.pack(padx=20, pady=10, fill="x")
        
        self.clientes_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="Clientes", 
            command=self.mostrar_clientes,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            height=40
        )
        self.clientes_btn.pack(padx=20, pady=10, fill="x")
        
        self.relatorios_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="Relatórios", 
            command=self.mostrar_relatorios,
            fg_color="#9b59b6",
            hover_color="#8e44ad",
            height=40
        )
        self.relatorios_btn.pack(padx=20, pady=10, fill="x")
        
        # Frame para o conteúdo
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=0, pady=0)
        
        # Inicializa com a tela de PDV
        self.mostrar_pdv()
        
    def limpar_content_frame(self):
        """Limpa o frame de conteúdo para mostrar uma nova tela."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def mostrar_pdv(self):
        """Mostra a tela de PDV."""
        self.limpar_content_frame()
        PDVView(self.content_frame, self.pdv_controller)
        
        # Atualiza o estilo dos botões
        self.pdv_btn.configure(fg_color="#3498db")
        self.produtos_btn.configure(fg_color="#e74c3c")
        self.clientes_btn.configure(fg_color="#2ecc71")
        self.relatorios_btn.configure(fg_color="#9b59b6")
    
    def mostrar_clientes(self):
        """Mostra a tela de clientes."""
        self.limpar_content_frame()
        ClientesView(self.content_frame, self.clientes_controller)
        
        # Atualiza o estilo dos botões
        self.pdv_btn.configure(fg_color="#3498db")
        self.produtos_btn.configure(fg_color="#2ecc71")
        self.clientes_btn.configure(fg_color="#e74c3c")
        self.relatorios_btn.configure(fg_color="#9b59b6")
    
    def mostrar_relatorios(self):
        """Mostra a tela de relatórios."""
        self.limpar_content_frame()
        RelatoriosView(self.content_frame, self.db_controller)
        
        # Atualiza o estilo dos botões
        self.pdv_btn.configure(fg_color="#3498db")
        self.produtos_btn.configure(fg_color="#2ecc71")
        self.clientes_btn.configure(fg_color="#9b59b6")
        self.relatorios_btn.configure(fg_color="#e74c3c")
    
    def run(self):
        """Inicia a aplicação."""
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()