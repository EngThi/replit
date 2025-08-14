"""
Sistema melhorado de interação com Google AI Studio
Versão mais robusta para encontrar elementos da interface
"""

import time
import json
from persistent_login import PersistentGoogleLogin

class AIStudioInteractionImproved(PersistentGoogleLogin):
    def __init__(self):
        super().__init__()
        
    def debug_page_elements(self):
        """Debug: Lista elementos da página para entender a estrutura"""
        try:
            print("🔍 ANALISANDO ELEMENTOS DA PÁGINA...")
            
            # Capturar informações sobre elementos interativos
            elements_info = self.page.evaluate("""
                () => {
                    const elements = [];
                    
                    // Procurar inputs e textareas
                    document.querySelectorAll('input, textarea, [contenteditable="true"]').forEach(el => {
                        if (el.offsetParent !== null) { // Visível
                            elements.push({
                                type: 'input',
                                tag: el.tagName,
                                type_attr: el.type,
                                placeholder: el.placeholder,
                                id: el.id,
                                classes: el.className,
                                text: el.textContent.slice(0, 50)
                            });
                        }
                    });
                    
                    // Procurar botões
                    document.querySelectorAll('button, [role="button"], a').forEach(el => {
                        if (el.offsetParent !== null) {
                            elements.push({
                                type: 'button',
                                tag: el.tagName,
                                text: el.textContent.trim().slice(0, 50),
                                id: el.id,
                                classes: el.className,
                                aria_label: el.getAttribute('aria-label')
                            });
                        }
                    });
                    
                    return elements;
                }
            """)
            
            print("📋 ELEMENTOS ENCONTRADOS:")
            
            inputs = [el for el in elements_info if el['type'] == 'input']
            buttons = [el for el in elements_info if el['type'] == 'button']
            
            print(f"\n📝 INPUTS/TEXTAREAS ({len(inputs)}):")
            for i, el in enumerate(inputs[:10]):  # Mostrar apenas os primeiros 10
                print(f"  {i+1}. {el['tag']} - placeholder: '{el['placeholder']}' - classes: '{el['classes'][:50]}'")
            
            print(f"\n🔘 BOTÕES ({len(buttons)}):")
            for i, el in enumerate(buttons[:15]):  # Mostrar apenas os primeiros 15
                text = el['text'].replace('\n', ' ').strip()
                print(f"  {i+1}. '{text}' - classes: '{el['classes'][:30]}'")
            
            return elements_info
            
        except Exception as e:
            print(f"❌ Erro no debug: {e}")
            return []
    
    def find_chat_interface(self):
        """Encontra e navega para a interface de chat"""
        try:
            print("🔍 Procurando interface de chat...")
            
            # Primeiro, analisar a página atual
            current_url = self.page.url
            print(f"🔗 URL atual: {current_url}")
            
            # Se já estiver em uma página de chat, usar ela
            if "chat" in current_url.lower() or "studio" in current_url.lower():
                print("✅ Já está em interface compatível")
                return True
            
            # Procurar links para chat/prompts
            chat_links = [
                "text=Prompts",
                "text=Chat", 
                "text=New prompt",
                "text=Create",
                "a[href*='prompt']",
                "a[href*='chat']",
                "[data-testid*='prompt']",
                "[data-testid*='chat']"
            ]
            
            for link in chat_links:
                try:
                    if self.page.is_visible(link, timeout=3000):
                        print(f"✅ Encontrado link para chat: {link}")
                        self.page.click(link)
                        time.sleep(3)
                        return True
                except:
                    continue
            
            # Se não encontrou links específicos, tentar URL direta
            print("🔗 Tentando navegar diretamente para prompt...")
            try:
                self.page.goto("https://aistudio.google.com/app/prompts/new", timeout=30000)
                time.sleep(5)
                print("✅ Navegou para nova prompt")
                return True
            except:
                pass
            
            # Tentar URL alternativa
            try:
                self.page.goto("https://aistudio.google.com/app/", timeout=30000)
                time.sleep(5)
                print("✅ Navegou para app principal")
                return True
            except:
                pass
                
            return False
            
        except Exception as e:
            print(f"❌ Erro ao encontrar chat: {e}")
            return False
    
    def find_text_input_advanced(self):
        """Busca avançada por campo de texto"""
        try:
            print("🔍 Busca avançada por campo de texto...")
            
            # Aguardar página carregar
            time.sleep(3)
            
            # Estratégia 1: Procurar por atributos comuns
            input_selectors = [
                "textarea[placeholder*='message']",
                "textarea[placeholder*='prompt']",
                "textarea[placeholder*='question']",
                "textarea[placeholder*='ask']",
                "textarea[placeholder*='type']",
                "textarea[placeholder*='enter']",
                "textarea[placeholder*='write']",
                "[contenteditable='true']",
                "textarea:not([style*='display: none'])",
                "input[type='text']:not([style*='display: none'])",
                ".chat-input textarea",
                ".prompt-input textarea",
                ".message-input textarea"
            ]
            
            for selector in input_selectors:
                try:
                    if self.page.is_visible(selector, timeout=2000):
                        print(f"✅ Campo encontrado (método 1): {selector}")
                        return selector
                except:
                    continue
            
            # Estratégia 2: JavaScript para encontrar campos grandes
            text_field = self.page.evaluate("""
                () => {
                    // Procurar textareas grandes (prováveis campos de prompt)
                    const textareas = Array.from(document.querySelectorAll('textarea'));
                    for (const textarea of textareas) {
                        if (textarea.offsetParent !== null) { // Visível
                            const rect = textarea.getBoundingClientRect();
                            if (rect.height > 50 || rect.width > 200) { // Campo razoavelmente grande
                                return {
                                    selector: `textarea${textarea.id ? '#' + textarea.id : ''}${textarea.className ? '.' + textarea.className.split(' ')[0] : ''}`,
                                    placeholder: textarea.placeholder,
                                    size: `${rect.width}x${rect.height}`
                                };
                            }
                        }
                    }
                    
                    // Procurar divs editáveis
                    const editables = Array.from(document.querySelectorAll('[contenteditable="true"]'));
                    for (const editable of editables) {
                        if (editable.offsetParent !== null) {
                            const rect = editable.getBoundingClientRect();
                            if (rect.height > 30) {
                                return {
                                    selector: `[contenteditable="true"]${editable.id ? '#' + editable.id : ''}`,
                                    placeholder: editable.getAttribute('data-placeholder') || 'contenteditable',
                                    size: `${rect.width}x${rect.height}`
                                };
                            }
                        }
                    }
                    
                    return null;
                }
            """)
            
            if text_field:
                print(f"✅ Campo encontrado (método 2): {text_field['selector']} - {text_field['placeholder']} ({text_field['size']})")
                return text_field['selector']
            
            # Estratégia 3: Pegar qualquer textarea visível
            all_textareas = self.page.evaluate("""
                () => {
                    const textareas = Array.from(document.querySelectorAll('textarea, [contenteditable="true"]'));
                    return textareas.map((el, index) => ({
                        index,
                        visible: el.offsetParent !== null,
                        placeholder: el.placeholder || el.getAttribute('data-placeholder') || '',
                        tag: el.tagName,
                        id: el.id,
                        classes: el.className
                    })).filter(el => el.visible);
                }
            """)
            
            if all_textareas:
                print(f"✅ Encontrados {len(all_textareas)} campos de texto")
                # Usar o primeiro textarea visível
                first_textarea = all_textareas[0]
                if first_textarea['id']:
                    selector = f"#{first_textarea['id']}"
                elif first_textarea['classes']:
                    selector = f".{first_textarea['classes'].split()[0]}"
                else:
                    selector = "textarea"
                
                print(f"✅ Usando primeiro textarea: {selector}")
                return selector
            
            print("❌ Nenhum campo de texto encontrado")
            return None
            
        except Exception as e:
            print(f"❌ Erro na busca avançada: {e}")
            return None
    
    def send_message_improved(self, message):
        """Versão melhorada para enviar mensagem"""
        try:
            print(f"💬 Enviando: '{message}'")
            
            # Encontrar campo de texto
            text_field = self.find_text_input_advanced()
            
            if not text_field:
                print("❌ Campo de texto não encontrado após busca avançada")
                return False
            
            # Clicar no campo
            print(f"👆 Clicando no campo: {text_field}")
            self.page.click(text_field)
            time.sleep(1)
            
            # Limpar campo
            self.page.fill(text_field, "")
            time.sleep(0.5)
            
            # Digitar mensagem
            print("⌨️ Digitando mensagem...")
            self.page.type(text_field, message, delay=30)
            time.sleep(1)
            
            # Tentar enviar
            send_methods = [
                # Método 1: Procurar botão de envio
                lambda: self._try_send_button(),
                # Método 2: Enter simples
                lambda: self.page.press(text_field, "Enter"),
                # Método 3: Ctrl+Enter (comum em prompts)
                lambda: self.page.press(text_field, "Control+Enter"),
                # Método 4: Shift+Enter
                lambda: self.page.press(text_field, "Shift+Enter")
            ]
            
            for i, method in enumerate(send_methods):
                try:
                    print(f"📤 Tentativa de envio {i+1}...")
                    method()
                    time.sleep(2)
                    
                    # Verificar se mensagem foi enviada (campo limpo ou loading)
                    current_value = self.page.input_value(text_field) if "contenteditable" not in text_field else ""
                    
                    if not current_value or len(current_value.strip()) == 0:
                        print("✅ Mensagem aparenta ter sido enviada (campo limpo)")
                        return True
                    
                except Exception as e:
                    print(f"⚠️ Método {i+1} falhou: {e}")
                    continue
            
            print("⚠️ Mensagem digitada mas envio incerto")
            return True  # Assumir sucesso parcial
            
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem: {e}")
            return False
    
    def _try_send_button(self):
        """Tenta encontrar e clicar botão de envio"""
        send_selectors = [
            "button[type='submit']",
            "button:has-text('Send')",
            "button:has-text('Run')",
            "button:has-text('Generate')",
            "button:has-text('Submit')",
            "[aria-label*='send']",
            "[aria-label*='submit']",
            "[aria-label*='run']",
            ".send-button",
            ".submit-button",
            ".run-button"
        ]
        
        for selector in send_selectors:
            try:
                if self.page.is_visible(selector, timeout=1000):
                    self.page.click(selector)
                    return True
            except:
                continue
        
        return False
    
    def wait_for_response_improved(self, timeout=45):
        """Aguarda resposta com detecção melhorada"""
        try:
            print("⏳ Aguardando resposta...")
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                # Procurar indicadores de loading
                loading_indicators = [
                    ".loading",
                    ".spinner",
                    "[aria-label*='loading']",
                    "text=Generating",
                    "text=Loading"
                ]
                
                is_loading = False
                for indicator in loading_indicators:
                    try:
                        if self.page.is_visible(indicator, timeout=500):
                            is_loading = True
                            break
                    except:
                        continue
                
                if is_loading:
                    print("🔄 Detectado loading...")
                    time.sleep(2)
                    continue
                
                # Procurar resposta
                response_text = self.page.evaluate("""
                    () => {
                        // Procurar por texto que aparenta ser resposta
                        const candidates = Array.from(document.querySelectorAll('div, p, span, pre'));
                        
                        for (const el of candidates) {
                            const text = el.textContent.trim();
                            
                            // Ignorar elementos muito pequenos ou que são menus/UI
                            if (text.length > 50 && text.length < 5000) {
                                // Verificar se não é texto de interface
                                if (!text.includes('Google AI Studio') && 
                                    !text.includes('Settings') && 
                                    !text.includes('Menu') &&
                                    !text.includes('API key')) {
                                    return text;
                                }
                            }
                        }
                        
                        return null;
                    }
                """)
                
                if response_text and len(response_text) > 20:
                    print(f"✅ Possível resposta encontrada ({len(response_text)} chars)")
                    return response_text
                
                time.sleep(1)
            
            print("⏰ Timeout na espera da resposta")
            
            # Capturar qualquer texto longo na página como fallback
            fallback_text = self.page.evaluate("""
                () => {
                    const text = document.body.textContent;
                    return text.length > 100 ? text.slice(-500) : text; // Últimos 500 chars
                }
            """)
            
            return fallback_text
            
        except Exception as e:
            print(f"❌ Erro ao aguardar resposta: {e}")
            return None
    
    def full_interaction(self, message):
        """Interação completa melhorada"""
        try:
            print("🚀 INTERAÇÃO COMPLETA COM AI STUDIO")
            print("=" * 50)
            
            # 1. Verificar login
            if not self.check_if_logged_in():
                print("❌ Faça login primeiro: python persistent_login.py")
                return None
            
            # 2. Navegar para interface de chat
            if not self.find_chat_interface():
                print("⚠️ Usando página atual")
            
            # 3. Debug da página
            self.debug_page_elements()
            
            # 4. Capturar screenshot antes
            self.page.screenshot(path="before_interaction.png")
            print("📸 Screenshot 'antes': before_interaction.png")
            
            # 5. Enviar mensagem
            if not self.send_message_improved(message):
                print("❌ Falha ao enviar mensagem")
                return None
            
            # 6. Capturar screenshot após envio
            self.page.screenshot(path="after_send.png")
            print("📸 Screenshot 'após envio': after_send.png")
            
            # 7. Aguardar resposta
            response = self.wait_for_response_improved()
            
            # 8. Screenshot final
            self.page.screenshot(path="final_interaction.png")
            print("📸 Screenshot final: final_interaction.png")
            
            if response:
                print("\n🎉 INTERAÇÃO CONCLUÍDA!")
                print("=" * 30)
                print(f"📤 Sua mensagem: {message}")
                print(f"📥 Resposta: {response[:300]}...")
                return response
            else:
                print("\n⚠️ Interação parcial")
                return "Mensagem enviada - verifique screenshots"
                
        except Exception as e:
            print(f"❌ Erro na interação: {e}")
            return None

def test_improved_interaction():
    """Teste da versão melhorada"""
    print("🧪 TESTE DE INTERAÇÃO MELHORADA")
    print("=" * 40)
    
    ai = AIStudioInteractionImproved()
    
    try:
        ai.initialize_with_profile()
        
        message = input("\n💬 Sua pergunta (Enter para exemplo): ").strip()
        if not message:
            message = "Qual é a capital do Brasil?"
        
        result = ai.full_interaction(message)
        
        if result:
            print(f"\n✅ Resultado: {result[:200]}...")
        else:
            print("\n❌ Sem resultado")
            
    finally:
        ai.cleanup()

if __name__ == "__main__":
    test_improved_interaction()
