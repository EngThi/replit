"""
Sistema de Interação com Google AI Studio (Versão Final Otimizada)
Com login automático melhorado e suporte a diferentes tipos de páginas
"""

import time
import json
import os
from datetime import datetime
from ai_studio_login_2fa import AIStudioLogin2FA
from credentials_manager import CredentialsManager

class AIStudioInteraction(AIStudioLogin2FA):
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
        """Acessa chat via URL específica com login automático"""
        try:
            print("🎯 Acessando AI Studio...")
            
            target_url = "https://aistudio.google.com/u/3/prompts/new_chat"
            self.page.goto(target_url, timeout=20000)
            time.sleep(5)
            
            final_url = self.page.url
            print(f"🔗 URL final: {final_url}")
            
            # Se redirecionado para login
            if "accounts.google.com" in final_url:
                print("🔑 Fazendo login...")
                
                if self.smart_login():
                    print("✅ Login concluído")
                    
                    # Tentar acessar chat novamente
                    self.page.goto(target_url, timeout=20000)
                    time.sleep(5)
                    
                    final_url = self.page.url
                    print(f"🔗 URL após login: {final_url}")
                else:
                    print("❌ Login falhou")
                    return False
            
            # Verificar se chegamos ao chat
            if "accounts.google.com" not in final_url:
                # Procurar campo de input
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
                    print("✅ Chat acessível!")
                    self.current_chat_url = final_url
                    self.take_screenshot("chat_ready")
                    return True
                else:
                    print("⚠️ Chat sem campo de input")
                    
                    # Tentar navegar para criar novo chat
                    return self.try_create_new_chat()
            
            return False
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def smart_login(self):
        """Login inteligente que detecta diferentes tipos de página"""
        try:
            time.sleep(3)
            
            # Detectar tipo de página
            page_info = self.page.evaluate("""
                () => {
                    const body = document.body.textContent.toLowerCase();
                    const url = window.location.href;
                    
                    return {
                        hasEmailField: !!document.querySelector('input[type="email"]'),
                        hasPasswordField: !!document.querySelector('input[type="password"]'),
                        isAccountChooser: body.includes('choose an account') || body.includes('escolher uma conta'),
                        bodyText: body.slice(0, 200),
                        url: url
                    };
                }
            """)
            
            print(f"🔍 Página detectada: {page_info}")
            
            # Escolhedor de conta
            if page_info['isAccountChooser']:
                print("👥 Selecionando conta...")
                return self.select_account()
            
            # Campo de email
            elif page_info['hasEmailField']:
                print("📧 Preenchendo email...")
                return self.fill_email_step()
            
            # Campo de senha
            elif page_info['hasPasswordField']:
                print("🔒 Preenchendo senha...")
                return self.fill_password_step()
            
            # Página desconhecida
            else:
                print("⚠️ Página desconhecida")
                self.take_screenshot("unknown_login_page")
                return self.wait_manual_login()
                
        except Exception as e:
            print(f"❌ Erro no login: {e}")
            return False
    
    def select_account(self):
        """Seleciona conta na página de escolha"""
        try:
            email = self.credentials_manager.get_email()
            if not email:
                return self.wait_manual_login()
            
            # Tentar clicar na conta
            account_selected = self.page.evaluate(f"""
                () => {{
                    const email = '{email}';
                    const elements = document.querySelectorAll('*');
                    
                    for (const el of elements) {{
                        if (el.textContent.includes(email) && el.offsetParent) {{
                            el.click();
                            return true;
                        }}
                    }}
                    
                    // Fallback: primeiro elemento clicável que parece conta
                    const clickable = document.querySelectorAll('[data-identifier], [role="button"], div[jsaction]');
                    for (const el of clickable) {{
                        if (el.textContent.includes('@')) {{
                            el.click();
                            return true;
                        }}
                    }}
                    
                    return false;
                }}
            """)
            
            if account_selected:
                print("✅ Conta selecionada")
                time.sleep(5)
                return self.smart_login()  # Recursão para próxima etapa
            else:
                return self.wait_manual_login()
                
        except Exception as e:
            print(f"❌ Erro selecionando conta: {e}")
            return False
    
    def fill_email_step(self):
        """Preenche email e avança"""
        try:
            email = self.credentials_manager.get_email()
            if not email:
                return self.wait_manual_login()
            
            self.page.fill('input[type="email"]', email)
            time.sleep(1)
            
            # Clicar Next
            if self.click_next_button():
                time.sleep(5)
                return self.smart_login()  # Recursão para próxima etapa
            
            return False
            
        except Exception as e:
            print(f"❌ Erro preenchendo email: {e}")
            return False
    
    def fill_password_step(self):
        """Preenche senha e faz login"""
        try:
            password = self.credentials_manager.get_password()
            if not password:
                return self.wait_manual_login()
            
            self.page.fill('input[type="password"]', password)
            time.sleep(1)
            
            # Clicar Next/Sign in
            if self.click_next_button():
                time.sleep(3)
                
                # Screenshot após envio
                self.take_screenshot("after_password_submit")
                print("📸 Screenshot salvo - verifique para 2FA!")
                
                return self.check_login_result()
            
            return False
            
        except Exception as e:
            print(f"❌ Erro preenchendo senha: {e}")
            return False
    
    def click_next_button(self):
        """Clica botão Next/Avançar de forma robusta"""
        selectors = [
            '#identifierNext', '#passwordNext',
            'button:has-text("Next")', 'button:has-text("Avançar")',
            'button:has-text("Sign in")', 'button:has-text("Entrar")',
            'input[type="submit"]', 'button[type="submit"]'
        ]
        
        for selector in selectors:
            try:
                if self.page.locator(selector).count() > 0:
                    self.page.click(selector)
                    return True
            except:
                continue
        
        # Fallback: Enter
        try:
            self.page.press('body', 'Enter')
            return True
        except:
            return False
    
    def check_login_result(self):
        """Verifica resultado do login"""
        try:
            time.sleep(5)
            current_url = self.page.url
            
            if "accounts.google.com" not in current_url:
                print("✅ Login concluído!")
                return True
            elif "challenge" in current_url or "2fa" in current_url.lower():
                print("🔐 2FA detectado!")
                return self.handle_2fa()
            else:
                print("⚠️ Ainda na página de login")
                return False
                
        except Exception as e:
            print(f"❌ Erro verificando login: {e}")
            return False
    
    def handle_2fa(self):
        """Aguarda resolução do 2FA"""
        try:
            print("📱 Aguarde - resolva o 2FA no seu dispositivo")
            print("⏳ 90 segundos para completar...")
            
            for i in range(18):  # 18 x 5 = 90 segundos
                time.sleep(5)
                
                if "accounts.google.com" not in self.page.url:
                    print(f"✅ 2FA resolvido em {(i+1)*5}s!")
                    self.take_screenshot("2fa_success")
                    return True
                
                if i % 6 == 0:  # A cada 30 segundos
                    print(f"⏳ Aguardando... ({(i+1)*5}s)")
            
            print("⚠️ Timeout do 2FA")
            return False
            
        except Exception as e:
            print(f"❌ Erro 2FA: {e}")
            return False
    
    def wait_manual_login(self):
        """Aguarda login manual"""
        print("⚠️ Aguardando login manual...")
        print("⏳ 60 segundos para fazer login...")
        
        for i in range(12):  # 12 x 5 = 60 segundos
            time.sleep(5)
            
            if "accounts.google.com" not in self.page.url:
                print("✅ Login manual concluído!")
                return True
                
        print("⚠️ Timeout do login manual")
        return False
    
    def try_create_new_chat(self):
        """Tenta criar novo chat se não estiver na página certa"""
        try:
            print("🔄 Tentando navegar para novo chat...")
            
            # URLs alternativas para tentar
            urls = [
                "https://aistudio.google.com/app/prompts/new_chat",
                "https://aistudio.google.com/prompts",
                "https://aistudio.google.com/"
            ]
            
            for url in urls:
                try:
                    self.page.goto(url, timeout=15000)
                    time.sleep(3)
                    
                    # Verificar se tem campo de input
                    has_input = self.page.evaluate("""
                        () => {
                            const inputs = document.querySelectorAll('textarea, [contenteditable="true"]');
                            for (const input of inputs) {
                                if (input.offsetParent && input.getBoundingClientRect().width > 200) {
                                    return true;
                                }
                            }
                            return false;
                        }
                    """)
                    
                    if has_input:
                        print(f"✅ Chat encontrado em: {url}")
                        self.current_chat_url = self.page.url
                        self.take_screenshot("chat_found")
                        return True
                        
                except Exception as e:
                    print(f"⚠️ Erro com {url}: {e}")
                    continue
            
            return False
            
        except Exception as e:
            print(f"❌ Erro criando chat: {e}")
            return False
    
    def find_input_field(self):
        """Encontra campo de input"""
        try:
            input_info = self.page.evaluate("""
                () => {
                    const selectors = ['textarea', '[contenteditable="true"]', 'input[type="text"]'];
                    
                    for (const selector of selectors) {
                        const elements = document.querySelectorAll(selector);
                        for (const el of elements) {
                            if (el.offsetParent && el.getBoundingClientRect().width > 200) {
                                let specificSelector = selector;
                                if (el.id) specificSelector = `#${el.id}`;
                                else if (el.className) {
                                    const firstClass = el.className.split(' ')[0];
                                    if (firstClass) specificSelector = `.${firstClass}`;
                                }
                                
                                return specificSelector;
                            }
                        }
                    }
                    return null;
                }
            """)
            
            if input_info:
                print(f"✅ Campo encontrado: {input_info}")
                return input_info
            else:
                print("❌ Campo não encontrado")
                return None
                
        except Exception as e:
            print(f"❌ Erro procurando campo: {e}")
            return None
    
    def send_message_robust(self, message):
        """Envia mensagem"""
        try:
            print(f"💬 Enviando: '{message[:50]}...'")
            
            input_selector = self.find_input_field()
            if not input_selector:
                return False
            
            # Focar e digitar
            self.page.click(input_selector)
            time.sleep(0.5)
            
            # Limpar e digitar
            self.page.evaluate(f"""
                () => {{
                    const field = document.querySelector('{input_selector}');
                    if (field) {{
                        field.value = '';
                        if (field.textContent !== undefined) field.textContent = '';
                        field.focus();
                    }}
                }}
            """)
            
            self.page.type(input_selector, message, delay=50)
            time.sleep(1)
            
            self.take_screenshot("before_send")
            
            # Enviar com Enter
            self.page.press(input_selector, "Enter")
            time.sleep(3)
            
            # Verificar se enviou
            field_empty = self.page.evaluate(f"""
                () => {{
                    const field = document.querySelector('{input_selector}');
                    if (field) {{
                        const value = field.value || field.textContent || '';
                        return value.trim() === '';
                    }}
                    return false;
                }}
            """)
            
            if field_empty:
                print("✅ Mensagem enviada!")
                self.conversation_history.append({
                    'type': 'user',
                    'content': message,
                    'timestamp': datetime.now().isoformat()
                })
                self.take_screenshot("after_send")
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Erro enviando: {e}")
            return False
    
    def wait_for_ai_response(self, timeout=60):
        """Aguarda resposta do AI"""
        try:
            print("🤖 Aguardando resposta...")
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                time.sleep(3)
                
                # Procurar resposta
                response = self.page.evaluate("""
                    () => {
                        // Procurar por respostas do AI
                        const selectors = [
                            '[data-message-author-role="model"]',
                            '.model-response',
                            '.ai-response'
                        ];
                        
                        for (const selector of selectors) {
                            const element = document.querySelector(selector);
                            if (element && element.textContent.trim().length > 10) {
                                return element.textContent.trim();
                            }
                        }
                        
                        // Fallback: procurar texto longo que parece resposta
                        const allDivs = document.querySelectorAll('div, p');
                        for (const div of allDivs) {
                            const text = div.textContent.trim();
                            if (text.length > 30 && text.length < 5000) {
                                // Verificar se parece resposta de AI
                                if (/\\b(i|eu|can|posso|help|ajud|yes|sim|no|não|the|a|an|um|uma)\\b/i.test(text)) {
                                    return text;
                                }
                            }
                        }
                        
                        return null;
                    }
                """)
                
                if response:
                    print(f"✅ Resposta: {response[:100]}...")
                    self.conversation_history.append({
                        'type': 'assistant',
                        'content': response,
                        'timestamp': datetime.now().isoformat()
                    })
                    self.take_screenshot("response_received")
                    return response
                
                elapsed = int(time.time() - start_time)
                if elapsed % 15 == 0:  # A cada 15 segundos
                    print(f"⏳ Aguardando... ({elapsed}s)")
            
            print("⏰ Timeout - resposta não encontrada")
            return None
            
        except Exception as e:
            print(f"❌ Erro aguardando resposta: {e}")
            return None
    
    def save_conversation(self):
        """Salva conversa"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"
            filepath = f"{self.interactions_dir}/conversations/{filename}"
            
            data = {
                'timestamp': datetime.now().isoformat(),
                'chat_url': self.current_chat_url,
                'conversation': self.conversation_history
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Conversa salva: {filename}")
            return filepath
            
        except Exception as e:
            print(f"❌ Erro salvando: {e}")
            return None
    
    def complete_interaction(self, message):
        """Executa interação completa"""
        try:
            print("🚀 INTERAÇÃO COMPLETA COM AI STUDIO")
            print("=" * 45)
            
            self.initialize_browser()
            
            if not self.access_chat_directly():
                print("❌ Não foi possível acessar chat")
                return None
            
            if not self.send_message_robust(message):
                print("❌ Falha ao enviar mensagem")
                return None
            
            response = self.wait_for_ai_response()
            conversation_file = self.save_conversation()
            
            if response:
                print("\n🎉 INTERAÇÃO CONCLUÍDA!")
                print(f"💬 Pergunta: {message}")
                print(f"🤖 Resposta: {response[:150]}...")
                print(f"📁 Salvo em: {conversation_file}")
                
                return {
                    'success': True,
                    'question': message,
                    'response': response,
                    'file': conversation_file
                }
            else:
                print("\n⚠️ Mensagem enviada mas resposta não capturada")
                return {
                    'success': False,
                    'question': message,
                    'response': None,
                    'file': conversation_file
                }
                
        except Exception as e:
            print(f"❌ Erro na interação: {e}")
            return None

def main():
    """Função principal"""
    print("🎯 SISTEMA AI STUDIO - VERSÃO FINAL")
    print("=" * 40)
    
    interaction = AIStudioInteraction(headless=True)
    
    try:
        message = input("\n💬 Sua pergunta (Enter para exemplo): ").strip()
        if not message:
            message = "Olá! Me explique brevemente como você funciona."
        
        result = interaction.complete_interaction(message)
        
        if result and result['success']:
            print(f"\n🎉 SUCESSO TOTAL!")
            print(f"📁 Arquivos em: {interaction.interactions_dir}")
        else:
            print(f"\n⚠️ Interação incompleta")
            
    except KeyboardInterrupt:
        print("\n⚠️ Interrompido")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    finally:
        interaction.cleanup()

if __name__ == "__main__":
    main()
