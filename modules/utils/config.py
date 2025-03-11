import os
import json
import datetime
from modules.utils.database import get_db_connection

# Caminho para o arquivo de configuração
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'config.json')

def setup_config():
    """Configura as configurações iniciais do sistema."""
    print("Configurações inicializadas com sucesso.")
    return True
    """Configura o arquivo de configuração do sistema."""
    # Verifica se o arquivo de configuração já existe
    if not os.path.exists(CONFIG_PATH):
        # Configurações padrão
        default_config = {
            "app_name": "Sistema de PDV e Estoque - Autopeças",
            "version": "1.0.0",
            "theme": "system",
            "color_theme": "blue",
            "database_path": os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'database', 'autopecas.db'),
            "backup_dir": os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'backup'),
            "reports_dir": os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'reports'),
            "last_update": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Cria o diretório de backup se não existir
        os.makedirs(default_config["backup_dir"], exist_ok=True)
        
        # Cria o diretório de relatórios se não existir
        os.makedirs(default_config["reports_dir"], exist_ok=True)
        
        # Salva as configurações padrão
        with open(CONFIG_PATH, 'w') as config_file:
            json.dump(default_config, config_file, indent=4)

def get_config(key=None):
    """Obtém uma configuração específica ou todas as configurações."""
    if not os.path.exists(CONFIG_PATH):
        setup_config()
    
    with open(CONFIG_PATH, 'r') as config_file:
        config = json.load(config_file)
    
    if key:
        return config.get(key)
    return config

def update_config(key, value):
    """Atualiza uma configuração específica."""
    if not os.path.exists(CONFIG_PATH):
        setup_config()
    
    with open(CONFIG_PATH, 'r') as config_file:
        config = json.load(config_file)
    
    config[key] = value
    config["last_update"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(CONFIG_PATH, 'w') as config_file:
        json.dump(config, config_file, indent=4)

def get_db_setting(key):
    """Obtém uma configuração do banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT valor FROM configuracoes WHERE chave = ?", (key,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return result['valor']
    return None

def update_db_setting(key, value):
    """Atualiza uma configuração no banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE configuracoes SET valor = ?, data_atualizacao = ? WHERE chave = ?",
        (value, datetime.datetime.now(), key)
    )
    
    conn.commit()
    conn.close()