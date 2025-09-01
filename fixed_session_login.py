"""
Sistema de sessão CORRIGIDO para Google AI Studio
Resolve problema de sessão não persistente
"""

import os
import time
import json
from automation import GoogleAIStudioAutomation
from playwright.sync_api import sync_playwright

class FixedSessionLogin:
    def __init__(self):
        self.user_data_dir = "/workspaces/replit/browser_profile_fixed"
        self.session_file = "/workspaces/replit/session_cookies.json"
        self.playwright = None
        self.context = None
        self.page = None
        
    def ensure_clean_profile(self):
        """Garante um perfil limpo"""
        if os.path.exists(self.user_data_dir):
            import shutil
            shutil.rmtree(self.user_data_dir)
            print("🧹 Perfil anterior removido")
        
        os.makedirs(self.user_data_dir, exist_ok=True)
        print(f"📁 Novo perfil criado: {self.user_data_dir}")
    
    def save_session_data(self):
        """Salva cookies e dados de sessão de forma mais robusta"""
        try:
            # Obter todos os cookies
            cookies = self.context.cookies()
            
            # Obter storage state completo
            storage_state = self.context.storage_state()
            
            # Informações da sessão
            session_data = {
                "timestamp": time.time(),
                "cookies": cookies,
                "storage_state": storage_state,
                "current_url": self.page.url,
                "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            
            # Salvar em arquivo JSON
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            print(f"✅ Sessão salva: {len(cookies)} cookies, URL: {self.page.url}")
            print(f"📄 Arquivo: {self.session_file}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar sessão: {e}")
            return False
    
    def load_session_data(self):
        """Carrega dados de sessão salvos"""
        try:
            if not os.path.exists(self.session_file):
                print("ℹ️ Nenhuma sessão salva encontrada")
                return False
            
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            
            # Verificar idade da sessão (12 horas)
            session_age = time.time() - session_data.get("timestamp", 0)
            if session_age > 12 * 60 * 60:
                print("⚠️ Sessão muito antiga (>12h)")
                return False
            
            # Aplicar storage state
            self.context.add_cookies(session_data["cookies"])
            
            print(f"✅ Sessão carregada - {len(session_data['cookies'])} cookies")
            print(f"📅 Idade: {session_age/3600:.1f} horas")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar sessão: {e}")
            return False
    
    def initialize_browser_with_session(self):
        """Inicializa navegador com configurações otimizadas para sessão"""
        try:
            self.playwright = sync_playwright().start()
            
            # Usar contexto persistente com configurações específicas
            context_options = {
                'headless': True,
                'executable_path': '/usr/bin/chromium-browser',
                'args': [
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-web-security',
                    '--disable-extensions',
                    '--no-first-run',
                    '--disable-default-apps',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-features=VizDisplayCompositor',
                    # Configurações para manter sessão
                    '--disable-background-timer-throttling',
                    '--disable-renderer-backgrounding',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-restore-session-state',
                    '--disable-background-networking'
                ],
                'viewport': {'width': 1366, 'height': 768},
                'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'extra_http_headers': {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none'
                }
            }
            
            # Usar contexto persistente
            self.context = self.playwright.chromium.launch_persistent_context(
                self.user_data_dir,
                **context_options
            )
            
            self.page = self.context.new_page()
            
            # Script para remover detecção de automação
            self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                // Sobrescrever outras propriedades
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                
                // Simular propriedades reais do navegador
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en'],
                });
            """)
            
            self.page.set_default_timeout(30000)
            print("✅ Navegador inicializado com sessão otimizada")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao inicializar: {e}")
            return False
    
    def test_if_really_logged_in(self):
        """Testa se realmente está logado verificando elementos específicos"""
        try:
            print("🧪 Testando status de login...")
            
            # Navegar para página principal
            self.page.goto("https://aistudio.google.com/", timeout=30000)
            time.sleep(5)
            
            # Capturar screenshot para análise
            self.page.screenshot(path="login_test.png")
            
            # Verificadores mais específicos
            logged_in_checks = [
                # Deve ter avatar/foto do usuário
                "img[alt*='avatar']",
                "img[alt*='profile']", 
                "[data-testid*='user']",
                "[data-testid*='profile']",
                # Deve ter menu de usuário
                "button[aria-label*='account']",
                "button[aria-label*='profile']",
                # Deve ter acesso a recursos
                "text=New chat",
                "text=Create new",
                "[href*='/app/']",
                # NÃO deve ter botões de login
                "text=Dashboard",
                "text=Studio",
                "text=API key"
            ]
            
            # Verificadores de NÃO logado
            not_logged_checks = [
                "text=Get started",
                "text=Sign in",
                "text=Login",
                "text=Sign up"
            ]
            
            # Contar indicadores positivos
            positive_count = 0
            negative_count = 0
            
            for check in logged_in_checks:
                try:
                    if self.page.is_visible(check, timeout=2000):
                        positive_count += 1
                        print(f"✅ Encontrado: {check}")
                except:
                    pass
            
            for check in not_logged_checks:
                try:
                    if self.page.is_visible(check, timeout=2000):
                        negative_count += 1
                        print(f"❌ Encontrado (ruim): {check}")
                except:
                    pass
            
            # Verificar URL atual
            current_url = self.page.url
            print(f"🔗 URL atual: {current_url}")
            
            # Decisão baseada em múltiplos fatores
            is_logged_in = (
                positive_count > 0 and 
                negative_count == 0 and 
                "accounts.google.com" not in current_url
            )
            
            print(f"📊 Score: +{positive_count} -{negative_count}")
            print(f"🎯 Status: {'LOGADO' if is_logged_in else 'NÃO LOGADO'}")
            
            return is_logged_in
            
        except Exception as e:
            print(f"❌ Erro no teste: {e}")
            return False
    
    def complete_fresh_login(self):
        """Faz login completo do zero"""
        try:
            print("🔑 FAZENDO LOGIN COMPLETO...")
            
            # Obter credenciais
            email = os.getenv("SEU_EMAIL", "")
            password = os.getenv("SUA_SENHA", "")
            
            if not email:
                email = input("📧 Email: ")
            else:
                print(f"📧 Email: {email}")
                
            if not password:
                password = input("🔒 Senha: ")
            else:
                print("🔒 Senha: [configurada]")
            
            # Usar automation para login
            automation = GoogleAIStudioAutomation(headless=True, timeout_2fa=120)
            automation.playwright = self.playwright
            automation.context = self.context
            automation.page = self.page
            automation.browser = None
            
            # Processo de login
            automation.navigate_to_ai_studio()
            automation.start_login()
            automation.enter_email(email)
            automation.enter_password(password)
            automation.wait_for_2fa()
            
            # Aguardar conclusão
            time.sleep(10)
            
            # Verificar se deu certo
            if self.test_if_really_logged_in():
                print("✅ Login bem-sucedido!")
                
                # Salvar sessão
                if self.save_session_data():
                    print("💾 Sessão salva com sucesso!")
                    return True
                else:
                    print("⚠️ Login OK mas falha ao salvar sessão")
                    return True
            else:
                print("❌ Login falhou")
                return False
                
        except Exception as e:
            print(f"❌ Erro no login: {e}")
            return False
    
    def smart_login(self):
        """Login inteligente - tenta sessão salva primeiro"""
        try:
            print("🧠 LOGIN INTELIGENTE")
            print("=" * 30)
            
            # Inicializar navegador
            if not self.initialize_browser_with_session():
                return False
            
            # Tentar carregar sessão existente
            session_loaded = self.load_session_data()
            
            if session_loaded:
                print("🔍 Testando sessão carregada...")
                if self.test_if_really_logged_in():
                    print("🎉 SESSÃO VÁLIDA! Já está logado!")
                    return True
                else:
                    print("❌ Sessão inválida, fazendo login fresh")
            else:
                print("ℹ️ Nenhuma sessão válida, fazendo login fresh")
            
            # Fazer login completo
            return self.complete_fresh_login()
            
        except Exception as e:
            print(f"❌ Erro no login inteligente: {e}")
            return False
    
    def cleanup(self):
        """Limpa recursos"""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.playwright:
                self.playwright.stop()
        except:
            pass

def test_fixed_session():
    """Testa o sistema corrigido de sessão"""
    print("🔧 TESTE DO SISTEMA DE SESSÃO CORRIGIDO")
    print("=" * 45)
    
    login_system = FixedSessionLogin()
    
    try:
        success = login_system.smart_login()
        
        if success:
            print("\n🎉 SUCESSO TOTAL!")
            print("✅ Login funcionando")
            print("💾 Sessão sendo salva corretamente")
            print("📸 Screenshots disponíveis para verificação")
            
            # Manter ativo por um tempo
            input("\nPressione Enter para finalizar...")
        else:
            print("\n❌ Falha no login")
            
    except KeyboardInterrupt:
        print("\n⚠️ Cancelado pelo usuário")
    finally:
        login_system.cleanup()

if __name__ == "__main__":
    test_fixed_session()
