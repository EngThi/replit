"""
Sistema de Interação com Google AI Studio
Permite navegar, criar chats e enviar mensagens após login
"""

import time
import json
from persistent_login import PersistentGoogleLogin

class AIStudioInteraction(PersistentGoogleLogin):
    def __init__(self):
        super().__init__()
        self.current_chat_url = None
    
    def navigate_to_studio(self):
        """Navega para a página principal do AI Studio"""
        try:
            print("🌐 Navegando para Google AI Studio...")
            self.page.goto("https://aistudio.google.com/", timeout=30000)
            self.page.wait_for_load_state('networkidle')
            time.sleep(3)
            
            # Verificar se carregou corretamente
            title = self.page.title()
            print(f"📄 Título da página: {title}")
            
            # Capturar screenshot
            self.page.screenshot(path="ai_studio_main.png")
            print("📸 Screenshot salvo: ai_studio_main.png")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao navegar: {e}")
            return False
    
    def find_and_click_new_chat(self):
        """Encontra e clica no botão para criar novo chat"""
        try:
            print("🔍 Procurando botão 'New Chat' ou similar...")
            
            # Possíveis seletores para novo chat
            new_chat_selectors = [
                "text=New chat",
                "text=Create new",
                "text=Start new",
                "text=Novo chat",
                "text=Criar novo",
                "[data-testid*='new-chat']",
                "[aria-label*='new chat']",
                "[aria-label*='create']",
                "button:has-text('New')",
                "button:has-text('Create')",
                ".create-button",
                ".new-chat-button",
                "[role='button']:has-text('New')"
            ]
            
            for selector in new_chat_selectors:
                try:
                    if self.page.is_visible(selector, timeout=3000):
                        print(f"✅ Encontrado botão: {selector}")
                        self.page.click(selector)
                        time.sleep(3)
                        
                        # Verificar se abriu nova página/modal
                        current_url = self.page.url
                        print(f"🔗 URL atual: {current_url}")
                        
                        return True
                except Exception as e:
                    print(f"⚠️ Seletor {selector} falhou: {e}")
                    continue
            
            # Se não encontrou, tentar abordagem JavaScript
            print("🔧 Tentando encontrar via JavaScript...")
            
            found_button = self.page.evaluate("""
                () => {
                    const buttons = Array.from(document.querySelectorAll('button, a, [role="button"], div[onclick]'));
                    const searchTerms = ['new', 'create', 'start', 'novo', 'criar', 'começar'];
                    
                    for (const button of buttons) {
                        const text = button.textContent.toLowerCase().trim();
                        const ariaLabel = (button.getAttribute('aria-label') || '').toLowerCase();
                        
                        if (searchTerms.some(term => text.includes(term) || ariaLabel.includes(term))) {
                            button.click();
                            return {
                                text: button.textContent.trim(),
                                html: button.outerHTML.slice(0, 200)
                            };
                        }
                    }
                    return null;
                }
            """)
            
            if found_button:
                print(f"✅ Clicou via JavaScript: {found_button['text']}")
                time.sleep(3)
                return True
            
            print("❌ Nenhum botão 'New Chat' encontrado")
            return False
            
        except Exception as e:
            print(f"❌ Erro ao procurar novo chat: {e}")
            return False
    
    def select_model(self, model_name="Gemini"):
        """Seleciona o modelo de IA (Gemini, etc)"""
        try:
            print(f"🤖 Procurando modelo: {model_name}")
            
            # Aguardar página carregar
            time.sleep(3)
            
            model_selectors = [
                f"text={model_name}",
                f"button:has-text('{model_name}')",
                f"[data-testid*='{model_name.lower()}']",
                f"[aria-label*='{model_name}']",
                ".model-selector",
                ".model-option"
            ]
            
            for selector in model_selectors:
                try:
                    if self.page.is_visible(selector, timeout=5000):
                        print(f"✅ Encontrado modelo: {selector}")
                        self.page.click(selector)
                        time.sleep(2)
                        return True
                except:
                    continue
            
            print(f"⚠️ Modelo {model_name} não encontrado, continuando...")
            return True  # Continuar mesmo se não encontrar
            
        except Exception as e:
            print(f"❌ Erro ao selecionar modelo: {e}")
            return False
    
    def send_message(self, message):
        """Envia uma mensagem no chat"""
        try:
            print(f"💬 Enviando mensagem: '{message[:50]}...'")
            
            # Procurar campo de texto
            text_field_selectors = [
                "textarea[placeholder*='message']",
                "textarea[placeholder*='pergunt']",
                "textarea[placeholder*='type']",
                "textarea[placeholder*='enter']",
                "input[type='text']",
                "textarea",
                "[contenteditable='true']",
                ".chat-input",
                ".message-input",
                "[data-testid*='input']",
                "[role='textbox']"
            ]
            
            text_field = None
            for selector in text_field_selectors:
                try:
                    if self.page.is_visible(selector, timeout=3000):
                        text_field = selector
                        print(f"✅ Campo de texto encontrado: {selector}")
                        break
                except:
                    continue
            
            if not text_field:
                # Tentar encontrar via JavaScript
                text_field_info = self.page.evaluate("""
                    () => {
                        const inputs = Array.from(document.querySelectorAll('textarea, input[type="text"], [contenteditable="true"]'));
                        for (const input of inputs) {
                            if (input.offsetParent !== null) { // Elemento visível
                                return {
                                    tagName: input.tagName,
                                    placeholder: input.placeholder,
                                    id: input.id,
                                    className: input.className
                                };
                            }
                        }
                        return null;
                    }
                """)
                
                if text_field_info:
                    print(f"🔍 Campo encontrado via JS: {text_field_info}")
                    # Usar seletor mais específico
                    if text_field_info['id']:
                        text_field = f"#{text_field_info['id']}"
                    elif text_field_info['className']:
                        text_field = f".{text_field_info['className'].split()[0]}"
                    else:
                        text_field = text_field_info['tagName'].lower()
            
            if not text_field:
                raise Exception("Campo de texto não encontrado")
            
            # Limpar e digitar mensagem
            self.page.click(text_field)
            time.sleep(0.5)
            
            # Limpar campo
            self.page.fill(text_field, "")
            time.sleep(0.3)
            
            # Digitar mensagem de forma humana
            for char in message:
                self.page.type(text_field, char, delay=50)
            
            time.sleep(1)
            
            # Procurar botão de envio
            send_button_selectors = [
                "button[type='submit']",
                "text=Send",
                "text=Enviar",
                "[aria-label*='send']",
                "[aria-label*='enviar']",
                ".send-button",
                "[data-testid*='send']",
                "button:has-text('Send')",
                "button svg", # Botões com ícone de envio
                "[role='button']:has([aria-label*='send'])"
            ]
            
            sent = False
            for selector in send_button_selectors:
                try:
                    if self.page.is_visible(selector, timeout=2000):
                        print(f"✅ Botão de envio encontrado: {selector}")
                        self.page.click(selector)
                        sent = True
                        break
                except:
                    continue
            
            if not sent:
                # Tentar Enter
                print("⌨️ Tentando enviar com Enter...")
                self.page.press(text_field, "Enter")
                sent = True
            
            if sent:
                print("✅ Mensagem enviada!")
                time.sleep(3)  # Aguardar processamento
                return True
            else:
                print("❌ Não foi possível enviar mensagem")
                return False
            
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem: {e}")
            return False
    
    def wait_for_response(self, timeout=30):
        """Aguarda e captura a resposta do AI"""
        try:
            print("⏳ Aguardando resposta do AI...")
            
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                # Procurar indicadores de que a resposta chegou
                response_indicators = [
                    ".response",
                    ".ai-response", 
                    ".assistant-message",
                    ".bot-message",
                    "[data-testid*='response']",
                    "[role='article']",
                    ".message:last-child"
                ]
                
                for indicator in response_indicators:
                    try:
                        if self.page.is_visible(indicator):
                            # Aguardar um pouco mais para garantir que a resposta terminou
                            time.sleep(3)
                            
                            # Capturar texto da resposta
                            response_text = self.page.evaluate(f"""
                                () => {{
                                    const element = document.querySelector('{indicator}');
                                    return element ? element.textContent.trim() : '';
                                }}
                            """)
                            
                            if response_text and len(response_text) > 10:
                                print(f"✅ Resposta recebida ({len(response_text)} chars)")
                                print(f"📝 Início da resposta: {response_text[:100]}...")
                                return response_text
                    except:
                        continue
                
                time.sleep(1)
            
            print("⏰ Timeout aguardando resposta")
            return None
            
        except Exception as e:
            print(f"❌ Erro ao aguardar resposta: {e}")
            return None
    
    def take_full_screenshot(self, filename="ai_studio_interaction.png"):
        """Captura screenshot completo da página"""
        try:
            self.page.screenshot(path=filename, full_page=True)
            print(f"📸 Screenshot completo salvo: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Erro ao capturar screenshot: {e}")
            return None
    
    def interact_with_ai(self, message):
        """Interação completa: navegar, criar chat, enviar mensagem e obter resposta"""
        try:
            print("🚀 Iniciando interação completa com AI Studio...")
            print("=" * 50)
            
            # 1. Verificar se está logado e navegar
            if not self.check_if_logged_in():
                print("❌ Não está logado. Execute 'python persistent_login.py' primeiro")
                return None
            
            # 2. Navegar para AI Studio
            if not self.navigate_to_studio():
                return None
            
            # 3. Tentar criar novo chat
            print("\n🆕 Tentando criar novo chat...")
            if self.find_and_click_new_chat():
                print("✅ Novo chat iniciado")
                
                # 4. Selecionar modelo (opcional)
                self.select_model("Gemini")
            else:
                print("⚠️ Não foi possível criar novo chat, usando página atual")
            
            # 5. Enviar mensagem
            print(f"\n💬 Enviando mensagem...")
            if not self.send_message(message):
                return None
            
            # 6. Aguardar resposta
            print("\n🤖 Aguardando resposta do AI...")
            response = self.wait_for_response(timeout=45)
            
            # 7. Capturar screenshot final
            self.take_full_screenshot("interaction_complete.png")
            
            if response:
                print("\n🎉 INTERAÇÃO CONCLUÍDA COM SUCESSO!")
                print("=" * 50)
                print(f"📝 Sua pergunta: {message}")
                print(f"🤖 Resposta do AI: {response[:200]}...")
                return response
            else:
                print("\n⚠️ Interação parcial - mensagem enviada mas resposta não capturada")
                return "Mensagem enviada, mas resposta não foi capturada automaticamente"
            
        except Exception as e:
            print(f"❌ Erro na interação: {e}")
            return None

def demo_interaction():
    """Demonstração da interação com AI Studio"""
    print("🎯 DEMO: Interação com Google AI Studio")
    print("=" * 45)
    
    ai_studio = AIStudioInteraction()
    
    try:
        # Inicializar com perfil persistente
        ai_studio.initialize_with_profile()
        
        # Mensagem de teste
        test_message = input("\n💬 Digite sua pergunta para o AI (ou pressione Enter para usar exemplo): ").strip()
        
        if not test_message:
            test_message = "Olá! Como você pode me ajudar hoje? Explique suas capacidades."
        
        print(f"\n🎯 Testando com: '{test_message}'")
        
        # Executar interação completa
        response = ai_studio.interact_with_ai(test_message)
        
        if response:
            print("\n" + "="*60)
            print("🎉 SUCESSO! Interação concluída!")
            print("📸 Screenshots salvos para verificação")
            print("🔗 Você agora pode interagir programaticamente com o AI Studio!")
        else:
            print("\n❌ Interação não concluída completamente")
            print("💡 Verifique os screenshots para debug")
        
    except Exception as e:
        print(f"\n❌ Erro na demo: {e}")
    finally:
        ai_studio.cleanup()

if __name__ == "__main__":
    demo_interaction()
