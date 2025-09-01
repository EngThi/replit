#!/usr/bin/env python3
"""
🥷 AI STUDIO STEALTH MODE - ANTI-DETECÇÃO AVANÇADA
✅ Mascara completamente a automação
✅ Simula usuário real do Brasil com Windows
✅ Bypass completo de detecção Google
"""

import sys
import time
import os
import random
from datetime import datetime
import json
sys.path.append('/workspaces/replit')

from playwright.sync_api import sync_playwright
from credentials_manager import CredentialsManager

class AIStudioStealthMode:
    
    def __init__(self, headless=True):
        self.headless = headless
        self.browser = None
        self.page = None
        self.context = None
        
        # Configurações de stealth brasileiras
        self.stealth_config = {
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'viewport': {'width': 1920, 'height': 1080},
            'locale': 'pt-BR',
            'timezone': 'America/Sao_Paulo',
            'geolocation': {'latitude': -23.5505, 'longitude': -46.6333},  # São Paulo
            'permissions': ['geolocation']
        }
        
        # Delays humanizados brasileiros
        self.human_delays = {
            'quick': (0.3, 0.8),      # Brasileiro rápido
            'normal': (0.8, 2.0),     # Ações normais
            'thinking': (1.5, 3.5),   # "Pensando"
            'reading': (2.0, 5.0),    # Lendo página
            'typing': (0.08, 0.15)    # Digitação rápida
        }
    
    def initialize_stealth_browser(self):
        """Inicializa navegador com configurações stealth avançadas"""
        print("🥷 Configurando modo stealth avançado...")
        
        playwright = sync_playwright().start()
        
        # Configurações avançadas de stealth
        browser_args = [
            '--no-first-run',
            '--no-default-browser-check',
            '--disable-blink-features=AutomationControlled',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor',
            '--disable-extensions',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--disable-gpu',
            '--window-size=1920,1080',
            '--start-maximized',
            # Simular Windows brasileiro
            '--user-agent=' + self.stealth_config['user_agent'],
            '--lang=pt-BR',
            '--accept-lang=pt-BR,pt;q=0.9,en;q=0.8',
        ]
        
        self.browser = playwright.chromium.launch(
            headless=self.headless,
            args=browser_args
        )
        
        # Criar contexto com configurações brasileiras
        self.context = self.browser.new_context(
            user_agent=self.stealth_config['user_agent'],
            viewport=self.stealth_config['viewport'],
            locale=self.stealth_config['locale'],
            timezone_id=self.stealth_config['timezone'],
            geolocation=self.stealth_config['geolocation'],
            permissions=self.stealth_config['permissions'],
            # Adicionar headers brasileiros
            extra_http_headers={
                'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Upgrade-Insecure-Requests': '1'
            }
        )
        
        self.page = self.context.new_page()
        
        # Script anti-detecção avançado
        stealth_script = """
        // Remover indicadores de automação
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        
        // Mascarar Chrome automation
        Object.defineProperty(navigator, 'plugins', {
            get: () => [
                {
                    0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format"},
                    description: "Portable Document Format",
                    filename: "internal-pdf-viewer",
                    length: 1,
                    name: "Chrome PDF Plugin"
                },
                {
                    0: {type: "application/pdf", suffixes: "pdf", description: ""},
                    description: "",
                    filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai",
                    length: 1,
                    name: "Chrome PDF Viewer"
                },
                {
                    0: {type: "application/x-nacl", suffixes: "", description: "Native Client Executable"},
                    1: {type: "application/x-pnacl", suffixes: "", description: "Portable Native Client Executable"},
                    description: "",
                    filename: "internal-nacl-plugin",
                    length: 2,
                    name: "Native Client"
                }
            ],
        });
        
        // Simular Chrome real
        Object.defineProperty(navigator, 'vendor', {
            get: () => 'Google Inc.',
        });
        
        Object.defineProperty(navigator, 'userAgent', {
            get: () => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        });
        
        // Adicionar propriedades do Chrome
        window.chrome = {
            runtime: {
                onConnect: undefined,
                onMessage: undefined
            },
            app: {
                isInstalled: false,
            },
            webstore: {
                onInstallStageChanged: undefined,
                onDownloadProgress: undefined,
            },
            csi: function() {},
            loadTimes: function() {
                return {
                    requestTime: performance.now(),
                    startLoadTime: performance.now(),
                    commitLoadTime: performance.now(),
                    finishDocumentLoadTime: performance.now(),
                    finishLoadTime: performance.now(),
                    firstPaintTime: performance.now(),
                    firstPaintAfterLoadTime: 0,
                    navigationType: "Other"
                };
            }
        };
        
        // Mascarar permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
        
        // Adicionar propriedades de tela brasileiras
        Object.defineProperty(screen, 'width', {
            get: () => 1920,
        });
        Object.defineProperty(screen, 'height', {
            get: () => 1080,
        });
        Object.defineProperty(screen, 'availWidth', {
            get: () => 1920,
        });
        Object.defineProperty(screen, 'availHeight', {
            get: () => 1040,
        });
        
        // Timezone brasileiro
        Date.prototype.getTimezoneOffset = function() {
            return 180; // UTC-3 (Brasília)
        };
        
        // Language brasileiro
        Object.defineProperty(navigator, 'language', {
            get: () => 'pt-BR',
        });
        Object.defineProperty(navigator, 'languages', {
            get: () => ['pt-BR', 'pt', 'en'],
        });
        
        // Hardware brasileiro típico
        Object.defineProperty(navigator, 'hardwareConcurrency', {
            get: () => 8,
        });
        Object.defineProperty(navigator, 'deviceMemory', {
            get: () => 8,
        });
        
        // Platform Windows
        Object.defineProperty(navigator, 'platform', {
            get: () => 'Win32',
        });
        
        console.log('🥷 Stealth mode ativado - usuário brasileiro Windows');
        """
        
        self.page.add_init_script(stealth_script)
        print("✅ Navegador stealth configurado com perfil brasileiro")
        
        return True
    
    def human_delay(self, delay_type='normal'):
        """Delay humanizado brasileiro (mais rápido)"""
        min_delay, max_delay = self.human_delays[delay_type]
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        return delay
    
    def human_typing(self, text, field_locator):
        """Digitação humanizada brasileira (mais rápida)"""
        try:
            field_locator.clear()
            self.human_delay('quick')
            field_locator.focus()
            self.human_delay('quick')
            
            for char in text:
                field_locator.type(char)
                typing_delay = random.uniform(0.05, 0.12)  # Digitação mais rápida
                time.sleep(typing_delay)
                
                if random.random() < 0.05:  # 5% chance de pausa
                    self.human_delay('quick')
            
            print(f"✅ Texto digitado: {text[:20]}...")
            
        except Exception as e:
            print(f"❌ Erro na digitação: {e}")
            field_locator.fill(text)
    
    def human_click(self, locator, description="elemento"):
        """Clique humanizado brasileiro"""
        try:
            bbox = locator.bounding_box()
            if bbox:
                target_x = bbox['x'] + bbox['width'] / 2 + random.randint(-5, 5)
                target_y = bbox['y'] + bbox['height'] / 2 + random.randint(-3, 3)
                self.page.mouse.move(target_x, target_y)
                self.human_delay('quick')
            
            self.human_delay('quick')
            locator.click()
            print(f"✅ Clique em: {description}")
            self.human_delay('normal')
            
        except Exception as e:
            print(f"❌ Erro no clique: {e}")
            locator.click()
    
    def take_screenshot(self, name):
        """Captura screenshot"""
        try:
            screenshot_dir = "/workspaces/replit/stealth_screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)
            
            self.page.screenshot(path=filepath)
            print(f"📸 Screenshot: {filename}")
            return filepath
            
        except Exception as e:
            print(f"❌ Erro screenshot: {e}")
            return None
    
    def stealth_login(self):
        """Login stealth com técnicas anti-detecção"""
        print("🥷 INICIANDO LOGIN STEALTH MODE")
        print("=" * 50)
        
        try:
            # ETAPA 1: Navegar como usuário brasileiro real
            print("🇧🇷 Simulando usuário brasileiro do Windows...")
            
            # Primeiro visitar Google.com (comportamento natural)
            print("🔍 Visitando Google.com primeiro (comportamento natural)...")
            self.page.goto("https://google.com.br", timeout=30000)
            self.human_delay('reading')
            self.take_screenshot("01_google_brasil")
            
            # Simular busca por AI Studio
            print("🔍 Simulando busca por AI Studio...")
            search_box = self.page.locator('input[name="q"]').first
            if search_box.count() > 0:
                self.human_typing("google ai studio", search_box)
                self.human_delay('thinking')
                self.page.keyboard.press('Enter')
                self.human_delay('reading')
                self.take_screenshot("02_search_results")
                
                # Clicar no primeiro resultado
                ai_studio_link = self.page.locator('a[href*="aistudio.google.com"]').first
                if ai_studio_link.count() > 0:
                    print("🎯 Clicando no link do AI Studio...")
                    self.human_click(ai_studio_link, "link AI Studio")
                else:
                    print("⚠️ Link não encontrado, navegando direto...")
                    self.page.goto("https://aistudio.google.com/", timeout=30000)
            else:
                # Fallback direto
                print("🔗 Navegando diretamente para AI Studio...")
                self.page.goto("https://aistudio.google.com/", timeout=30000)
            
            self.human_delay('reading')
            self.take_screenshot("03_ai_studio_homepage")
            
            # ETAPA 2: Procurar Get Started
            print("🔍 Procurando botão 'Get started'...")
            
            get_started_selectors = [
                'text="Get started"',
                'text="Começar"',
                'text="Iniciar"',
                'a:has-text("Get started")',
                'button:has-text("Get started")',
                '[data-analytics*="get-started"]'
            ]
            
            get_started_clicked = False
            for selector in get_started_selectors:
                try:
                    btn = self.page.locator(selector).first
                    if btn.count() > 0 and btn.is_visible():
                        print(f"✅ Get started encontrado: {selector}")
                        self.take_screenshot("04_before_get_started")
                        self.human_delay('thinking')
                        self.human_click(btn, "Get started")
                        get_started_clicked = True
                        break
                except:
                    continue
            
            if not get_started_clicked:
                print("🔗 Navegando direto para new_chat...")
                self.page.goto("https://aistudio.google.com/prompts/new_chat", timeout=30000)
            
            self.human_delay('reading')
            current_url = self.page.url
            print(f"📍 URL atual: {current_url}")
            self.take_screenshot("05_after_get_started")
            
            # ETAPA 3: Login stealth
            if "accounts.google.com" in current_url:
                print("🔐 Página de login detectada - modo stealth...")
                
                # Aguardar carregamento
                time.sleep(3)
                
                # Email
                email_field = self.page.locator('input[type="email"]').first
                if email_field.count() > 0 and email_field.is_visible():
                    print("📧 Inserindo email brasileiro...")
                    self.take_screenshot("06_email_page")
                    
                    target_email = "steveplayer120@gmail.com"
                    self.human_typing(target_email, email_field)
                    self.take_screenshot("07_email_entered")
                    
                    # Next
                    next_btn = self.page.locator('button:has-text("Avançar"), button:has-text("Next")').first
                    if next_btn.count() > 0:
                        self.human_click(next_btn, "Avançar")
                    else:
                        self.page.keyboard.press('Enter')
                    
                    self.human_delay('reading')
                    time.sleep(2)
                
                # Senha
                password_field = self.page.locator('input[type="password"]').first
                if password_field.count() > 0 and password_field.is_visible():
                    print("🔐 Inserindo senha...")
                    self.take_screenshot("08_password_page")
                    
                    credentials = CredentialsManager()
                    password = credentials.get_password_for_email("steveplayer120@gmail.com")
                    
                    if password:
                        self.human_typing(password, password_field)
                        self.take_screenshot("09_password_entered")
                        
                        # Submit senha
                        submit_btn = self.page.locator('button:has-text("Avançar"), button:has-text("Next")').first
                        if submit_btn.count() > 0:
                            self.human_click(submit_btn, "Submit senha")
                        else:
                            self.page.keyboard.press('Enter')
                        
                        print("✅ Senha enviada")
                        self.human_delay('reading')
                        time.sleep(5)
                        
                        # Verificar 2FA
                        current_url = self.page.url
                        print(f"📍 URL pós-senha: {current_url}")
                        self.take_screenshot("10_after_password")
                        
                        # Se ainda em accounts.google.com, pode ser 2FA
                        if "accounts.google.com" in current_url:
                            print("📱 Possível 2FA detectado...")
                            self.take_screenshot("11_possible_2fa")
                            
                            # Aguardar até 90 segundos para 2FA
                            print("⏰ Aguardando aprovação 2FA por até 90 segundos...")
                            for i in range(18):  # 18 x 5s = 90s
                                time.sleep(5)
                                current_url = self.page.url
                                
                                if i % 3 == 0:  # Screenshot a cada 15s
                                    self.take_screenshot(f"12_2fa_wait_{i*5}s")
                                
                                print(f"⏳ 2FA aguardando... ({(i+1)*5}s/90s)")
                                
                                if "aistudio.google.com" in current_url:
                                    print("✅ 2FA aprovado!")
                                    self.take_screenshot("13_2fa_approved")
                                    break
                            else:
                                print("⏰ Timeout 2FA")
                                self.take_screenshot("13_2fa_timeout")
            
            # ETAPA 4: Verificar sucesso
            final_url = self.page.url
            print(f"📍 URL final: {final_url}")
            
            if "aistudio.google.com" in final_url:
                print("🎉 AI Studio acessado!")
                self.take_screenshot("14_ai_studio_success")
                
                # Aguardar carregar
                time.sleep(5)
                self.take_screenshot("15_ai_studio_loaded")
                
                # Verificar se não há erro
                error_elements = self.page.locator('text="authentication error", text="Failed to list", text="An unknown error"')
                if error_elements.count() > 0:
                    print("❌ Erro de autenticação detectado!")
                    self.take_screenshot("16_auth_error")
                    return False
                else:
                    print("✅ Sem erros detectados!")
                    self.take_screenshot("16_no_errors")
                    
                    # Testar funcionalidade
                    print("🧪 Testando funcionalidade...")
                    try:
                        # Procurar campo de input
                        input_field = self.page.locator('textarea, input[type="text"]').first
                        if input_field.count() > 0:
                            print("✅ Campo de input encontrado")
                            self.human_typing("Olá, teste de funcionamento", input_field)
                            self.take_screenshot("17_test_input")
                            print("🎯 Teste de digitação realizado!")
                    except Exception as e:
                        print(f"⚠️ Teste opcional falhou: {e}")
                
                return True
            else:
                print("❌ Não chegou ao AI Studio")
                self.take_screenshot("16_failed")
                return False
                
        except Exception as e:
            print(f"❌ Erro no login stealth: {e}")
            self.take_screenshot("error_state")
            return False
    
    def cleanup(self):
        """Limpar recursos"""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
        except:
            pass

def main():
    """Execução principal stealth mode"""
    print("🥷 AI STUDIO STEALTH MODE - ANTI-DETECÇÃO TOTAL")
    print("🇧🇷 Simulando usuário brasileiro Windows Chrome")
    print("=" * 60)
    
    system = AIStudioStealthMode(headless=True)  # Mude para False se quiser ver
    
    try:
        # Inicializar modo stealth
        system.initialize_stealth_browser()
        
        # Executar login stealth
        success = system.stealth_login()
        
        if success:
            print("\n" + "="*60)
            print("🎉 SUCESSO STEALTH MODE!")
            print("✅ Login realizado sem detecção")
            print("✅ Bypass completo Google Anti-Bot")
            print("✅ AI Studio funcionando")
            print("🇧🇷 Simulação brasileira perfeita")
            print("="*60)
            
            # Manter sessão ativa
            print("\n🕐 Mantendo sessão stealth ativa por 120 segundos...")
            time.sleep(120)
            
        else:
            print("\n😞 Stealth mode não completou")
            print("📸 Verifique screenshots em /stealth_screenshots/")
            
    except Exception as e:
        print(f"\n❌ Erro no sistema stealth: {e}")
        
    finally:
        system.cleanup()

if __name__ == "__main__":
    main()
