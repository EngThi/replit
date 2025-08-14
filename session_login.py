"""
Sistema de salvamento e carregamento de sessão para evitar logins repetidos
"""

import json
import os
import time
from automation import GoogleAIStudioAutomation

class SessionManager:
    def __init__(self, session_file="google_session.json"):
        self.session_file = session_file
        
    def save_session(self, automation):
        """
        Salva cookies e dados de sessão
        """
        try:
            if not automation.page:
                print("❌ Nenhuma página ativa para salvar sessão")
                return False
                
            # Obter cookies
            cookies = automation.context.cookies()
            
            # Obter storage state (inclui localStorage, sessionStorage, etc)
            storage_state = automation.context.storage_state()
            
            # Salvar dados
            session_data = {
                "cookies": cookies,
                "storage_state": storage_state,
                "timestamp": time.time(),
                "url": automation.page.url
            }
            
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
                
            print(f"✅ Sessão salva em: {self.session_file}")
            print(f"📅 Timestamp: {time.ctime()}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar sessão: {e}")
            return False
    
    def load_session(self, automation):
        """
        Carrega cookies e dados de sessão salvos
        """
        try:
            if not os.path.exists(self.session_file):
                print(f"ℹ️ Arquivo de sessão não encontrado: {self.session_file}")
                return False
                
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            
            # Verificar se a sessão não é muito antiga (24 horas)
            session_age = time.time() - session_data.get("timestamp", 0)
            if session_age > 24 * 60 * 60:  # 24 horas
                print("⚠️ Sessão muito antiga (>24h). Faça novo login.")
                return False
            
            # Aplicar storage state (inclui cookies, localStorage, etc)
            automation.context.clear_cookies()
            automation.context.add_cookies(session_data["cookies"])
            
            print(f"✅ Sessão carregada!")
            print(f"📅 Salva em: {time.ctime(session_data['timestamp'])}")
            print(f"🔗 URL original: {session_data.get('url', 'N/A')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar sessão: {e}")
            return False
    
    def is_session_valid(self):
        """
        Verifica se existe uma sessão válida
        """
        if not os.path.exists(self.session_file):
            return False
            
        try:
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            
            session_age = time.time() - session_data.get("timestamp", 0)
            return session_age <= 24 * 60 * 60  # Válida por 24 horas
            
        except:
            return False

def automated_login_with_session():
    """
    Login automatizado que reutiliza sessão quando possível
    """
    print("🚀 Login Automatizado com Salvamento de Sessão")
    print("=" * 55)
    
    session_manager = SessionManager()
    
    # Verificar credenciais
    email = os.getenv("SEU_EMAIL", "")
    password = os.getenv("SUA_SENHA", "")
    
    if not email:
        email = input("📧 Digite seu email: ")
    else:
        print(f"📧 Email: {email}")
        
    if not password:
        password = input("🔒 Digite sua senha: ")
    else:
        print("🔒 Senha: [configurada]")
    
    automation = GoogleAIStudioAutomation(headless=True, timeout_2fa=120)
    
    try:
        print("\n1. ✅ Inicializando navegador...")
        automation.initialize_browser()
        
        # Tentar carregar sessão existente
        if session_manager.is_session_valid():
            print("🔄 Tentando usar sessão salva...")
            if session_manager.load_session(automation):
                
                # Testar se a sessão ainda funciona
                print("🧪 Testando sessão...")
                automation.page.goto("https://aistudio.google.com/", timeout=30000)
                
                # Verificar se está logado (procurar indicadores de login)
                time.sleep(3)
                
                # Verificar se precisa fazer login
                login_indicators = [
                    "text=Get started",
                    "text=Sign in",
                    "text=Login"
                ]
                
                needs_login = False
                for indicator in login_indicators:
                    try:
                        if automation.page.is_visible(indicator, timeout=2000):
                            needs_login = True
                            break
                    except:
                        continue
                
                if not needs_login:
                    print("🎉 SESSÃO VÁLIDA! Você já está logado!")
                    automation.take_screenshot("session_loaded.png")
                    
                    # Salvar sessão atualizada
                    session_manager.save_session(automation)
                    
                    return automation
                else:
                    print("⚠️ Sessão expirada. Fazendo novo login...")
        
        # Fazer login normal
        print("🔑 Iniciando processo de login...")
        
        print("2. ✅ Navegando para Google AI Studio...")
        automation.navigate_to_ai_studio()
        
        print("3. ✅ Clicando em Get started...")
        automation.start_login()
        
        print("4. ✅ Inserindo email...")
        automation.enter_email(email)
        
        print("5. ✅ Inserindo senha...")
        automation.enter_password(password)
        
        print("6. 📱 Verificando 2FA...")
        handle_2fa_interactive(automation)
        
        # Aguardar conclusão do login
        print("7. ⏳ Aguardando conclusão do login...")
        time.sleep(5)
        
        # Salvar sessão após login bem-sucedido
        print("8. 💾 Salvando sessão para próximas vezes...")
        session_manager.save_session(automation)
        
        print("✅ LOGIN CONCLUÍDO E SESSÃO SALVA!")
        automation.take_screenshot("login_complete.png")
        
        return automation
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        try:
            automation.take_screenshot("error.png")
        except:
            pass
        return None

