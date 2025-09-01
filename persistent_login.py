"""
Sistema de login persistente usando perfil de navegador
"""

import os
import time
from automation import GoogleAIStudioAutomation
from playwright.sync_api import sync_playwright

class PersistentGoogleLogin:
    def __init__(self):
        self.user_data_dir = "/workspaces/replit/browser_profile"
        self.automation = None
        
    def ensure_profile_dir(self):
        """Cria diretório do perfil se não existir"""
        if not os.path.exists(self.user_data_dir):
            os.makedirs(self.user_data_dir, exist_ok=True)
            print(f"📁 Criado diretório do perfil: {self.user_data_dir}")
        else:
            print(f"📁 Usando perfil existente: {self.user_data_dir}")
    
    def initialize_with_profile(self):
        """Inicializa navegador com perfil persistente"""
        try:
            self.ensure_profile_dir()
            
            self.playwright = sync_playwright().start()
            
            # Usar launch_persistent_context para perfil persistente
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
                    '--disable-blink-features=AutomationControlled'
                ],
                'viewport': {'width': 1366, 'height': 768},
                'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            # Usar contexto persistente
            self.context = self.playwright.chromium.launch_persistent_context(
                self.user_data_dir,
                **context_options
            )
            self.page = self.context.new_page()
            self.browser = None  # Não há browser separado com contexto persistente
            
            # Remover indicadores de automação
            self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            """)
            
            self.page.set_default_timeout(30000)
            print("✅ Navegador com perfil persistente inicializado!")
            
        except Exception as e:
            self.cleanup()
            raise Exception(f"Erro ao inicializar navegador: {e}")
    
    def check_if_logged_in(self):
        """Verifica se já está logado"""
        try:
            print("🔍 Verificando se já está logado...")
            self.page.goto("https://aistudio.google.com/", timeout=30000)
            time.sleep(5)
            
            # Indicadores de que está logado
            logged_in_indicators = [
                "text=Create new",
                "text=New chat", 
                "[data-testid*='user']",
                ".user-avatar",
                "text=Workspace",
                "text=API key",
                "profile-button",
                "account-button"
            ]
            
            # Indicadores de que NÃO está logado
            login_needed_indicators = [
                "text=Get started",
                "text=Sign in",
                "text=Login"
            ]
            
            # Verificar se está logado
            for indicator in logged_in_indicators:
                try:
                    if self.page.is_visible(indicator, timeout=3000):
                        print(f"✅ Indicador de login encontrado: {indicator}")
                        self.page.screenshot(path="already_logged_in.png")
                        return True
                except:
                    continue
            
            # Verificar se precisa fazer login
            for indicator in login_needed_indicators:
                try:
                    if self.page.is_visible(indicator, timeout=3000):
                        print(f"⚠️ Indicador de login necessário: {indicator}")
                        return False
                except:
                    continue
            
            # Se não encontrou nenhum indicador claro, usar URL como backup
            current_url = self.page.url
            if "accounts.google.com" in current_url:
                print("⚠️ Redirecionado para login - não está logado")
                return False
            
            # Se chegou até aqui, assumir que está logado
            print("✅ Assumindo que está logado (nenhum indicador de login encontrado)")
            self.page.screenshot(path="status_check.png")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao verificar status de login: {e}")
            return False
    
    def full_login_flow(self):
        """Executa o fluxo completo de login"""
        try:
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
            
            # Usar automation normal para login
            automation = GoogleAIStudioAutomation(headless=True, timeout_2fa=120)
            automation.context = self.context 
            automation.page = self.page
            automation.playwright = self.playwright
            automation.browser = None  # Não há browser separado
            
            print("🔑 Iniciando processo de login...")
            
            automation.navigate_to_ai_studio()
            automation.start_login()
            automation.enter_email(email)
            automation.enter_password(password)
            automation.wait_for_2fa()
            
            print("⏳ Aguardando conclusão do login...")
            time.sleep(5)
            
            # Verificar se login foi bem-sucedido
            if self.check_if_logged_in():
                print("🎉 LOGIN CONCLUÍDO E PERFIL SALVO!")
                self.page.screenshot(path="login_success_with_profile.png")
                return True
            else:
                print("❌ Login pode não ter sido concluído")
                return False
                
        except Exception as e:
            print(f"❌ Erro no login: {e}")
            self.page.screenshot(path="login_error.png")
            return False
    
    def quick_access(self):
        """Acesso rápido usando perfil salvo"""
        try:
            self.initialize_with_profile()
            
            if self.check_if_logged_in():
                print("🎉 ACESSO RÁPIDO CONCLUÍDO!")
                print("💾 Sessão mantida pelo perfil do navegador")
                return True
            else:
                print("⚠️ Perfil não contém sessão válida - fazendo login completo...")
                return self.full_login_flow()
                
        except Exception as e:
            print(f"❌ Erro no acesso rápido: {e}")
            return False
    
    def login_with_persistence(self):
        """Login com persistência automática"""
        try:
            self.initialize_with_profile()
            
            # Verificar se já está logado
            if self.check_if_logged_in():
                print("🎉 JÁ ESTÁ LOGADO!")
                print("💾 Usando sessão salva do perfil")
                return True
            else:
                print("🔑 Não está logado - iniciando processo de login...")
                return self.full_login_flow()
                
        except Exception as e:
            print(f"❌ Erro geral: {e}")
            return False
    
    def cleanup(self):
        """Limpa recursos"""
        try:
            if hasattr(self, 'page') and self.page:
                self.page.close()
            if hasattr(self, 'context') and self.context:
                self.context.close()
            if hasattr(self, 'playwright') and self.playwright:
                self.playwright.stop()
        except:
            pass

def main():
    """Função principal"""
    print("🚀 Login Persistente do Google AI Studio")
    print("=" * 45)
    
    login_manager = PersistentGoogleLogin()
    
    try:
        success = login_manager.login_with_persistence()
        
        if success:
            print("\n✅ SUCESSO!")
            print("📱 O Google AI Studio está acessível")
            print("💾 Suas credenciais foram salvas no perfil do navegador")
            print("⚡ Na próxima vez, o acesso será mais rápido")
            
            # Manter navegador aberto por um tempo para demonstração
            print("\n⏳ Mantendo sessão ativa por 30 segundos...")
            time.sleep(30)
        else:
            print("\n❌ FALHA!")
            print("💡 Tente novamente ou verifique suas credenciais")
        
    except KeyboardInterrupt:
        print("\n⚠️ Interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    finally:
        login_manager.cleanup()

def quick_access():
    """Acesso rápido usando perfil salvo"""
    print("⚡ Acesso Rápido ao Google AI Studio")
    print("=" * 40)
    
    login_manager = PersistentGoogleLogin()
    
    try:
        success = login_manager.quick_access()
        
        if success:
            print("\n🎉 ACESSO CONCLUÍDO!")
            print("📱 Google AI Studio está pronto para uso")
        else:
            print("\n❌ Falha no acesso rápido")
            
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    finally:
        login_manager.cleanup()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        quick_access()
    else:
        main()
