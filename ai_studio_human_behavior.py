#!/usr/bin/env python3
"""
🧠 AI STUDIO COM COMPORTAMENTO HUMANO
✅ Simula interações reais para evitar detecção de automação
✅ Pausas naturais, movimentos de mouse, delays variáveis
✅ Comportamento indistinguível de usuário real
"""

import sys
import time
import os
import random
from datetime import datetime
sys.path.append('/workspaces/replit')

from ai_studio_login_2fa import AIStudioLogin2FA
from credentials_manager import CredentialsManager

class AIStudioHumanBehavior(AIStudioLogin2FA):
    
    def __init__(self, headless=False):
        super().__init__(headless)
        self.human_delays = {
            'quick': (0.5, 1.5),      # Ações rápidas
            'normal': (1.0, 3.0),     # Ações normais
            'thinking': (2.0, 5.0),   # "Pensando"
            'reading': (3.0, 8.0),    # Lendo página
            'typing': (0.1, 0.3)      # Entre caracteres
        }
    
    def human_delay(self, delay_type='normal'):
        """Delay humanizado com variação natural"""
        min_delay, max_delay = self.human_delays[delay_type]
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        return delay
    
    def human_mouse_movement(self):
        """Simula movimento natural de mouse"""
        try:
            # Mover mouse para posições aleatórias da tela
            positions = [
                (200, 300), (400, 200), (600, 400), 
                (300, 500), (500, 250), (350, 350)
            ]
            
            for _ in range(random.randint(2, 4)):
                x, y = random.choice(positions)
                # Adicionar variação
                x += random.randint(-50, 50)
                y += random.randint(-50, 50)
                
                self.page.mouse.move(x, y)
                self.human_delay('quick')
                
        except Exception as e:
            print(f"⚠️ Mouse movement error: {e}")
    
    def human_typing(self, text, field_locator):
        """Digitação humanizada caracter por caracter"""
        try:
            # Limpar campo primeiro
            field_locator.clear()
            self.human_delay('quick')
            
            # Focar no campo
            field_locator.focus()
            self.human_delay('quick')
            
            # Digitar caracter por caracter
            for char in text:
                field_locator.type(char)
                # Delay variável entre caracteres
                typing_delay = random.uniform(0.05, 0.25)
                time.sleep(typing_delay)
                
                # Ocasionalmente pausar como se estivesse pensando
                if random.random() < 0.1:  # 10% chance
                    self.human_delay('thinking')
            
            print(f"✅ Texto digitado humanizadamente: {text[:20]}...")
            
        except Exception as e:
            print(f"❌ Erro na digitação humanizada: {e}")
            # Fallback para método normal
            field_locator.fill(text)
    
    def human_click(self, locator, description="elemento"):
        """Clique humanizado com movimento de mouse"""
        try:
            # Mover mouse próximo ao elemento primeiro
            bbox = locator.bounding_box()
            if bbox:
                # Posição próxima mas não exata
                target_x = bbox['x'] + bbox['width'] / 2 + random.randint(-10, 10)
                target_y = bbox['y'] + bbox['height'] / 2 + random.randint(-5, 5)
                
                self.page.mouse.move(target_x, target_y)
                self.human_delay('quick')
            
            # Pequena pausa antes do clique
            self.human_delay('quick')
            
            # Realizar clique
            locator.click()
            print(f"✅ Clique humanizado em: {description}")
            
            # Pausa após clique
            self.human_delay('normal')
            
        except Exception as e:
            print(f"❌ Erro no clique humanizado: {e}")
            # Fallback para clique normal
            locator.click()
    
    def simulate_page_reading(self):
        """Simula leitura da página"""
        print("👀 Simulando leitura da página...")
        
        # Scroll para cima e para baixo como se estivesse lendo
        for _ in range(random.randint(2, 4)):
            scroll_amount = random.randint(100, 300)
            self.page.mouse.wheel(0, scroll_amount)
            self.human_delay('reading')
            
            # Scroll de volta
            self.page.mouse.wheel(0, -scroll_amount // 2)
            self.human_delay('thinking')
    
    def take_screenshot(self, name):
        """Captura screenshot com nome personalizado"""
        try:
            screenshot_dir = "/workspaces/replit/interactions/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)
            
            self.page.screenshot(path=filepath)
            print(f"📸 Screenshot: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Erro ao capturar screenshot: {e}")
            return None

    def login_with_human_behavior(self):
        """
        Login com comportamento humano natural
        """
        print("🧠 INICIANDO LOGIN COM COMPORTAMENTO HUMANO")
        print("=" * 50)
        
        try:
            # ETAPA 1: Chegada à página (simular usuário chegando)
            target_url = "https://aistudio.google.com/"  # Página inicial primeiro
            print(f"🏠 Acessando página inicial primeiro...")
            
            self.page.goto(target_url, timeout=30000)
            self.human_delay('reading')
            
            # Simular leitura da página inicial
            self.simulate_page_reading()
            self.take_screenshot("01_homepage")
            
            # Agora ir para o chat (como usuário real faria)
            print("🔗 Navegando para o chat...")
            chat_url = "https://aistudio.google.com/u/3/prompts/new_chat"
            self.page.goto(chat_url, timeout=30000)
            self.human_delay('reading')
            
            current_url = self.page.url
            print(f"📍 URL atual: {current_url}")
            self.take_screenshot("02_initial_chat")
            
            # ETAPA 2: Lidar com login se necessário
            if "accounts.google.com" in current_url:
                print("🔑 Login necessário - comportamento humano")
                
                # Simular confusão/hesitação inicial
                self.human_delay('thinking')
                self.human_mouse_movement()
                
                if "accountchooser" in current_url:
                    print("👥 Escolhendo conta...")
                    
                    # Simular olhando as opções
                    self.simulate_page_reading()
                    
                    # Lista de contas para tentar
                    accounts = [
                        "thiago.edu511@gmail.com",
                        "steveplayer120@gmail.com"
                    ]
                    
                    account_found = False
                    for email in accounts:
                        print(f"👀 Procurando conta: {email}")
                        account_locator = self.page.locator(f'text={email}').first
                        
                        if account_locator.count() > 0 and account_locator.is_visible():
                            print(f"✅ Conta encontrada: {email}")
                            self.take_screenshot(f"03_before_account_click_{email.split('@')[0]}")
                            
                            # Clique humanizado
                            self.human_click(account_locator, f"conta {email}")
                            account_found = True
                            
                            # Aguardar carregamento
                            self.human_delay('reading')
                            current_url = self.page.url
                            print(f"📍 Após clique na conta: {current_url}")
                            break
                    
                    if not account_found:
                        print("⚠️ Nenhuma conta conhecida encontrada na página")
                
                # ETAPA 3: Detectar e inserir senha
                # Verificar se há campo de senha visível (independente da URL)
                password_field = self.page.locator('input[type="password"]').first
                
                if password_field.count() > 0 and password_field.is_visible():
                    print("🔐 Página de senha detectada! Inserindo senha humanamente...")
                    
                    credentials_manager = CredentialsManager()
                    
                    # Determinar qual conta estamos usando baseado na URL ou contexto
                    current_url = self.page.url
                    current_account = None
                    
                    # Verificar se conseguimos identificar a conta na página
                    for email in credentials_manager.get_accounts().keys():
                        if email.split('@')[0] in current_url or email in self.page.content():
                            current_account = email
                            break
                    
                    # Se não identificou, usar primeira disponível
                    if not current_account:
                        current_account = credentials_manager.get_email()
                    
                    password = credentials_manager.get_password_for_email(current_account)
                    
                    if password:
                        print(f"🔑 Usando conta: {current_account}")
                        credentials_manager.set_current_account(current_account)
                        
                        self.take_screenshot("04_password_page")
                        
                        # Simular leitura da página de senha
                        print("👀 Analisando página de senha...")
                        self.human_delay('reading')
                        
                        print("✅ Campo de senha encontrado")
                        
                        # Digitação humanizada
                        print("⌨️ Digitando senha humanamente...")
                        self.human_typing(password, password_field)
                        
                        self.take_screenshot("05_password_entered")
                        
                        # Pausa antes de enviar (como usuário pensando)
                        print("💭 Pausa antes de enviar...")
                        self.human_delay('thinking')
                        
                        # Enter humanizado
                        print("⏎ Enviando senha...")
                        self.page.keyboard.press('Enter')
                        print("✅ Senha enviada")
                        
                        # Aguardar processamento
                        print("⏳ Aguardando processamento...")
                        self.human_delay('reading')
                        
                        # Aguardar mudança de página
                        time.sleep(5)
                        current_url = self.page.url
                        print(f"📍 URL após senha: {current_url}")
                        
                elif "challenge/pwd" in current_url or "password" in current_url.lower():
                    print("🔐 Página de senha detectada pela URL...")
                    # Código original mantido como fallback
                    credentials_manager = CredentialsManager()
                    password = credentials_manager.get_password()
                    
                    if password:
                        self.take_screenshot("04_password_page_url")
                        self.human_delay('reading')
                        
                        password_field = self.page.locator('input[type="password"]').first
                        if password_field.count() > 0:
                            self.human_typing(password, password_field)
                            self.take_screenshot("05_password_entered_url")
                            self.human_delay('thinking')
                            self.page.keyboard.press('Enter')
                            print("✅ Senha enviada (método URL)")
                            self.human_delay('reading')
                
                # ETAPA 4: Aguardar carregamento final
                print("⏳ Aguardando carregamento completo...")
                
                # Aguardar até 30 segundos para carregar
                for i in range(6):
                    self.human_delay('normal')
                    current_url = self.page.url
                    
                    if "aistudio.google.com" in current_url and "accounts.google.com" not in current_url:
                        print(f"✅ Carregou AI Studio: {current_url}")
                        break
                    
                    print(f"⏳ Aguardando... ({i+1}/6)")
            
            # ETAPA 5: Interação inicial no AI Studio
            final_url = self.page.url
            print(f"📍 URL final: {final_url}")
            
            if "aistudio.google.com" in final_url:
                print("🎉 AI Studio acessado!")
                self.take_screenshot("06_ai_studio_loaded")
                
                # Simular comportamento de primeiro uso
                print("🧠 Simulando comportamento de primeiro uso...")
                
                # Aguardar página carregar completamente
                self.human_delay('reading')
                
                # Simular exploração da interface
                self.simulate_page_reading()
                
                # Pequenas interações como usuário real
                try:
                    # Tentar clicar em "Chat" se disponível
                    chat_btn = self.page.locator('text=Chat').first
                    if chat_btn.count() > 0 and chat_btn.is_visible():
                        print("💬 Clicando em Chat...")
                        self.human_click(chat_btn, "botão Chat")
                        self.human_delay('reading')
                
                except Exception as e:
                    print(f"⚠️ Interação opcional falhou: {e}")
                
                # Aguardar estabilizar
                self.human_delay('reading')
                self.take_screenshot("07_final_state")
                
                return True
            else:
                print("❌ Não chegou ao AI Studio")
                return False
                
        except Exception as e:
            print(f"❌ Erro no login humanizado: {e}")
            return False

def main():
    """Execução principal com comportamento humano"""
    print("🧠 AI STUDIO - COMPORTAMENTO HUMANO AVANÇADO")
    print("🎭 Simulando interações naturais para evitar detecção")
    print("=" * 60)
    
    # Usar modo não-headless para parecer mais humano
    system = AIStudioHumanBehavior(headless=True)  # Mude para False se quiser ver
    
    try:
        # Configurações adicionais para parecer humano
        print("🔧 Configurando navegador com perfil humano...")
        system.initialize_browser()
        
        # Adicionar configurações anti-detecção
        system.page.add_init_script("""
            // Remover indicadores de automação
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            // Simular comportamento humano
            window.chrome = {
                runtime: {}
            };
            
            // Adicionar propriedades humanas
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
        """)
        
        # Configurar viewport como desktop real
        system.page.set_viewport_size({"width": 1366, "height": 768})
        
        print("✅ Configurações aplicadas")
        
        # Executar login humanizado
        success = system.login_with_human_behavior()
        
        if success:
            print("\n" + "="*60)
            print("🎉 SUCESSO COM COMPORTAMENTO HUMANO!")
            print("✅ Login realizado naturalmente")
            print("✅ Detecção de automação evitada")
            print("✅ AI Studio acessível")
            print("💬 Pronto para interações naturais!")
            print("="*60)
            
            # Manter sessão ativa mais tempo para uso
            print("\n🕐 Mantendo sessão ativa por 60 segundos...")
            print("💡 Use este tempo para interagir manualmente se necessário")
            time.sleep(60)
            
        else:
            print("\n😞 Login humanizado não completou")
            print("📸 Verifique screenshots para análise")
            
    except Exception as e:
        print(f"\n❌ Erro no sistema: {e}")
        
    finally:
        try:
            system.cleanup()
        except:
            pass

if __name__ == "__main__":
    main()
