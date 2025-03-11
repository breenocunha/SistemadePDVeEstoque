import os
import json
import datetime

class FiscalController:
    def __init__(self, db_controller):
        self.db_controller = db_controller
        self.nfce_file = os.path.join(os.path.dirname(__file__), "data", "nfce.json")
        self.ensure_data_dir()
    
    def ensure_data_dir(self):
        """Garante que o diretório de dados existe."""
        data_dir = os.path.dirname(self.nfce_file)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def emitir_nfce(self, venda_data):
        """Emite uma NFC-e para a venda."""
        # Em um sistema real, aqui seria feita a integração com a API da SEFAZ
        # Para fins de demonstração, vamos apenas simular a emissão
        
        # Gera um número de NFC-e fictício
        numero = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Gera uma chave de acesso fictícia
        chave_acesso = f"NFCe{numero}{'0' * 34}"
        
        # Gera um protocolo fictício
        protocolo = f"PROT{numero}"
        
        # Prepara os dados da NFC-e
        nfce_data = {
            "venda_id": venda_data["id"],
            "numero": numero,
            "chave_acesso": chave_acesso,
            "protocolo": protocolo,
            "data_emissao": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Autorizada",
            "itens": venda_data["itens"],
            "cliente": venda_data["cliente"],
            "total": venda_data["total"]
        }
        
        # Salva a NFC-e
        nfces = self._carregar_nfces()
        nfces.append(nfce_data)
        self._salvar_nfces(nfces)
        
        return {
            "sucesso": True, 
            "numero": numero, 
            "chave_acesso": chave_acesso, 
            "protocolo": protocolo
        }
    
    def cancelar_nfce(self, nfce_numero):
        """Cancela uma NFC-e pelo número."""
        # Em um sistema real, aqui seria feita a integração com a API da SEFAZ
        # Para fins de demonstração, vamos apenas simular o cancelamento
        
        nfces = self._carregar_nfces()
        
        for i, nfce in enumerate(nfces):
            if nfce["numero"] == nfce_numero:
                nfces[i]["status"] = "Cancelada"
                nfces[i]["data_cancelamento"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._salvar_nfces(nfces)
                return {"sucesso": True}
        
        return {"sucesso": False, "mensagem": "NFC-e não encontrada."}
    
    def listar_nfces(self):
        """Lista todas as NFC-e emitidas."""
        return self._carregar_nfces()
    
    def obter_nfce(self, nfce_numero):
        """Obtém uma NFC-e pelo número."""
        nfces = self._carregar_nfces()
        
        for nfce in nfces:
            if nfce["numero"] == nfce_numero:
                return nfce
        
        return None
    
    def _carregar_nfces(self):
        """Carrega as NFC-e do arquivo JSON."""
        if not os.path.exists(self.nfce_file):
            return []
        
        try:
            with open(self.nfce_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar NFC-e: {str(e)}")
            return []
    
    def _salvar_nfces(self, nfces):
        """Salva as NFC-e no arquivo JSON."""
        try:
            with open(self.nfce_file, 'w', encoding='utf-8') as f:
                json.dump(nfces, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Erro ao salvar NFC-e: {str(e)}")
            return False
    
    # Find the incomplete method and fix it:
    def obter_configuracoes(self):
        """
        Obtém as configurações fiscais do sistema.
        
        Returns:
            dict: Configurações fiscais ou valores padrão se não encontradas
        """
        try:
            # Verifica se a tabela de configurações existe
            check_table = """
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='configuracoes_fiscais'
            """
            result = self.db_controller.execute_query(check_table)
            
            # Se a tabela não existir, cria ela
            if not result:
                self.criar_tabela_configuracoes()
                return self.get_configuracoes_padrao()
            
            # Consulta as configurações
            query = "SELECT * FROM configuracoes_fiscais LIMIT 1"
            result = self.db_controller.execute_query(query)
            
            # Se não houver configurações, retorna os valores padrão
            if not result:
                return self.get_configuracoes_padrao()
            
            # Retorna as configurações encontradas
            return dict(result[0])
        except Exception as e:
            print(f"Erro ao obter configurações fiscais: {str(e)}")
            return self.get_configuracoes_padrao()
    
    def criar_tabela_configuracoes(self):
        """Cria a tabela de configurações fiscais."""
        try:
            query = """
                CREATE TABLE IF NOT EXISTS configuracoes_fiscais (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cnpj TEXT,
                    razao_social TEXT,
                    nome_fantasia TEXT,
                    inscricao_estadual TEXT,
                    regime_tributario TEXT,
                    ambiente TEXT DEFAULT 'Homologação',
                    certificado_path TEXT,
                    certificado_senha TEXT,
                    ultima_atualizacao TEXT
                )
            """
            self.db_controller.execute_query(query)
            
            # Insere as configurações padrão
            config_padrao = self.get_configuracoes_padrao()
            
            # Remove o id do dicionário para que seja autoincrement
            if 'id' in config_padrao:
                del config_padrao['id']
            
            # Constrói a query de inserção
            campos = ', '.join(config_padrao.keys())
            placeholders = ', '.join(['?' for _ in config_padrao])
            
            query = f"""
                INSERT INTO configuracoes_fiscais ({campos})
                VALUES ({placeholders})
            """
            
            self.db_controller.execute_query(query, list(config_padrao.values()))
            
            print("Tabela de configurações fiscais criada com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao criar tabela de configurações fiscais: {str(e)}")
            return False
        
    def get_configuracoes_padrao(self):
        """Retorna as configurações fiscais padrão."""
        return {
            'razao_social': 'Minha Empresa LTDA',
            'nome_fantasia': 'Minha Empresa',
            'cnpj': '00.000.000/0000-00',
            'inscricao_estadual': 'ISENTO',
            'inscricao_municipal': 'ISENTO',
            'endereco': 'Rua Exemplo, 123',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'cep': '00000-000',
            'telefone': '(00) 0000-0000',
            'email': 'contato@minhaempresa.com',
            'regime_tributario': 'Simples Nacional',
            'ambiente_nfe': 'Homologação',
            'certificado_caminho': '',
            'certificado_senha': '',
            'serie_nfe': 1,
            'proxima_numeracao': 1
        }

    def salvar_configuracoes(self, config):
        """
        Salva as configurações fiscais no banco de dados.
        
        Args:
            config (dict): Dicionário com as configurações a serem salvas
        
        Returns:
            dict: Resultado da operação
                - sucesso (bool): True se a operação foi bem-sucedida
                - mensagem (str): Mensagem de resultado
        """
        try:
            # Verifica se a tabela existe
            check_table = """
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='configuracoes_fiscais'
            """
            result = self.db_controller.execute_query(check_table)
            
            # Se a tabela não existir, cria ela
            if not result:
                self.criar_tabela_configuracoes()
            
            # Verifica se já existem configurações
            query_check = "SELECT id FROM configuracoes_fiscais LIMIT 1"
            result = self.db_controller.execute_query(query_check)
            
            if result:
                # Atualiza as configurações existentes
                config_id = result[0]['id']
                
                # Constrói a query de atualização
                campos = []
                valores = []
                
                for campo, valor in config.items():
                    campos.append(f"{campo} = ?")
                    valores.append(valor)
                
                query = f"""
                    UPDATE configuracoes_fiscais 
                    SET {', '.join(campos)}
                    WHERE id = ?
                """
                valores.append(config_id)
                
                self.db_controller.execute_query(query, valores)
            else:
                # Insere novas configurações
                campos = ', '.join(config.keys())
                placeholders = ', '.join(['?' for _ in config])
                
                query = f"""
                    INSERT INTO configuracoes_fiscais ({campos})
                    VALUES ({placeholders})
                """
                
                self.db_controller.execute_query(query, list(config.values()))
            
            return {"sucesso": True, "mensagem": "Configurações salvas com sucesso!"}
            
        except Exception as e:
            print(f"Erro ao salvar configurações fiscais: {str(e)}")
            return {"sucesso": False, "mensagem": f"Erro ao salvar configurações: {str(e)}"}

    def listar_vendas_periodo(self, data_inicio, data_fim):
        """Lista as vendas em um período específico."""
        try:
            query = """
                SELECT v.id, v.data, v.total, v.forma_pagamento, v.status,
                       COUNT(i.id) as itens_count
                FROM vendas v
                LEFT JOIN itens_venda i ON v.id = i.venda_id
                WHERE v.data BETWEEN ? AND ?
                GROUP BY v.id
                ORDER BY v.data DESC
            """
            
            result = self.db_controller.execute_query(query, (data_inicio, data_fim))
            
            # Converte os resultados para uma lista de dicionários
            vendas = []
            for row in result:
                vendas.append(dict(row))
            
            return vendas
        except Exception as e:
            print(f"Erro ao listar vendas do período: {str(e)}")
            return []