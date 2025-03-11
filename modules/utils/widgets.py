import customtkinter as ctk
from tkinter import Canvas, Frame

class ScrollableLabelButtonFrame(ctk.CTkFrame):
    """
    Frame com rolagem que contém labels e botões.
    Útil para exibir listas de itens com opções de ação.
    """
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Comando a ser executado quando um botão é clicado
        self.command = command
        
        # Cria um canvas para permitir rolagem
        self.canvas = Canvas(self, bg=self._fg_color, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Adiciona uma barra de rolagem
        self.scrollbar = ctk.CTkScrollbar(self, command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        
        # Configura o canvas para usar a barra de rolagem
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Cria um frame dentro do canvas para conter os widgets
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color=self._fg_color)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Ajusta o tamanho do frame quando o canvas é redimensionado
        self.canvas.bind("<Configure>", self.adjust_frame_width)
        
        # Lista para armazenar os itens
        self.items = []
    
    def adjust_frame_width(self, event):
        """Ajusta a largura do frame interno para corresponder à largura do canvas."""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)
    
    def add_item(self, text, index=None):
        """
        Adiciona um item (label + botão) ao frame.
        
        Args:
            text (str): Texto a ser exibido no label
            index: Índice ou identificador do item (passado para o comando)
        """
        # Cria um frame para o item
        item_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=self._fg_color)
        item_frame.pack(fill="x", padx=5, pady=2)
        
        # Adiciona o label com o texto
        label = ctk.CTkLabel(item_frame, text=text, anchor="w", justify="left")
        label.pack(side="left", fill="x", expand=True, padx=5)
        
        # Adiciona o botão de remoção
        button = ctk.CTkButton(
            item_frame, 
            text="X", 
            width=30, 
            height=24,
            command=lambda i=index: self.remove_item(i)
        )
        button.pack(side="right", padx=5)
        
        # Armazena o item
        self.items.append((item_frame, label, button, index))
    
    def remove_item(self, index):
        """
        Remove um item do frame e executa o comando associado.
        
        Args:
            index: Índice ou identificador do item a ser removido
        """
        if self.command:
            self.command(index)
    
    def clear_all(self):
        """Remove todos os itens do frame."""
        for item_frame, _, _, _ in self.items:
            item_frame.destroy()
        self.items = []


class SearchableComboBox(ctk.CTkFrame):
    """
    Combobox com funcionalidade de pesquisa.
    Permite filtrar os itens conforme o usuário digita.
    """
    def __init__(self, master, values=None, command=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.values = values or []
        self.filtered_values = self.values.copy()
        self.command = command
        self.dropdown_visible = False
        
        # Cria o layout
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface do combobox."""
        # Frame principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)
        
        # Campo de entrada
        self.entry_var = ctk.StringVar()
        self.entry = ctk.CTkEntry(self.main_frame, textvariable=self.entry_var)
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<KeyRelease>", self.filter_values)
        self.entry.bind("<Return>", self.select_value)
        self.entry.bind("<Down>", self.show_dropdown)
        
        # Botão de dropdown
        self.dropdown_button = ctk.CTkButton(
            self.main_frame, 
            text="▼", 
            width=30,
            command=self.toggle_dropdown
        )
        self.dropdown_button.pack(side="right")
        
        # Frame de dropdown (inicialmente oculto)
        self.dropdown_frame = None
    
    def filter_values(self, event=None):
        """Filtra os valores com base no texto digitado."""
        search_text = self.entry_var.get().lower()
        self.filtered_values = [v for v in self.values if search_text in str(v).lower()]
        
        # Atualiza o dropdown se estiver visível
        if self.dropdown_visible:
            self.show_dropdown()
    
    def toggle_dropdown(self):
        """Alterna a visibilidade do dropdown."""
        if self.dropdown_visible:
            self.hide_dropdown()
        else:
            self.show_dropdown()
    
    def show_dropdown(self, event=None):
        """Exibe o dropdown com os valores filtrados."""
        # Destrói o dropdown existente, se houver
        if self.dropdown_frame:
            self.dropdown_frame.destroy()
        
        # Cria um novo dropdown
        self.dropdown_frame = ctk.CTkFrame(self.master)
        self.dropdown_frame.place(
            x=self.winfo_rootx() - self.master.winfo_rootx(),
            y=self.winfo_rooty() - self.master.winfo_rooty() + self.winfo_height(),
            width=self.winfo_width()
        )
        
        # Adiciona os valores filtrados
        for i, value in enumerate(self.filtered_values[:10]):  # Limita a 10 itens
            item_button = ctk.CTkButton(
                self.dropdown_frame,
                text=str(value),
                anchor="w",
                command=lambda v=value: self.select_item(v)
            )
            item_button.pack(fill="x", padx=2, pady=1)
        
        self.dropdown_visible = True
    
    def hide_dropdown(self):
        """Oculta o dropdown."""
        if self.dropdown_frame:
            self.dropdown_frame.destroy()
            self.dropdown_frame = None
        self.dropdown_visible = False
    
    def select_item(self, value):
        """Seleciona um item do dropdown."""
        self.entry_var.set(value)
        self.hide_dropdown()
        
        if self.command:
            self.command(value)
    
    def select_value(self, event=None):
        """Seleciona o valor atual do campo de entrada."""
        value = self.entry_var.get()
        self.hide_dropdown()
        
        if self.command:
            self.command(value)
    
    def get(self):
        """Retorna o valor atual do campo de entrada."""
        return self.entry_var.get()
    
    def set(self, value):
        """Define o valor do campo de entrada."""
        self.entry_var.set(value)


class NumericEntry(ctk.CTkEntry):
    """
    Campo de entrada que aceita apenas números.
    Pode ser configurado para aceitar números inteiros ou decimais.
    """
    def __init__(self, master, decimal=False, **kwargs):
        super().__init__(master, **kwargs)
        
        self.decimal = decimal
        self.bind("<KeyRelease>", self.validate)
    
    def validate(self, event=None):
        """Valida o conteúdo do campo para garantir que seja numérico."""
        value = self.get()
        
        if not value:
            return
        
        if self.decimal:
            # Permite números decimais (com ponto ou vírgula)
            value = value.replace(",", ".")
            try:
                float(value)
                # Formata para ter no máximo 2 casas decimais
                formatted = "{:.2f}".format(float(value))
                if value != formatted and len(value.split(".")[1]) > 2:
                    self.delete(0, "end")
                    self.insert(0, formatted)
            except ValueError:
                # Remove caracteres não numéricos, exceto ponto decimal
                new_value = ''.join(c for c in value if c.isdigit() or c == '.')
                # Garante que há apenas um ponto decimal
                if new_value.count('.') > 1:
                    new_value = new_value[:new_value.rfind('.')] + new_value[new_value.rfind('.'):]
                
                self.delete(0, "end")
                self.insert(0, new_value)
        else:
            # Permite apenas números inteiros
            if not value.isdigit():
                new_value = ''.join(c for c in value if c.isdigit())
                self.delete(0, "end")
                self.insert(0, new_value)