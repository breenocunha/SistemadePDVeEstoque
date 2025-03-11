import customtkinter as ctk
from tkinter import messagebox
from ..utils.widgets import NumericEntry

def abrir_form_produto(parent, controller, callback, produto_id=None):
    """Abre o formulário para adicionar ou editar um produto."""
    # Cria uma nova janela
    produto_window = ctk.CTkToplevel(parent)
    produto_window.title("Novo Produto" if not produto_id else "Editar Produto")
    produto_window.geometry("600x650")
    produto_window.grab_set()  # Torna a janela modal
    
    # Título
    title_label = ctk.CTkLabel(
        produto_window, 
        text="CADASTRO DE PRODUTO", 
        font=ctk.CTkFont(size=20, weight="bold")
    )
    title_label.pack(pady=10)
    
    # Frame principal
    main_frame = ctk.CTkScrollableFrame(produto_window)
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Formulário
    # Código
    codigo_label = ctk.CTkLabel(main_frame, text="Código:")
    codigo_label.pack(anchor="w", padx=10, pady=5)
    
    codigo_var = ctk.StringVar()
    codigo_entry = ctk.CTkEntry(main_frame, textvariable=codigo_var, width=300)
    codigo_entry.pack(fill="x", padx=10, pady=5)
    
    # Nome
    nome_label = ctk.CTkLabel(main_frame, text="Nome:")
    nome_label.pack(anchor="w", padx=10, pady=5)
    
    nome_var = ctk.StringVar()
    nome_entry = ctk.CTkEntry(main_frame, textvariable=nome_var, width=300)
    nome_entry.pack(fill="x", padx=10, pady=5)
    
    # Descrição
    descricao_label = ctk.CTkLabel(main_frame, text="Descrição:")
    descricao_label.pack(anchor="w", padx=10, pady=5)
    
    descricao_var = ctk.StringVar()
    descricao_entry = ctk.CTkEntry(main_frame, textvariable=descricao_var, width=300)
    descricao_entry.pack(fill="x", padx=10, pady=5)
    
    # Categoria
    categoria_label = ctk.CTkLabel(main_frame, text="Categoria:")
    categoria_label.pack(anchor="w", padx=10, pady=5)
    
    categorias = controller.listar_categorias()
    categoria_options = [f"{cat['id']} - {cat['nome']}" for cat in categorias]
    
    categoria_var = ctk.StringVar()
    categoria_combobox = ctk.CTkComboBox(
        main_frame, 
        values=categoria_options,
        variable=categoria_var,
        width=300
    )
    categoria_combobox.pack(fill="x", padx=10, pady=5)
    
    # Fornecedor
    fornecedor_label = ctk.CTkLabel(main_frame, text="Fornecedor:")
    fornecedor_label.pack(anchor="w", padx=10, pady=5)
    
    fornecedores = controller.listar_fornecedores()
    fornecedor_options = [f"{forn['id']} - {forn['nome']}" for forn in fornecedores]
    
    fornecedor_var = ctk.StringVar()
    fornecedor_combobox = ctk.CTkComboBox(
        main_frame, 
        values=fornecedor_options,
        variable=fornecedor_var,
        width=300
    )
    fornecedor_combobox.pack(fill="x", padx=10, pady=5)
    
    # Preço de custo
    preco_custo_label = ctk.CTkLabel(main_frame, text="Preço de Custo (R$):")
    preco_custo_label.pack(anchor="w", padx=10, pady=5)
    
    preco_custo_var = ctk.StringVar()
    preco_custo_entry = NumericEntry(main_frame, decimal=True, textvariable=preco_custo_var, width=300)
    preco_custo_entry.pack(fill="x", padx=10, pady=5)
    
    # Preço de venda
    preco_venda_label = ctk.CTkLabel(main_frame, text="Preço de Venda (R$):")
    preco_venda_label.pack(anchor="w", padx=10, pady=5)
    
    preco_venda_var = ctk.StringVar()
    preco_venda_entry = NumericEntry(main_frame, decimal=True, textvariable=preco_venda_var, width=300)
    preco_venda_entry.pack(fill="x", padx=10, pady=5)
    
    # Estoque atual
    estoque_atual_label = ctk.CTkLabel(main_frame, text="Estoque Atual:")
    estoque_atual_label.pack(anchor="w", padx=10, pady=5)
    
    estoque_atual_var = ctk.StringVar()
    estoque_atual_entry = NumericEntry(main_frame, textvariable=estoque_atual_var, width=300)
    estoque_atual_entry.pack(fill="x", padx=10, pady=5)
    
    # Estoque mínimo
    estoque_minimo_label = ctk.CTkLabel(main_frame, text="Estoque Mínimo:")
    estoque_minimo_label.pack(anchor="w", padx=10, pady=5)
    
    estoque_minimo_var = ctk.StringVar()
    estoque_minimo_entry = NumericEntry(main_frame, textvariable=estoque_minimo_var, width=300)
    estoque_minimo_entry.pack(fill="x", padx=10, pady=5)
    
    # Unidade
    unidade_label = ctk.CTkLabel(main_frame, text="Unidade:")
    unidade_label.pack(anchor="w", padx=10, pady=5)
    
    unidade_var = ctk.StringVar(value="UN")
    unidade_entry = ctk.CTkEntry(main_frame, textvariable=unidade_var, width=300)
    unidade_entry.pack(fill="x", padx=10, pady=5)
    
    # Localização
    localizacao_label = ctk.CTkLabel(main_frame, text="Localização:")
    localizacao_label.pack(anchor="w", padx=10, pady=5)
    
    localizacao_var = ctk.StringVar()
    localizacao_entry = ctk.CTkEntry(main_frame, textvariable=localizacao_var, width=300)
    localizacao_entry.pack(fill="x", padx=10, pady=5)
    
    # Código de barras
    codigo_barras_label = ctk.CTkLabel(main_frame, text="Código de Barras:")
    codigo_barras_label.pack(anchor="w", padx=10, pady=5)
    
    codigo_barras_var = ctk.StringVar()
    codigo_barras_entry = ctk.CTkEntry(main_frame, textvariable=codigo_barras_var, width=300)
    codigo_barras_entry.pack(fill="x", padx=10, pady=5)
    
    # Frame de botões
    botoes_frame = ctk.CTkFrame(produto_window, fg_color="transparent")
    botoes_frame.pack(fill="x", padx=20, pady=20)
    
    # Se estiver editando, carrega os dados do produto
    if produto_id:
        produto = controller.obter_produto(produto_id)
        if produto:
            codigo_var.set(produto["codigo"])
            nome_var.set(produto["nome"])
            descricao_var.set(produto["descricao"] or "")
            
            # Seleciona a categoria
            if produto["categoria_id"]:
                for i, cat in enumerate(categorias):
                    if cat["id"] == produto["categoria_id"]:
                        categoria_combobox.set(categoria_options[i])
                        break
            
            # Seleciona o fornecedor
            if produto["fornecedor_id"]:
                for i, forn in enumerate(fornecedores):
                    if forn["id"] == produto["fornecedor_id"]:
                        fornecedor_combobox.set(fornecedor_options[i])
                        break
            
            preco_custo_var.set(str(produto["preco_custo"]))
            preco_venda_var.set(str(produto["preco_venda"]))
            estoque_atual_var.set(str(produto["estoque_atual"]))
            estoque_minimo_var.set(str(produto["estoque_minimo"]))
            unidade_var.set(produto["unidade"] or "UN")
            localizacao_var.set(produto["localizacao"] or "")
            codigo_barras_var.set(produto["codigo_barras"] or "")
    
    # Função para salvar o produto
    def salvar():
        # Validação básica
        if not codigo_var.get() or not nome_var.get():
            messagebox.showerror("Erro", "Código e Nome são campos obrigatórios.")
            return
        
        try:
            preco_custo = float(preco_custo_var.get() or 0)
            preco_venda = float(preco_venda_var.get() or 0)
            estoque_atual = int(estoque_atual_var.get() or 0)
            estoque_minimo = int(estoque_minimo_var.get() or 0)
        except ValueError:
            messagebox.showerror("Erro", "Valores numéricos inválidos.")
            return
        
        # Prepara os dados do produto
        produto_data = {
            "codigo": codigo_var.get(),
            "nome": nome_var.get(),
            "descricao": descricao_var.get(),
            "preco_custo": preco_custo,
            "preco_venda": preco_venda,
            "estoque_atual": estoque_atual,
            "estoque_minimo": estoque_minimo,
            "unidade": unidade_var.get(),
            "localizacao": localizacao_var.get(),
            "codigo_barras": codigo_barras_var.get()
        }
        
        # Extrai os IDs da categoria e fornecedor selecionados
        if categoria_var.get():
            try:
                categoria_id = int(categoria_var.get().split(" - ")[0])
                produto_data["categoria_id"] = categoria_id
            except (ValueError, IndexError):
                pass
        
        if fornecedor_var.get():
            try:
                fornecedor_id = int(fornecedor_var.get().split(" - ")[0])
                produto_data["fornecedor_id"] = fornecedor_id
            except (ValueError, IndexError):
                pass
        
        # Salva o produto
        if produto_id:
            produto_data["id"] = produto_id
            resultado = controller.atualizar_produto(produto_data)
            mensagem = "Produto atualizado com sucesso!"
        else:
            resultado = controller.adicionar_produto(produto_data)
            mensagem = "Produto adicionado com sucesso!"
        
        if isinstance(resultado, dict) and "erro" in resultado:
            messagebox.showerror("Erro", resultado["erro"])
        elif resultado:
            messagebox.showinfo("Sucesso", mensagem)
            produto_window.destroy()
            callback()
        else:
            messagebox.showerror("Erro", "Não foi possível salvar o produto.")
    
    # Botões de salvar e cancelar
    salvar_btn = ctk.CTkButton(
        botoes_frame, 
        text="Salvar", 
        command=salvar
    )
    salvar_btn.pack(side="left", padx=5)
    
    cancelar_btn = ctk.CTkButton(
        botoes_frame, 
        text="Cancelar", 
        command=produto_window.destroy
    )
    cancelar_btn.pack(side="right", padx=5)