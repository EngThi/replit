#!/usr/bin/env python3
"""
🚀 AI Studio - Login via Requests (Sem GUI)
Sistema alternativo usando requests HTTP diretos
"""

import requests
import json
import time
import re
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from credentials_manager import CredentialsManager

class AIStudioLoginHTTP:
    def __init__(self):
        self.credentials = CredentialsManager()
        self.session = requests.Session()
        
        # Headers para simular navegador
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
    def extract_form_data(self, html):
        """Extrai dados do formulário de login"""
        form_data = {}
        
        # Buscar valores de input hidden
        input_patterns = [
            r'<input[^>]+name="([^"]+)"[^>]+value="([^"]*)"',
            r'<input[^>]+value="([^"]*)"[^>]+name="([^"]+)"'
        ]
        
        for pattern in input_patterns:
            matches = re.findall(pattern, html)
            for match in matches:
                if len(match) == 2:
                    name, value = match
                    form_data[name] = value
                    
        return form_data
        
    def get_login_form_url(self, response_text):
        """Extrai URL do formulário de login"""
        # Procurar por action do form
        action_match = re.search(r'<form[^>]+action="([^"]*)"', response_text)
        if action_match:
            return action_match.group(1)
        return None
        
    def login_google(self):
        """Executa login no Google via requests"""
        print("\n🔐 INICIANDO LOGIN VIA HTTP")
        print("=" * 50)
        
        # Obter credenciais
        email = self.credentials.get_email()
        password = self.credentials.get_password()
        
        if not email or not password:
            print("❌ Credenciais não encontradas")
            return False
        
        print(f"📧 Email: {email}")
        
        try:
            # 1. Acessar página inicial do AI Studio
            print("🌐 Acessando AI Studio...")
            ai_studio_url = "https://aistudio.google.com/"
            response = self.session.get(ai_studio_url)
            
            if response.status_code != 200:
                print(f"❌ Erro ao acessar AI Studio: {response.status_code}")
                return False
                
            # 2. Seguir redirecionamento para login
            print("🔄 Seguindo redirecionamento para login...")
            if "accounts.google.com" in response.url:
                login_page = response.text
            else:
                # Procurar link de login
                login_url = "https://accounts.google.com/signin"
                response = self.session.get(login_url)
                login_page = response.text
                
            # 3. Extrair dados do formulário
            print("📋 Extraindo dados do formulário...")
            form_data = self.extract_form_data(login_page)
            
            # Adicionar email
            form_data['identifier'] = email
            form_data['Email'] = email
            
            print(f"📝 Dados do formulário: {list(form_data.keys())}")
            
            # 4. Enviar email
            print("📧 Enviando email...")
            email_url = "https://accounts.google.com/signin/v2/identifier"
            
            response = self.session.post(email_url, data=form_data)
            
            if response.status_code != 200:
                print(f"❌ Erro ao enviar email: {response.status_code}")
                return False
                
            # 5. Extrair dados para senha
            print("🔑 Preparando envio de senha...")
            password_page = response.text
            form_data = self.extract_form_data(password_page)
            
            # Adicionar senha
            form_data['password'] = password
            form_data['Passwd'] = password
            
            # 6. Enviar senha
            print("🔐 Enviando senha...")
            password_url = "https://accounts.google.com/signin/v2/challenge/pwd"
            
            response = self.session.post(password_url, data=form_data)
            
            if response.status_code != 200:
                print(f"❌ Erro ao enviar senha: {response.status_code}")
                return False
                
            # 7. Verificar se login funcionou
            print("✅ Verificando resultado do login...")
            
            # Tentar acessar AI Studio novamente
            response = self.session.get("https://aistudio.google.com/")
            
            if "accounts.google.com" not in response.url:
                print("✅ LOGIN REALIZADO COM SUCESSO!")
                return True
            else:
                print("❌ Login falhou - ainda redirecionando para accounts.google.com")
                
                # Verificar se precisa de 2FA
                if "challenge" in response.text or "verify" in response.text:
                    print("🔐 2FA NECESSÁRIO!")
                    print("📱 Este método não suporta 2FA automático")
                    print("💡 Use o sistema com GUI para 2FA manual")
                    return False
                    
                return False
                
        except Exception as e:
            print(f"❌ Erro durante login: {e}")
            return False
            
    def test_ai_studio_access(self):
        """Testa acesso ao AI Studio"""
        print("\n🧪 TESTANDO ACESSO AO AI STUDIO")
        print("=" * 50)
        
        try:
            # Tentar acessar nova conversa
            chat_url = "https://aistudio.google.com/prompts/new_chat"
            response = self.session.get(chat_url)
            
            print(f"📍 Status: {response.status_code}")
            print(f"📍 URL final: {response.url}")
            
            if response.status_code == 200 and "aistudio.google.com" in response.url:
                print("✅ AI Studio acessível!")
                
                # Verificar se há erro de autenticação
                if "authentication" in response.text.lower() or "failed to list models" in response.text.lower():
                    print("❌ Erro de autenticação nos modelos")
                    return False
                else:
                    print("✅ Sistema funcionando corretamente!")
                    return True
            else:
                print("❌ AI Studio não acessível")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao testar acesso: {e}")
            return False
            
    def save_session(self):
        """Salva cookies da sessão"""
        try:
            cookies_file = Path("session_cookies.json")
            cookies_dict = {}
            
            for cookie in self.session.cookies:
                cookies_dict[cookie.name] = {
                    'value': cookie.value,
                    'domain': cookie.domain,
                    'path': cookie.path
                }
                
            with open(cookies_file, 'w') as f:
                json.dump(cookies_dict, f, indent=2)
                
            print(f"💾 Sessão salva em: {cookies_file}")
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar sessão: {e}")
            return False
            
    def load_session(self):
        """Carrega cookies da sessão"""
        try:
            cookies_file = Path("session_cookies.json")
            if not cookies_file.exists():
                return False
                
            with open(cookies_file, 'r') as f:
                cookies_dict = json.load(f)
                
            for name, cookie_data in cookies_dict.items():
                self.session.cookies.set(
                    name, 
                    cookie_data['value'],
                    domain=cookie_data['domain'],
                    path=cookie_data['path']
                )
                
            print(f"📂 Sessão carregada de: {cookies_file}")
            return True
        except Exception as e:
            print(f"❌ Erro ao carregar sessão: {e}")
            return False
            
    def run(self):
        """Executa o sistema completo"""
        print("🌟 AI STUDIO - LOGIN VIA HTTP")
        print("🎯 Conta: steveplayer120@gmail.com")
        print("⚡ Método sem interface gráfica")
        print("=" * 60)
        
        # Tentar carregar sessão existente
        if self.load_session():
            print("🔄 Testando sessão existente...")
            if self.test_ai_studio_access():
                print("✅ Sessão válida! Sistema pronto!")
                return True
            else:
                print("❌ Sessão inválida, fazendo novo login...")
        
        # Fazer login
        login_success = self.login_google()
        if not login_success:
            print("❌ Falha no login")
            return False
            
        # Testar acesso
        access_success = self.test_ai_studio_access()
        if not access_success:
            print("❌ Falha no acesso ao AI Studio")
            return False
            
        # Salvar sessão
        self.save_session()
        
        print("\n🎉 SISTEMA FUNCIONANDO!")
        print("✅ Login realizado")
        print("✅ AI Studio acessível")
        print("✅ Sessão salva")
        print("=" * 60)
        
        return True

def main():
    """Função principal"""
    sistema = AIStudioLoginHTTP()
    sucesso = sistema.run()
    
    if sucesso:
        print("🎉 Sistema executado com sucesso!")
        return 0
    else:
        print("❌ Sistema falhou")
        return 1

if __name__ == "__main__":
    exit(main())
