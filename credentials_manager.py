"""
Sistema de Credenciais para AI Studio
Verifica variáveis de ambiente e arquivos de configuração
"""

import os
import json
from typing import Optional, Dict

class CredentialsManager:
    def __init__(self):
        self.accounts = {
            'thiago.edu511@gmail.com': 'Thiagao15@',
            'steveplayer120@gmail.com': 'Thiagao15@'
        }
        self.current_account = None
        self.load_credentials()
    
    def load_credentials(self):
        """Carrega credenciais de múltiplas fontes"""
        print("🔑 Verificando credenciais disponíveis...")
        
        # 1. Variáveis de ambiente
        env_creds = self.get_env_credentials()
        if env_creds:
            # Adicionar conta das variáveis de ambiente
            email = env_creds.get('email')
            password = env_creds.get('password')
            if email and password:
                self.accounts[email] = password
                self.current_account = email
                print(f"✅ Conta adicionada de variáveis de ambiente: {email}")
        
        # 2. Arquivo de configuração
        file_creds = self.get_file_credentials()
        if file_creds:
            email = file_creds.get('email')
            password = file_creds.get('password')
            if email and password:
                self.accounts[email] = password
                self.current_account = email
                print(f"✅ Conta adicionada de arquivo: {email}")
        
        # 3. Verificar se tem o mínimo necessário
        if self.has_valid_credentials():
            print(f"✅ {len(self.accounts)} conta(s) disponível(is)!")
            for email in self.accounts.keys():
                print(f"   📧 {email}")
        else:
            print(f"⚠️ Usando contas padrão configuradas")
    
    def get_accounts(self) -> dict:
        """Retorna todas as contas disponíveis"""
        return self.accounts
    
    def get_password_for_email(self, email: str) -> Optional[str]:
        """Retorna senha para um email específico"""
        return self.accounts.get(email)
    
    def has_valid_credentials(self) -> bool:
        """Verifica se há credenciais válidas"""
        return len(self.accounts) > 0
    
    def get_email(self) -> Optional[str]:
        """Retorna email atual ou primeiro disponível"""
        if self.current_account:
            return self.current_account
        emails = list(self.accounts.keys())
        return emails[0] if emails else None
    
    def get_password(self) -> Optional[str]:
        """Retorna senha para email atual"""
        email = self.get_email()
        return self.accounts.get(email) if email else None
    
    def set_current_account(self, email: str):
        """Define conta atual"""
        if email in self.accounts:
            self.current_account = email
            print(f"🔄 Conta atual: {email}")
            return True
        return False
    
    def get_env_credentials(self) -> Optional[Dict]:
        """Busca credenciais em variáveis de ambiente"""
        env_vars = [
            # Google/Gmail
            ('GOOGLE_EMAIL', 'email'),
            ('GOOGLE_USER', 'email'),
            ('GMAIL_EMAIL', 'email'),
            ('EMAIL', 'email'),
            
            # Senhas
            ('GOOGLE_PASSWORD', 'password'),
            ('GOOGLE_PASS', 'password'),
            ('GMAIL_PASSWORD', 'password'),
            ('PASSWORD', 'password'),
            
            # AI Studio específico
            ('AI_STUDIO_EMAIL', 'email'),
            ('AI_STUDIO_PASSWORD', 'password'),
            ('AISTUDIO_EMAIL', 'email'),
            ('AISTUDIO_PASSWORD', 'password'),
        ]
        
        creds = {}
        for env_var, key in env_vars:
            value = os.getenv(env_var)
            if value:
                creds[key] = value
                print(f"   📧 {env_var} -> {key}")
        
        return creds if creds else None
    
    def get_file_credentials(self) -> Optional[Dict]:
        """Busca credenciais em arquivos de configuração"""
        config_files = [
            '/workspaces/replit/.env',
            '/workspaces/replit/config.json',
            '/workspaces/replit/credentials.json',
            '/workspaces/replit/.config/credentials.json',
        ]
        
        for config_file in config_files:
            if os.path.exists(config_file):
                try:
                    if config_file.endswith('.json'):
                        with open(config_file, 'r') as f:
                            data = json.load(f)
                            if 'google' in data:
                                return data['google']
                            elif 'ai_studio' in data:
                                return data['ai_studio']
                            elif 'email' in data or 'password' in data:
                                return data
                    elif config_file.endswith('.env'):
                        # Ler arquivo .env
                        creds = {}
                        with open(config_file, 'r') as f:
                            for line in f:
                                if '=' in line and not line.startswith('#'):
                                    key, value = line.strip().split('=', 1)
                                    if 'email' in key.lower():
                                        creds['email'] = value.strip('"\'')
                                    elif 'pass' in key.lower():
                                        creds['password'] = value.strip('"\'')
                        if creds:
                            print(f"   📁 {config_file}")
                            return creds
                except Exception as e:
                    print(f"   ❌ Erro lendo {config_file}: {e}")
        
        return None
    
    def show_configuration_help(self):
        """Mostra ajuda de configuração"""
        print("\n🔧 COMO CONFIGURAR CREDENCIAIS:")
        print("=" * 40)
        
        print("\n📋 OPÇÃO 1 - Variáveis de Ambiente:")
        print("export GOOGLE_EMAIL='seu_email@gmail.com'")
        print("export GOOGLE_PASSWORD='sua_senha'")
        
        print("\n📋 OPÇÃO 2 - Arquivo config.json:")
        print("Criar: /workspaces/replit/config.json")
        print(json.dumps({
            "google": {
                "email": "seu_email@gmail.com",
                "password": "sua_senha"
            }
        }, indent=2))
        
        print("\n📋 OPÇÃO 3 - Arquivo .env:")
        print("Criar: /workspaces/replit/.env")
        print("GOOGLE_EMAIL=seu_email@gmail.com")
        print("GOOGLE_PASSWORD=sua_senha")
        
        print("\n⚠️ IMPORTANTE:")
        print("• Use senha de app se tiver 2FA ativado")
        print("• Nunca commite credenciais no git")
        print("• Adicione .env e config.json no .gitignore")
    
    def create_sample_config(self):
        """Cria arquivo de configuração de exemplo"""
        config_path = "/workspaces/replit/config.example.json"
        sample_config = {
            "google": {
                "email": "seu_email@gmail.com",
                "password": "sua_senha_ou_app_password"
            },
            "notes": [
                "Renomeie este arquivo para config.json",
                "Use senha de aplicativo se tiver 2FA",
                "Adicione config.json no .gitignore"
            ]
        }
        
        with open(config_path, 'w') as f:
            json.dump(sample_config, f, indent=2)
        
        print(f"📄 Arquivo de exemplo criado: {config_path}")

def main():
    """Teste do sistema de credenciais"""
    print("🔍 VERIFICAÇÃO DE CREDENCIAIS")
    print("=" * 35)
    
    creds = CredentialsManager()
    
    if creds.has_valid_credentials():
        print(f"\n✅ CREDENCIAIS ENCONTRADAS!")
        print(f"📧 Email: {creds.get_email()}")
        print(f"🔒 Senha: {'*' * len(creds.get_password())}")
        print(f"\n🚀 Sistema pronto para login automático!")
    else:
        print(f"\n⚠️ CREDENCIAIS NÃO ENCONTRADAS")
        print(f"ℹ️ Configure suas credenciais para uso automático")
        
        # Criar arquivo de exemplo
        creds.create_sample_config()

if __name__ == "__main__":
    main()
