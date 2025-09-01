"""
Versão Corrigida - Sem Loop Infinito
Detecta e resolve o problema da página de escolha de conta
"""

import time
import json
import os
from datetime import datetime
from ai_studio_login_2fa import AIStudioLogin2FA
from credentials_manager import CredentialsManager

class AIStudioInteractionFixed(AIStudioLogin2FA):
    def __init__(self, headless=True):
        super().__init__(headless)
        self.current_chat_url = None
        self.conversation_history = []
        self.interactions_dir = "/workspaces/replit/interactions"
        self.credentials_manager = CredentialsManager()
        self.ensure_interaction_dirs()
        
    def ensure_interaction_dirs(self):
        """Cria diretórios necessários"""
        os.makedirs(self.interactions_dir, exist_ok=True)
        os.makedirs(f"{self.interactions_dir}/screenshots", exist_ok=True)
        os.makedirs(f"{self.interactions_dir}/conversations", exist_ok=True)
    
    def take_screenshot(self, name):
        """Captura screenshot"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = f"{self.interactions_dir}/screenshots/{name}_{timestamp}.png"
            self.page.screenshot(path=path, full_page=True)
            print(f"📸 Screenshot: {path}")
            return path
        except Exception as e:
            print(f"❌ Erro screenshot: {e}")
            return None
    
    def access_chat_directly(self):
        """Acessa chat com correção de loop infinito"""
        try:
            print("🎯 Acessando chat (versão corrigida)...")
            
            target_url = "https://aistudio.google.com/u/3/prompts/new_chat"
            print(f"🔗 URL: {target_url}")
            
            self.page.goto(target_url, timeout=20000)
            time.sleep(3)
            
            final_url = self.page.url
            print(f"🔗 URL inicial: {final_url}")
            
            # Se redirecionado para login, fazer login
            if "accounts.google.com" in final_url:
                print("🔑 Redirecionado para login...")
                
                if self.handle_google_login_with_loop_prevention():
                    print("✅ Login realizado, tentando acessar chat novamente...")
                    
                    # Tentar novamente após login
                    self.page.goto(target_url, timeout=20000)
                    time.sleep(5)
                    
                    final_url = self.page.url
                    print(f"🔗 URL após login: {final_url}")
                else:
                    print("❌ Login falhou")
                    return False
            
            # Verificar se chegamos ao chat
            if "accounts.google.com" not in final_url:
                # Procurar por campo de input
                has_input = self.page.evaluate("""
                    () => {
                        const selectors = ['textarea', 'input[type="text"]', '[contenteditable="true"]'];
                        for (const sel of selectors) {
                            const elements = document.querySelectorAll(sel);
                            for (const el of elements) {
                                if (el.offsetParent && el.getBoundingClientRect().width > 100) {
                                    return true;
                                }
                            }
                        }
                        return false;
                    }
                """)
                
                if has_input:
                    print(f"✅ Chat acessível!")
                    self.current_chat_url = final_url
                    self.take_screenshot("chat_ready")
                    return True
                else:
                    print(f"⚠️ Página carregou mas sem campo de input")
                    self.take_screenshot("no_input_found")
            else:
                print(f"⚠️ Ainda na página de login")
            
            return False
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def handle_google_login_with_loop_prevention(self):
        """Login do Google com prevenção de loop infinito"""
        try:
            print("🔐 Fazendo login com prevenção de loop...")
            
            max_attempts = 5  # Máximo 5 tentativas
            account_chooser_attempts = 0
            
            for attempt in range(max_attempts):
                print(f"\n🔄 Tentativa {attempt + 1}/{max_attempts}")
                
                current_url = self.page.url
                print(f"🔗 URL atual: {current_url[:80]}...")
                
                # Detectar tipo de página
                page_info = self.page.evaluate("""
                    () => {
                        const hasEmail = document.querySelector('input[type="email"]') !== null;
                        const hasPassword = document.querySelector('input[type="password"]') !== null;
                        const bodyText = document.body.textContent.toLowerCase();
                        const isAccountChooser = bodyText.includes('choose an account') || 
                                               bodyText.includes('escolher conta') ||
                                               bodyText.includes('thiago.edu511@gmail.com');
                        
                        return {
                            hasEmailField: hasEmail,
                            hasPasswordField: hasPassword,
                            isAccountChooser: isAccountChooser,
                            url: window.location.href
                        };
                    }
                """)
                
                print(f"🔍 Página: {page_info}")
                
                # Se não estamos mais em página de login, sucesso!
                if "accounts.google.com" not in current_url:
                    print("✅ Login concluído - saiu da página Google!")
                    return True
                
                # Página de escolha de conta
                if page_info['isAccountChooser']:
                    account_chooser_attempts += 1
                    print(f"👥 Página de escolha (tentativa {account_chooser_attempts})")
                    
                    if account_chooser_attempts > 2:
                        print("❌ Muitas tentativas na escolha de conta - possível loop")
                        print("🔧 Tentando aguardar mais tempo...")
                        time.sleep(10)
                        
                        # Verificar se saiu da página
                        new_url = self.page.url
                        if "accounts.google.com" not in new_url:
                            print("✅ Saiu da página de login após aguardar!")
                            return True
                        
                        # Se ainda em loop, tentar abordagem diferente
                        if account_chooser_attempts > 3:
                            print("⚠️ Loop detectado - tentando abordagem alternativa")
                            break
                    
                    # Tentar clicar na conta
                    success = self.click_account_safely()
                    if success:
                        # Aguardar navegação
                        print("⏳ Aguardando navegação...")
                        time.sleep(5)
                        
                        # Verificar se mudou de página
                        new_url = self.page.url
                        if new_url != current_url:
                            print(f"✅ URL mudou: {new_url[:50]}...")
                            
                            # Se não está mais no Google accounts, sucesso
                            if "accounts.google.com" not in new_url:
                                print("🎉 Login completo!")
                                return True
                        else:
                            print("⚠️ URL não mudou - possível loop")
                
                # Página de email
                elif page_info['hasEmailField']:
                    print("📧 Página de email")
                    if self.handle_email_step():
                        time.sleep(3)
                        continue
                    else:
                        break
                
                # Página de senha
                elif page_info['hasPasswordField']:
                    print("🔒 Página de senha")
                    if self.handle_password_step():
                        time.sleep(5)
                        continue
                    else:
                        break
                
                else:
                    print("❓ Página desconhecida - aguardando...")
                    time.sleep(3)
            
            print("❌ Login não concluído após todas as tentativas")
            return False
            
        except Exception as e:
            print(f"❌ Erro no login: {e}")
            return False
    
    def click_account_safely(self):
        """Clica na conta de forma segura"""
        try:
            print("👤 Clicando na conta...")
            
            # Múltiplos seletores para a conta
            account_selectors = [
                'div:has-text("thiago.edu511@gmail.com")',
                'div:has-text("Thiago")',
                '[data-email="thiago.edu511@gmail.com"]',
                '.BHzsHc',  # Classe comum para itens de conta
                '.oOGH8d',  # Outra classe comum
            ]
            
            for selector in account_selectors:
                try:
                    elements = self.page.query_selector_all(selector)
                    for element in elements:
                        if element.is_visible():
                            print(f"🎯 Clicando: {selector}")
                            element.click()
                            return True
                except:
                    continue
            
            # Fallback: clicar no primeiro elemento visível que contém o email
            try:
                self.page.click('text=thiago.edu511@gmail.com')
                print("✅ Clique via texto do email")
                return True
            except:
                pass
            
            print("❌ Não foi possível clicar na conta")
            return False
            
        except Exception as e:
            print(f"❌ Erro ao clicar na conta: {e}")
            return False
    
    def handle_email_step(self):
        """Gerencia step do email"""
        try:
            email = self.credentials_manager.get_email()
            if email:
                print(f"📧 Preenchendo email: {email}")
                self.page.fill('input[type="email"]', email)
                time.sleep(1)
                
                # Clicar Next
                self.page.press('input[type="email"]', 'Enter')
                return True
            else:
                print("❌ Email não configurado")
                return False
        except Exception as e:
            print(f"❌ Erro email step: {e}")
            return False
    
    def handle_password_step(self):
        """Gerencia step da senha"""
        try:
            password = self.credentials_manager.get_password()
            if password:
                print(f"🔒 Preenchendo senha...")
                self.page.fill('input[type="password"]', password)
                time.sleep(1)
                
                # Screenshot após senha
                self.take_screenshot("after_password")
                
                # Enviar
                self.page.press('input[type="password"]', 'Enter')
                
                print("📸 Screenshot capturado após enviar senha")
                return True
            else:
                print("❌ Senha não configurada")
                return False
        except Exception as e:
            print(f"❌ Erro password step: {e}")
            return False

def main():
    """Teste da versão corrigida"""
    print("🚀 TESTE VERSÃO SEM LOOP INFINITO")
    print("=" * 40)
    
    interaction = AIStudioInteractionFixed(headless=True)
    
    try:
        interaction.initialize_browser()
        
        if interaction.access_chat_directly():
            print("🎉 SUCESSO! Chat acessível!")
        else:
            print("⚠️ Não foi possível acessar chat")
            
    except KeyboardInterrupt:
        print("\n⚠️ Interrompido")
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        interaction.cleanup()

if __name__ == "__main__":
    main()
