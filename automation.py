try:
    from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    # Definir tipos dummy para compatibilidade
    Browser = None
    Page = None
    BrowserContext = None

import time
import os
from typing import Optional

class GoogleAIStudioAutomation:
    """
    Classe para automação de login no Google AI Studio usando Playwright
    """
    
    def __init__(self, headless: bool = True, timeout_2fa: int = 40):
        """
        Inicializa a automação
        
        Args:
            headless (bool): Se True, executa o navegador em modo headless
            timeout_2fa (int): Timeout em segundos para aguardar autenticação 2FA
        """
        self.headless = headless
        self.timeout_2fa = timeout_2fa * 1000  # Converter para milissegundos
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
    
    def initialize_browser(self):
        """
        Inicializa o navegador Playwright
        """
        if not PLAYWRIGHT_AVAILABLE:
            raise Exception("❌ Playwright não está instalado. "
                          "Este módulo é necessário para a automação. "
                          "Para usar esta funcionalidade, instale o Playwright: "
                          "'pip install playwright' e 'playwright install'")
        
        try:
            self.playwright = sync_playwright().start()
            
            # Configurações do navegador otimizadas para Alpine Linux
            browser_options = {
                'headless': True,  # Força headless no ambiente containerizado
                'executable_path': '/usr/bin/chromium-browser',  # Usar Chromium do sistema
                'args': [
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-web-security',
                    '--disable-extensions',
                    '--no-first-run',
                    '--disable-default-apps',
                    # Args para evitar detecção de automação
                    '--disable-blink-features=AutomationControlled',
                    '--disable-features=VizDisplayCompositor',
                    '--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    '--disable-plugins-discovery',
                    '--disable-preconnect',
                    '--disable-sync',
                    '--no-default-browser-check',
                    '--no-first-run',
                    '--disable-default-apps',
                    '--disable-translate',
                    '--disable-background-timer-throttling',
                    '--disable-renderer-backgrounding',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-ipc-flooding-protection'
                ]
            }
            
            self.browser = self.playwright.chromium.launch(**browser_options)
            self.context = self.browser.new_context(
                viewport={'width': 1366, 'height': 768},
                user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                extra_http_headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                }
            )
            self.page = self.context.new_page()
            
            # Remover propriedades que indicam automação
            self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                // Remover outras propriedades de detecção
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            """)
            
            # Configurar timeouts
            self.page.set_default_timeout(30000)  # 30 segundos
            
            print("✅ Navegador inicializado com sucesso!")
            
        except Exception as e:
            # Limpar recursos em caso de erro
            try:
                if hasattr(self, 'browser') and self.browser:
                    self.browser.close()
                if hasattr(self, 'playwright') and self.playwright:
                    self.playwright.stop()
            except:
                pass
                
            error_msg = str(e)
            if "Host system is missing dependencies" in error_msg:
                raise Exception("❌ Dependências do sistema faltando para executar navegadores. "
                              "Este erro é comum no ambiente Replit. "
                              "Para usar esta funcionalidade completamente, execute em um ambiente local "
                              "com todas as dependências instaladas.")
            else:
                raise Exception(f"Erro ao inicializar navegador: {error_msg}")
    
    def navigate_to_ai_studio(self):
        """
        Navega para o Google AI Studio
        """
        try:
            self.page.goto("https://aistudio.google.com/", wait_until='networkidle')
            self.page.wait_for_load_state('domcontentloaded')
            
        except Exception as e:
            raise Exception(f"Erro ao navegar para Google AI Studio: {str(e)}")
    
    def start_login(self):
        """
        Inicia o processo de login clicando no botão Sign in ou Get started
        """
        try:
            # Aguardar a página carregar completamente
            self.page.wait_for_load_state('networkidle')
            
            # Lista de seletores para botões de login/cadastro
            login_selectors = [
                "text=Get started",  # Botão principal "Get started" 
                "text=Sign in",      # Botão "Sign in" se estiver logado
                "text=Fazer login",
                "text=Entrar",
                "text=Começar",
                "[data-value='sign_in']",
                "button:has-text('Get started')",
                "button:has-text('Sign in')",
                "a:has-text('Get started')",
                "a:has-text('Sign in')",
                "button[aria-label*='sign']",
                "button[aria-label*='login']",
                "button[aria-label*='started']",
                ".mdc-button:has-text('Get started')",
                ".mdc-button:has-text('Sign in')"
            ]
            
            clicked = False
            for selector in login_selectors:
                try:
                    # Aguardar o elemento aparecer
                    self.page.wait_for_selector(selector, timeout=5000)
                    
                    # Verificar se o elemento está visível
                    if self.page.is_visible(selector):
                        self.page.click(selector)
                        clicked = True
                        print(f"✅ Clicou no botão: {selector}")
                        break
                except Exception as e:
                    print(f"⚠️ Seletor {selector} não encontrado: {str(e)}")
                    continue
            
            if not clicked:
                # Tentar uma abordagem mais geral
                try:
                    # Procurar por qualquer botão ou link que contenha palavras relacionadas a login
                    self.page.wait_for_timeout(2000)
                    
                    # JavaScript para encontrar botões de login
                    login_button = self.page.evaluate("""
                        () => {
                            const buttons = Array.from(document.querySelectorAll('button, a, [role="button"]'));
                            const loginTexts = ['get started', 'sign in', 'login', 'entrar', 'começar'];
                            
                            for (const button of buttons) {
                                const text = button.textContent.toLowerCase().trim();
                                if (loginTexts.some(term => text.includes(term))) {
                                    return button.outerHTML;
                                }
                            }
                            return null;
                        }
                    """)
                    
                    if login_button:
                        print(f"🔍 Encontrado botão via JavaScript: {login_button[:100]}...")
                        # Tentar clicar usando JavaScript
                        self.page.evaluate("""
                            () => {
                                const buttons = Array.from(document.querySelectorAll('button, a, [role="button"]'));
                                const loginTexts = ['get started', 'sign in', 'login', 'entrar', 'começar'];
                                
                                for (const button of buttons) {
                                    const text = button.textContent.toLowerCase().trim();
                                    if (loginTexts.some(term => text.includes(term))) {
                                        button.click();
                                        return true;
                                    }
                                }
                                return false;
                            }
                        """)
                        clicked = True
                    
                except Exception as e:
                    print(f"⚠️ Erro na busca JavaScript: {str(e)}")
            
            if not clicked:
                # Capturar screenshot para debug
                screenshot_path = "debug_login_page.png"
                self.page.screenshot(path=screenshot_path)
                raise Exception(f"Nenhum botão de login encontrado. Screenshot salvo em: {screenshot_path}")
            
            # Aguardar redirecionamento ou mudança na página
            try:
                # Aguardar redirecionamento para página de login do Google OU mudança na URL
                self.page.wait_for_function(
                    "() => window.location.href.includes('accounts.google.com') || document.querySelector('input[type=\"email\"]')",
                    timeout=15000
                )
            except:
                # Se não redirecionar, pode ser que já tenha carregado o formulário de login
                print("⚠️ Não houve redirecionamento detectado, continuando...")
            
        except Exception as e:
            # Capturar screenshot em caso de erro
            try:
                self.page.screenshot(path="erro_start_login.png")
            except:
                pass
            raise Exception(f"Erro ao iniciar login: {str(e)}")
    
    def enter_email(self, email: str):
        """
        Insere o email no formulário de login de forma mais humana
        
        Args:
            email (str): Email para login
        """
        try:
            # Aguardar campo de email com tempo extra
            self.page.wait_for_load_state('networkidle', timeout=10000)
            
            email_selectors = [
                "input[type='email']",
                "input[name='identifier']", 
                "#identifierId",
                "input[autocomplete='username']",
                "input[id*='email']",
                "input[name*='email']"
            ]
            
            email_field = None
            for selector in email_selectors:
                try:
                    self.page.wait_for_selector(selector, timeout=5000)
                    if self.page.is_visible(selector):
                        email_field = selector
                        break
                except:
                    continue
            
            if not email_field:
                raise Exception("Campo de email não encontrado")
            
            # Simular comportamento humano
            self.page.click(email_field)
            self.page.wait_for_timeout(500)  # Pequena pausa
            
            # Limpar campo
            self.page.fill(email_field, "")
            self.page.wait_for_timeout(200)
            
            # Digitar email character por character para parecer mais humano
            for char in email:
                self.page.type(email_field, char, delay=50)  # 50ms entre caracteres
            
            self.page.wait_for_timeout(1000)  # Pausa antes de clicar Next
            
            # Clicar em "Próximo"
            next_selectors = [
                "text=Next",
                "text=Próximo", 
                "#identifierNext",
                "button[type='submit']",
                "button:has-text('Next')",
                "input[type='submit']"
            ]
            
            for selector in next_selectors:
                try:
                    if self.page.is_visible(selector):
                        self.page.click(selector)
                        break
                except:
                    continue
            
            # Aguardar carregamento da próxima página
            self.page.wait_for_timeout(3000)
            
        except Exception as e:
            raise Exception(f"Erro ao inserir email: {str(e)}")
    
    def enter_password(self, password: str):
        """
        Insere a senha no formulário de login de forma mais humana
        
        Args:
            password (str): Senha para login
        """
        try:
            # Aguardar página de senha carregar completamente
            self.page.wait_for_load_state('networkidle', timeout=15000)
            
            password_selectors = [
                "input[type='password']",
                "input[name='password']", 
                "#password",
                "input[autocomplete='current-password']",
                "input[id*='password']",
                "input[name*='passwd']"
            ]
            
            password_field = None
            for selector in password_selectors:
                try:
                    self.page.wait_for_selector(selector, timeout=10000)
                    if self.page.is_visible(selector):
                        password_field = selector
                        break
                except:
                    continue
            
            if not password_field:
                raise Exception("Campo de senha não encontrado")
            
            # Simular comportamento humano
            self.page.click(password_field)
            self.page.wait_for_timeout(800)  # Pausa mais longa
            
            # Limpar campo
            self.page.fill(password_field, "")
            self.page.wait_for_timeout(300)
            
            # Digitar senha character por character
            for char in password:
                self.page.type(password_field, char, delay=80)  # 80ms entre caracteres
            
            self.page.wait_for_timeout(1500)  # Pausa antes de submeter
            
            # Clicar em "Próximo"
            next_selectors = [
                "text=Next",
                "text=Próximo",
                "#passwordNext", 
                "button[type='submit']",
                "button:has-text('Next')",
                "input[type='submit']",
                "button[id*='next']"
            ]
            
            for selector in next_selectors:
                try:
                    if self.page.is_visible(selector):
                        self.page.click(selector)
                        break
                except:
                    continue
            
            # Aguardar processamento
            self.page.wait_for_timeout(2000)
            
        except Exception as e:
            raise Exception(f"Erro ao inserir senha: {str(e)}")
    
    def wait_for_2fa(self):
        """
        Aguarda e trata a autenticação de dois fatores
        """
        try:
            print("🔍 Verificando se há 2FA...")
            
            # Aguardar um pouco para a página carregar
            self.page.wait_for_timeout(3000)
            
            # Verificar se estamos na página de 2FA
            two_fa_indicators = [
                "text=2-Step Verification",
                "text=Verificação em duas etapas", 
                "text=Enter code",
                "text=Digite o código",
                "input[type='tel']",
                "input[name='totpPin']",
                "input[id*='code']",
                "input[id*='pin']",
                "[data-testid*='code']"
            ]
            
            is_2fa_page = False
            for indicator in two_fa_indicators:
                try:
                    if self.page.is_visible(indicator, timeout=2000):
                        is_2fa_page = True
                        print(f"✅ Detectada página de 2FA: {indicator}")
                        break
                except:
                    continue
            
            if is_2fa_page:
                print("📱 2FA detectado!")
                
                # Capturar screenshot da página de 2FA
                screenshot_path = "2fa_page.png"
                self.page.screenshot(path=screenshot_path)
                print(f"📸 Screenshot da página 2FA salvo em: {screenshot_path}")
                
                # Extrair texto da página para mostrar ao usuário
                page_text = self.page.evaluate("""
                    () => {
                        const elements = document.querySelectorAll('div, span, p');
                        const texts = [];
                        elements.forEach(el => {
                            const text = el.textContent.trim();
                            if (text && text.length > 5 && text.length < 200) {
                                texts.push(text);
                            }
                        });
                        return [...new Set(texts)].slice(0, 10);
                    }
                """)
                
                print("📋 Texto da página de 2FA:")
                for text in page_text:
                    if any(word in text.lower() for word in ['code', 'código', 'verify', 'verificar']):
                        print(f"  → {text}")
                
                # Procurar campo de código
                code_selectors = [
                    "input[type='tel']",
                    "input[name='totpPin']", 
                    "input[id*='code']",
                    "input[id*='pin']",
                    "input[autocomplete='one-time-code']",
                    "input[inputmode='numeric']"
                ]
                
                code_field = None
                for selector in code_selectors:
                    try:
                        if self.page.is_visible(selector):
                            code_field = selector
                            print(f"✅ Campo de código encontrado: {selector}")
                            break
                    except:
                        continue
                
                if code_field:
                    print("⏳ Aguardando você inserir o código 2FA...")
                    print("💡 Opções:")
                    print("   1. Verifique seu celular para o código")
                    print("   2. Olhe o screenshot: 2fa_page.png") 
                    print("   3. O código será inserido automaticamente quando recebido")
                    
                    # Aguardar o código ser inserido (manualmente ou por outro meio)
                    start_time = time.time()
                    timeout_seconds = self.timeout_2fa / 1000
                    
                    while time.time() - start_time < timeout_seconds:
                        try:
                            # Verificar se o campo foi preenchido
                            current_value = self.page.input_value(code_field)
                            if current_value and len(current_value) >= 6:
                                print(f"✅ Código detectado: {current_value}")
                                
                                # Procurar botão de submissão
                                submit_selectors = [
                                    "text=Next",
                                    "text=Próximo",
                                    "text=Verify", 
                                    "text=Verificar",
                                    "button[type='submit']",
                                    "input[type='submit']"
                                ]
                                
                                for selector in submit_selectors:
                                    try:
                                        if self.page.is_visible(selector):
                                            self.page.click(selector)
                                            print("✅ Código submetido!")
                                            break
                                    except:
                                        continue
                                
                                # Aguardar processamento
                                self.page.wait_for_timeout(3000)
                                break
                                
                        except:
                            pass
                            
                        # Verificar se saiu da página de 2FA
                        current_url = self.page.url
                        if "accounts.google.com" not in current_url:
                            print("✅ 2FA concluído - redirecionado!")
                            break
                            
                        self.page.wait_for_timeout(1000)  # Verificar a cada segundo
                    
                    else:
                        print("⚠️ Timeout do 2FA - continuando...")
                
            else:
                print("ℹ️ Nenhum 2FA detectado - continuando...")
                
        except Exception as e:
            print(f"⚠️ Erro durante 2FA: {str(e)}")
            # Continuar mesmo com erro
            pass
    
    def close_browser(self):
        """
        Fecha o navegador e limpa recursos
        """
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
                
        except Exception as e:
            # Não propagar erros de fechamento
            pass
    
    def take_screenshot(self, path: str = "screenshot.png"):
        """
        Captura screenshot da página atual
        
        Args:
            path (str): Caminho para salvar o screenshot
        """
        try:
            if self.page:
                self.page.screenshot(path=path, full_page=True)
                return path
        except Exception:
            return None
    
    def get_page_title(self) -> str:
        """
        Retorna o título da página atual
        
        Returns:
            str: Título da página
        """
        try:
            if self.page:
                return self.page.title()
            return ""
        except Exception:
            return ""
    
    def get_current_url(self) -> str:
        """
        Retorna a URL atual
        
        Returns:
            str: URL atual
        """
        try:
            if self.page:
                return self.page.url
            return ""
        except Exception:
            return ""
