from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext
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
        try:
            self.playwright = sync_playwright().start()
            
            # Configurações do navegador
            browser_options = {
                'headless': self.headless,
                'args': [
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor'
                ]
            }
            
            self.browser = self.playwright.chromium.launch(**browser_options)
            self.context = self.browser.new_context(
                viewport={'width': 1366, 'height': 768},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )
            self.page = self.context.new_page()
            
            # Configurar timeouts
            self.page.set_default_timeout(30000)  # 30 segundos
            
        except Exception as e:
            raise Exception(f"Erro ao inicializar navegador: {str(e)}")
    
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
        Inicia o processo de login clicando no botão Sign in
        """
        try:
            # Aguardar e clicar no botão de login
            sign_in_selectors = [
                "text=Sign in",
                "text=Fazer login",
                "text=Entrar",
                "[data-value='sign_in']",
                "button:has-text('Sign in')",
                "a:has-text('Sign in')"
            ]
            
            for selector in sign_in_selectors:
                try:
                    self.page.wait_for_selector(selector, timeout=5000)
                    self.page.click(selector)
                    break
                except:
                    continue
            else:
                raise Exception("Botão de login não encontrado")
            
            # Aguardar redirecionamento para página de login do Google
            self.page.wait_for_url("**/accounts.google.com/**", timeout=10000)
            
        except Exception as e:
            raise Exception(f"Erro ao iniciar login: {str(e)}")
    
    def enter_email(self, email: str):
        """
        Insere o email no formulário de login
        
        Args:
            email (str): Email para login
        """
        try:
            # Aguardar campo de email
            email_selectors = [
                "input[type='email']",
                "input[name='identifier']",
                "#identifierId",
                "input[autocomplete='username']"
            ]
            
            email_field = None
            for selector in email_selectors:
                try:
                    self.page.wait_for_selector(selector, timeout=5000)
                    email_field = selector
                    break
                except:
                    continue
            
            if not email_field:
                raise Exception("Campo de email não encontrado")
            
            # Limpar e inserir email
            self.page.fill(email_field, "")
            self.page.fill(email_field, email)
            
            # Clicar em "Próximo"
            next_selectors = [
                "text=Next",
                "text=Próximo",
                "#identifierNext",
                "button[type='submit']"
            ]
            
            for selector in next_selectors:
                try:
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
        Insere a senha no formulário de login
        
        Args:
            password (str): Senha para login
        """
        try:
            # Aguardar campo de senha
            password_selectors = [
                "input[type='password']",
                "input[name='password']",
                "#password",
                "input[autocomplete='current-password']"
            ]
            
            password_field = None
            for selector in password_selectors:
                try:
                    self.page.wait_for_selector(selector, timeout=10000)
                    password_field = selector
                    break
                except:
                    continue
            
            if not password_field:
                raise Exception("Campo de senha não encontrado")
            
            # Limpar e inserir senha
            self.page.fill(password_field, "")
            self.page.fill(password_field, password)
            
            # Clicar em "Próximo"
            next_selectors = [
                "text=Next",
                "text=Próximo",
                "#passwordNext",
                "button[type='submit']"
            ]
            
            for selector in next_selectors:
                try:
                    self.page.click(selector)
                    break
                except:
                    continue
            
        except Exception as e:
            raise Exception(f"Erro ao inserir senha: {str(e)}")
    
    def wait_for_2fa(self):
        """
        Aguarda a autenticação de dois fatores
        """
        try:
            # Aguardar o tempo configurado para 2FA
            self.page.wait_for_timeout(self.timeout_2fa)
            
            # Verificar se ainda estamos na página de login ou se foi redirecionado
            current_url = self.page.url
            
            # Se ainda estivermos em accounts.google.com, pode ser que o 2FA não foi concluído
            if "accounts.google.com" in current_url:
                # Verificar se há elementos de 2FA na página
                two_fa_indicators = [
                    "text=2-Step Verification",
                    "text=Verificação em duas etapas",
                    "text=Enter code",
                    "text=Digite o código",
                    "input[type='tel']"
                ]
                
                for indicator in two_fa_indicators:
                    try:
                        if self.page.is_visible(indicator):
                            raise Exception("Autenticação de dois fatores não foi concluída no tempo esperado")
                    except:
                        continue
            
        except Exception as e:
            if "Autenticação de dois fatores" in str(e):
                raise e
            else:
                # Se der timeout mas não for erro de 2FA, consideramos sucesso
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
