"""
Sistema Completo de Login com 2FA para Google AI Studio
- Detecta automaticamente quando precisa de 2FA
- Captura screenshot do código para visualização
- Permite inserir código manualmente
- Salva sessão persistente para evitar relogins
"""

import os
import time
import json
from playwright.sync_api import sync_playwright
from datetime import datetime

class AIStudioLogin2FA:
    def __init__(self, headless=False):
        """
        Inicializa sistema de login com 2FA
        
        Args:
            headless (bool): False para mostrar navegador (útil para debug)
        """
        self.headless = headless
        self.user_data_dir = "/workspaces/replit/browser_profile"
        self.session_file = "/workspaces/replit/session_data.json"
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        
    def ensure_directories(self):
        """Cria diretórios necessários"""
        os.makedirs(self.user_data_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
        
    def initialize_browser(self):
        """Inicializa navegador com perfil persistente"""
        try:
            self.ensure_directories()
            self.playwright = sync_playwright().start()
            
            # Configurações otimizadas para Docker/Alpine
            launch_options = {
                'headless': self.headless,
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
                    '--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                ]
            }
            
            # Usar contexto persistente para manter sessão
            self.context = self.playwright.chromium.launch_persistent_context(
                self.user_data_dir,
                **launch_options,
                viewport={'width': 1366, 'height': 768}
            )
            
            self.page = self.context.new_page()
            
            # Script para mascarar automação
            self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            """)
            
            self.page.set_default_timeout(30000)
            print("✅ Navegador inicializado com perfil persistente")
            
        except Exception as e:
            self.cleanup()
            raise Exception(f"Erro ao inicializar navegador: {e}")
    
    def save_session_info(self, status, details=None):
        """Salva informações da sessão"""
        try:
            session_data = {
                'timestamp': datetime.now().isoformat(),
                'status': status,
                'details': details or {},
                'url': self.page.url if self.page else None
            }
            
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
                
            print(f"💾 Sessão salva: {status}")
            
        except Exception as e:
            print(f"⚠️ Erro ao salvar sessão: {e}")
    
    def load_session_info(self):
        """Carrega informações da sessão anterior"""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"⚠️ Erro ao carregar sessão: {e}")
            return None
    
    def check_if_logged_in(self):
        """Verifica se já está logado no AI Studio"""
        try:
            print("🔍 Verificando status de login...")
            
            # Navegar para AI Studio
            self.page.goto("https://aistudio.google.com/", timeout=30000)
            self.page.wait_for_load_state('networkidle')
            time.sleep(3)
            
            current_url = self.page.url
            print(f"🔗 URL atual: {current_url}")
            
            # Capturar screenshot para análise
            self.page.screenshot(path="login_status_check.png", full_page=True)
            print("📸 Screenshot de status: login_status_check.png")
            
            # Indicadores de que está logado
            logged_in_selectors = [
                "text=Create new",
                "text=New chat",
                "text=Workspace",
                "text=API key",
                "[data-testid*='user']",
                ".user-avatar",
                "button[aria-label*='account']",
                "button[aria-label*='profile']"
            ]
            
            for selector in logged_in_selectors:
                try:
                    if self.page.is_visible(selector, timeout=2000):
                        print(f"✅ Indicador de login encontrado: {selector}")
                        self.save_session_info("logged_in", {"method": "existing_session"})
                        return True
                except:
                    continue
            
            # Verificar se está na página de login
            if "accounts.google.com" in current_url:
                print("⚠️ Redirecionado para login - não está logado")
                return False
            
            # Verificar por indicadores de login necessário
            login_needed_selectors = [
                "text=Get started",
                "text=Sign in", 
                "text=Login",
                "text=Continue"
            ]
            
            for selector in login_needed_selectors:
                try:
                    if self.page.is_visible(selector, timeout=2000):
                        print(f"⚠️ Indicador de login necessário: {selector}")
                        return False
                except:
                    continue
            
            # Se não encontrou indicadores claros, fazer análise mais profunda
            page_text = self.page.evaluate("() => document.body.textContent")
            
            if any(term in page_text.lower() for term in ["sign in", "get started", "login"]):
                print("⚠️ Texto indica que login é necessário")
                return False
            
            print("✅ Assumindo que está logado (nenhum indicador de login encontrado)")
            self.save_session_info("logged_in", {"method": "assumption"})
            return True
            
        except Exception as e:
            print(f"❌ Erro ao verificar login: {e}")
            self.page.screenshot(path="login_check_error.png")
            return False
    
    def start_login_process(self, email, password):
        """Inicia processo de login"""
        try:
            print("🔑 Iniciando processo de login...")
            
            # Se não estiver na página de login, ir para lá
            if "accounts.google.com" not in self.page.url:
                self.page.goto("https://accounts.google.com/signin")
                time.sleep(2)
            
            # Inserir email
            email_selectors = [
                "input[type='email']",
                "input[name='identifier']",
                "#identifierId"
            ]
            
            email_inserted = False
            for selector in email_selectors:
                try:
                    if self.page.is_visible(selector, timeout=3000):
                        print(f"📧 Inserindo email no campo: {selector}")
                        self.page.fill(selector, email)
                        time.sleep(1)
                        
                        # Clicar em "Próximo"
                        next_selectors = ["text=Next", "text=Próximo", "button[type='submit']"]
                        for next_sel in next_selectors:
                            try:
                                if self.page.is_visible(next_sel):
                                    self.page.click(next_sel)
                                    email_inserted = True
                                    break
                            except:
                                continue
                        
                        if email_inserted:
                            break
                except:
                    continue
            
            if not email_inserted:
                raise Exception("Não foi possível inserir email")
            
            time.sleep(3)
            
            # Inserir senha
            password_selectors = [
                "input[type='password']",
                "input[name='password']",
                "#password"
            ]
            
            password_inserted = False
            for selector in password_selectors:
                try:
                    if self.page.is_visible(selector, timeout=5000):
                        print(f"🔒 Inserindo senha no campo: {selector}")
                        self.page.fill(selector, password)
                        time.sleep(1)
                        
                        # Clicar em "Próximo" ou "Entrar"
                        submit_selectors = ["text=Next", "text=Próximo", "text=Sign in", "text=Entrar", "button[type='submit']"]
                        for submit_sel in submit_selectors:
                            try:
                                if self.page.is_visible(submit_sel):
                                    self.page.click(submit_sel)
                                    password_inserted = True
                                    break
                            except:
                                continue
                        
                        if password_inserted:
                            break
                except:
                    continue
            
            if not password_inserted:
                raise Exception("Não foi possível inserir senha")
            
            print("✅ Credenciais inseridas, aguardando resposta...")
            time.sleep(5)
            return True
            
        except Exception as e:
            print(f"❌ Erro no processo de login: {e}")
            self.page.screenshot(path="login_process_error.png")
            return False
    
    def detect_and_handle_2fa(self):
        """Detecta e gerencia 2FA automaticamente"""
        try:
            print("🔍 Verificando se 2FA é necessário...")
            
            # Aguardar um pouco para a página carregar
            time.sleep(3)
            
            current_url = self.page.url
            print(f"🔗 URL atual: {current_url}")
            
            # Capturar screenshot da situação atual
            self.page.screenshot(path="after_password.png", full_page=True)
            print("📸 Screenshot após senha: after_password.png")
            
            # Verificar se está na página de 2FA
            if "accounts.google.com" not in current_url:
                print("✅ Login concluído sem 2FA necessário")
                return True
            
            # Procurar por campos/textos de 2FA
            twofa_indicators = [
                "text=Enter the code",
                "text=verification code", 
                "text=2-step verification",
                "text=código de verificação",
                "text=verificação em 2 etapas",
                "input[type='tel']",
                "input[name='totpPin']",
                "input[autocomplete='one-time-code']",
                "input[inputmode='numeric']",
                "input[aria-label*='code']",
                "input[aria-label*='pin']"
            ]
            
            twofa_detected = False
            twofa_field = None
            
            for indicator in twofa_indicators:
                try:
                    if self.page.is_visible(indicator, timeout=2000):
                        print(f"🔍 Indicador de 2FA detectado: {indicator}")
                        twofa_detected = True
                        
                        # Se for um campo de input, salvar para uso posterior
                        if indicator.startswith("input"):
                            twofa_field = indicator
                        
                        break
                except:
                    continue
            
            if not twofa_detected:
                # Verificar por texto na página
                page_text = self.page.evaluate("() => document.body.textContent")
                twofa_keywords = ["verification", "code", "2-step", "verificação", "código"]
                
                if any(keyword in page_text.lower() for keyword in twofa_keywords):
                    print("🔍 Possível 2FA detectado via texto da página")
                    twofa_detected = True
            
            if twofa_detected:
                return self.handle_2fa_input(twofa_field)
            else:
                print("ℹ️ 2FA não detectado, verificando se login foi concluído...")
                
                # Aguardar um pouco mais e verificar novamente
                time.sleep(5)
                return self.check_if_logged_in()
                
        except Exception as e:
            print(f"❌ Erro na detecção de 2FA: {e}")
            self.page.screenshot(path="2fa_detection_error.png")
            return False
    
    def handle_2fa_input(self, field_selector=None):
        """Gerencia a entrada do código 2FA"""
        try:
            print("📱 2FA DETECTADO!")
            print("=" * 40)
            
            # Capturar screenshot do estado atual
            screenshot_path = f"2fa_screen_{int(time.time())}.png"
            self.page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Screenshot 2FA capturado: {screenshot_path}")
            
            # Tentar encontrar o campo de código se não foi fornecido
            if not field_selector:
                code_field_selectors = [
                    "input[type='tel']",
                    "input[name='totpPin']",
                    "input[autocomplete='one-time-code']",
                    "input[inputmode='numeric']",
                    "input[aria-label*='code']",
                    "input[aria-label*='pin']",
                    "input[maxlength='6']",
                    "input[maxlength='8']"
                ]
                
                for selector in code_field_selectors:
                    try:
                        if self.page.is_visible(selector, timeout=2000):
                            field_selector = selector
                            print(f"✅ Campo de código encontrado: {selector}")
                            break
                    except:
                        continue
            
            if not field_selector:
                print("⚠️ Campo de código não encontrado automaticamente")
                print("📱 Verifique o screenshot e insira o código manualmente no navegador")
                
                # Aguardar um tempo para permitir inserção manual
                print("⏳ Aguardando 120 segundos para inserção manual...")
                time.sleep(120)
                
                return self.check_if_logged_in()
            
            # Solicitar código ao usuário
            print("\n" + "="*50)
            print("📱 CÓDIGO 2FA NECESSÁRIO")
            print("="*50)
            print(f"📸 Verifique o screenshot: {screenshot_path}")
            print("📱 Abra seu app autenticador (Google Authenticator, etc.)")
            print("🔢 Encontre o código de 6 dígitos para Google/AI Studio")
            print("="*50)
            
            # Capturar screenshot focado no campo de código
            try:
                # Destacar o campo de código
                self.page.evaluate(f"""
                    () => {{
                        const field = document.querySelector('{field_selector}');
                        if (field) {{
                            field.style.border = '3px solid red';
                            field.style.backgroundColor = '#ffeeee';
                        }}
                    }}
                """)
                
                code_field_screenshot = f"2fa_code_field_{int(time.time())}.png"
                self.page.screenshot(path=code_field_screenshot)
                print(f"📸 Campo de código destacado: {code_field_screenshot}")
                
            except Exception as e:
                print(f"⚠️ Erro ao destacar campo: {e}")
            
            # Solicitar código
            while True:
                code = input("\n🔢 Digite o código 2FA (6 dígitos): ").strip()
                
                if len(code) == 6 and code.isdigit():
                    break
                else:
                    print("❌ Código deve ter exatamente 6 dígitos numéricos")
            
            # Inserir código
            print(f"⌨️ Inserindo código: {code}")
            self.page.fill(field_selector, code)
            time.sleep(1)
            
            # Procurar e clicar botão de envio
            submit_selectors = [
                "text=Next",
                "text=Próximo", 
                "text=Verify",
                "text=Verificar",
                "text=Continue",
                "text=Continuar",
                "button[type='submit']",
                "[data-testid*='submit']"
            ]
            
            submitted = False
            for selector in submit_selectors:
                try:
                    if self.page.is_visible(selector, timeout=2000):
                        print(f"📤 Enviando via: {selector}")
                        self.page.click(selector)
                        submitted = True
                        break
                except:
                    continue
            
            if not submitted:
                # Tentar Enter
                print("⌨️ Tentando enviar com Enter...")
                self.page.press(field_selector, "Enter")
            
            print("✅ Código 2FA enviado!")
            time.sleep(5)
            
            # Verificar resultado
            current_url = self.page.url
            print(f"🔗 URL após 2FA: {current_url}")
            
            if "accounts.google.com" not in current_url or self.check_if_logged_in():
                print("🎉 2FA CONCLUÍDO COM SUCESSO!")
                self.page.screenshot(path="2fa_success.png")
                self.save_session_info("logged_in", {"method": "2fa_completed"})
                return True
            else:
                print("❌ 2FA pode ter falhado")
                self.page.screenshot(path="2fa_failed.png")
                
                # Verificar se há mensagem de erro
                error_text = self.page.evaluate("() => document.body.textContent")
                if "incorrect" in error_text.lower() or "wrong" in error_text.lower():
                    print("🔄 Código incorreto, tente novamente...")
                    return self.handle_2fa_input(field_selector)
                
                return False
                
        except Exception as e:
            print(f"❌ Erro no manuseio do 2FA: {e}")
            self.page.screenshot(path="2fa_handle_error.png")
            return False
    
    def complete_login(self, email=None, password=None):
        """Executa login completo com 2FA automático"""
        try:
            print("🚀 INICIANDO LOGIN COMPLETO NO AI STUDIO")
            print("=" * 50)
            
            # Inicializar navegador
            self.initialize_browser()
            
            # Verificar se já está logado
            if self.check_if_logged_in():
                print("🎉 JÁ ESTÁ LOGADO!")
                return True
            
            # Obter credenciais
            if not email:
                email = os.getenv("GOOGLE_EMAIL") or input("📧 Digite seu email Google: ")
            if not password:
                password = os.getenv("GOOGLE_PASSWORD") or input("🔒 Digite sua senha: ")
            
            print(f"📧 Email: {email}")
            print("🔒 Senha: [fornecida]")
            
            # Executar login
            if not self.start_login_process(email, password):
                return False
            
            # Gerenciar 2FA se necessário
            if not self.detect_and_handle_2fa():
                return False
            
            # Verificação final
            if self.check_if_logged_in():
                print("\n🎉 LOGIN COMPLETO CONCLUÍDO COM SUCESSO!")
                print("💾 Sessão salva no perfil do navegador")
                print("⚡ Próximo login será mais rápido!")
                return True
            else:
                print("\n❌ Login não foi concluído completamente")
                return False
                
        except Exception as e:
            print(f"❌ Erro no login completo: {e}")
            self.page.screenshot(path="complete_login_error.png")
            return False
    
    def quick_login(self):
        """Login rápido usando sessão salva"""
        try:
            print("⚡ TENTATIVA DE LOGIN RÁPIDO")
            print("=" * 35)
            
            # Verificar sessão anterior
            session_info = self.load_session_info()
            if session_info:
                print(f"📅 Última sessão: {session_info.get('timestamp', 'Desconhecido')}")
                print(f"📊 Status: {session_info.get('status', 'Desconhecido')}")
            
            # Inicializar navegador com perfil persistente
            self.initialize_browser()
            
            # Verificar se está logado
            if self.check_if_logged_in():
                print("🎉 LOGIN RÁPIDO CONCLUÍDO!")
                print("💾 Usando sessão persistente do navegador")
                return True
            else:
                print("⚠️ Sessão expirou, login completo necessário")
                return False
                
        except Exception as e:
            print(f"❌ Erro no login rápido: {e}")
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

def main():
    """Função principal para teste"""
    print("🤖 Sistema de Login AI Studio com 2FA")
    print("=" * 45)
    
    login_system = AIStudioLogin2FA(headless=True)
    
    try:
        # Tentar login rápido primeiro
        if not login_system.quick_login():
            print("\n🔑 Login rápido falhou, executando login completo...")
            login_system.complete_login()
        
        # Manter sessão ativa por um tempo
        print("\n⏳ Mantendo sessão ativa por 60 segundos...")
        print("💡 Use este tempo para testar a integração!")
        time.sleep(60)
        
    except KeyboardInterrupt:
        print("\n⚠️ Interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    finally:
        login_system.cleanup()
        print("\n✅ Recursos liberados")

if __name__ == "__main__":
    main()