def handle_2fa_interactive(automation):
    """
    Lida com 2FA de forma interativa
    """
    time.sleep(3)
    
    # Verificar se há campo de código
    code_selectors = [
        "input[type='tel']",
        "input[name='totpPin']", 
        "input[id*='code']",
        "input[id*='pin']",
        "input[autocomplete='one-time-code']"
    ]
    
    code_field = None
    for selector in code_selectors:
        try:
            if automation.page.is_visible(selector):
                code_field = selector
                break
        except:
            continue
    
    if code_field:
        automation.take_screenshot("2fa_screen.png")
        print("\n📱 2FA DETECTADO!")
        print("🔍 Verifique seu celular e escolha o número correto")
        print("📸 Screenshot salvo em: 2fa_screen.png")
        
        while True:
            try:
                code = input("\n🔢 Digite o código 2FA: ")
                
                if len(code) >= 6 and code.isdigit():
                    automation.page.fill(code_field, code)
                    time.sleep(1)
                    
                    # Submeter
                    submit_selectors = ["text=Next", "text=Verify", "button[type='submit']"]
                    for selector in submit_selectors:
                        try:
                            if automation.page.is_visible(selector):
                                automation.page.click(selector)
                                break
                        except:
                            continue
                    
                    time.sleep(5)
                    
                    # Verificar se saiu da página de 2FA
                    if not automation.page.is_visible(code_field):
                        print("✅ 2FA concluído!")
                        break
                    else:
                        print("❌ Código incorreto. Tente novamente.")
                        automation.take_screenshot("2fa_screen.png")
                        
            except KeyboardInterrupt:
                break

def quick_access():
    """
    Acesso rápido usando sessão salva
    """
    print("⚡ Acesso Rápido ao Google AI Studio")
    print("=" * 40)
    
    session_manager = SessionManager()
    
    if not session_manager.is_session_valid():
        print("❌ Nenhuma sessão válida encontrada.")
        print("💡 Execute 'python session_login.py' primeiro para fazer login")
        return
    
    automation = GoogleAIStudioAutomation(headless=True)
    
    try:
        automation.initialize_browser()
        
        if session_manager.load_session(automation):
            automation.page.goto("https://aistudio.google.com/")
            time.sleep(3)
            automation.take_screenshot("quick_access.png")
            print("🎉 Acesso rápido concluído!")
            print("📸 Screenshot: quick_access.png")
            
            return automation
        else:
            print("❌ Falha ao carregar sessão")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        
    return None

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        automation = quick_access()
    else:
        automation = automated_login_with_session()
    
    if automation:
        input("\nPressione Enter para fechar...")
        automation.close_browser()
