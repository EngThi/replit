"""
Sistema de Interação com Google AI Studio
Permite navegar, criar chats e enviar mensagens após login bem-sucedido
"""

import time
import json
import os
import re
from datetime import datetime
from ai_studio_login_2fa import AIStudioLogin2FA

class AIStudioAutomator(AIStudioLogin2FA):
    def __init__(self, headless=True):
        """
        Inicializa sistema de interação com AI Studio
        Herda funcionalidades de login do AIStudioLogin2FA
        """
        super().__init__(headless)
        self.current_chat_url = None
        self.conversation_history = []
        self.interactions_dir = "interactions"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = f"{self.interactions_dir}/logs/log_{timestamp}.json"
        self.ensure_interaction_dirs()
        
    def ensure_interaction_dirs(self):
        """Cria e limpa os diretórios de interação."""
        screenshots_dir = f"{self.interactions_dir}/screenshots"
        logs_dir = f"{self.interactions_dir}/logs"
        conversations_dir = f"{self.interactions_dir}/conversations"

        os.makedirs(self.interactions_dir, exist_ok=True)
        os.makedirs(screenshots_dir, exist_ok=True)
        os.makedirs(logs_dir, exist_ok=True)
        os.makedirs(conversations_dir, exist_ok=True)

        # Limpar arquivos antigos, mantendo os 3 mais recentes
        self._cleanup_old_files(screenshots_dir, ".png", 3)
        self._cleanup_old_files(logs_dir, ".json", 3)
        self._cleanup_old_files(conversations_dir, ".json", 3)

    def _cleanup_old_files(self, directory, file_extension, keep_count):
        """Limpa arquivos antigos em um diretório, mantendo os mais recentes."""
        try:
            if not os.path.isdir(directory):
                return

            files = [f for f in os.listdir(directory) if f.endswith(file_extension)]

            def get_timestamp(filename):
                match = re.search(r'(\d{8}_\d{6})', filename)
                return match.group(1) if match else "00000000_000000"

            files.sort(key=get_timestamp, reverse=True)

            if len(files) > keep_count:
                files_to_delete = files[keep_count:]
                for f in files_to_delete:
                    try:
                        os.remove(os.path.join(directory, f))
                    except OSError:
                        pass
        except Exception:
            pass
    
    def save_interaction_log(self, action, details=None):
        """Salva log de interações"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action': action,
                'details': details or {},
                'url': self.page.url if self.page else None
            }
            
            log_file = self.log_file
            
            # Carregar logs existentes
            logs = []
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            
            logs.append(log_entry)
            
            # Manter apenas últimas 100 interações
            if len(logs) > 100:
                logs = logs[-100:]
            
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
                
            print(f"📝 Log salvo: {action}")
            
        except Exception as e:
            print(f"⚠️ Erro ao salvar log: {e}")
    
    def take_interaction_screenshot(self, name):
        """Captura screenshot da interação"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"{self.interactions_dir}/screenshots/{name}_{timestamp}.png"
            
            self.page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Screenshot: {screenshot_path}")
            return screenshot_path
            
        except Exception as e:
            print(f"❌ Erro ao capturar screenshot: {e}")
            return None
    
    def navigate_to_studio_home(self):
        """Navega para página inicial do AI Studio"""
        try:
            print("🏠 Navegando para AI Studio...")
            
            self.page.goto("https://aistudio.google.com/", timeout=30000)
            self.page.wait_for_load_state('networkidle')
            time.sleep(3)
            
            # Verificar se carregou corretamente
            current_url = self.page.url
            title = self.page.title()
            
            print(f"🔗 URL: {current_url}")
            print(f"📄 Título: {title}")
            
            # Screenshot da página inicial
            self.take_interaction_screenshot("home_page")
            
            self.save_interaction_log("navigate_home", {
                "url": current_url,
                "title": title
            })
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao navegar: {e}")
            return False
    
    def find_new_chat_button(self):
        """Encontra botão para criar novo chat"""
        try:
            print("🔍 Procurando botão 'Novo Chat'...")
            
            # Aguardar página carregar completamente
            time.sleep(3)
            
            # Possíveis seletores para novo chat
            new_chat_selectors = [
                # Textos específicos de chat (mais específicos primeiro)
                "text=New chat",
                "text=Novo chat", 
                "text=Create new chat",
                "text=Criar novo chat",
                "text=Start new conversation",
                "text=Nova conversa",
                
                # Botões mais genéricos
                "text=Create new",
                "text=Criar novo",
                "text=Start new",
                
                # Seletores por atributos
                "[data-testid*='new-chat']",
                "[data-testid*='create']",
                "[aria-label*='new chat']",
                "[aria-label*='create']",
                "[aria-label*='novo']",
                
                # Seletores por classes comuns
                ".new-chat-button",
                ".create-button",
                ".start-button",
                
                # Botões com texto específico
                "button:has-text('New')",
                "button:has-text('Create')",
                "button:has-text('Novo')",
                "button:has-text('Criar')",
                
                # Links com texto
                "a:has-text('New')",
                "a:has-text('Create')",
                "a:has-text('Novo')",
                
                # Elementos com role button
                "[role='button']:has-text('New')",
                "[role='button']:has-text('Create')",
                "[role='button']:has-text('Novo')"
            ]
            
            found_button = None
            
            for selector in new_chat_selectors:
                try:
                    if self.page.is_visible(selector, timeout=2000):
                        print(f"✅ Botão encontrado: {selector}")
                        found_button = selector
                        break
                except:
                    continue
            
            if not found_button:
                # Busca mais avançada via JavaScript
                print("🔧 Buscando via JavaScript...")
                
                found_button = self.page.evaluate("""
                    () => {
                        const searchTerms = ['new', 'create', 'start', 'novo', 'criar', 'começar', 'iniciar'];
                        const elements = Array.from(document.querySelectorAll('button, a, [role="button"], div[onclick], .clickable'));
                        
                        for (const element of elements) {
                            if (!element.offsetParent) continue; // Elemento não visível
                            
                            const text = element.textContent.toLowerCase().trim();
                            const ariaLabel = (element.getAttribute('aria-label') || '').toLowerCase();
                            const title = (element.getAttribute('title') || '').toLowerCase();
                            
                            const allText = text + ' ' + ariaLabel + ' ' + title;
                            
                            if (searchTerms.some(term => allText.includes(term))) {
                                // Retornar informações do elemento
                                const rect = element.getBoundingClientRect();
                                return {
                                    text: element.textContent.trim(),
                                    tag: element.tagName,
                                    id: element.id,
                                    className: element.className,
                                    ariaLabel: element.getAttribute('aria-label'),
                                    x: rect.x,
                                    y: rect.y,
                                    selector: element.id ? `#${element.id}` : 
                                             element.className ? `.${element.className.split(' ')[0]}` :
                                             element.tagName.toLowerCase()
                                };
                            }
                        }
                        return null;
                    }
                """)
                
                if found_button:
                    print(f"✅ Botão encontrado via JS: {found_button['text']}")
                    # Usar seletor mais específico
                    if found_button['id']:
                        found_button = f"#{found_button['id']}"
                    elif found_button['className']:
                        found_button = f".{found_button['className'].split()[0]}"
                    else:
                        # Usar coordenadas como fallback
                        print(f"🎯 Clicando em coordenadas: ({found_button['x']}, {found_button['y']})")
                        self.page.click(f"{found_button['x']},{found_button['y']}")
                        time.sleep(3)
                        return True
            
            if found_button:
                return found_button
            else:
                print("❌ Nenhum botão de novo chat encontrado")
                return None
                
        except Exception as e:
            print(f"❌ Erro ao procurar botão: {e}")
            return None
    
    def create_new_chat(self):
        """Cria um novo chat de forma robusta, tentando várias URLs e botões."""
        try:
            print("🆕 Criando novo chat...")
            
            chat_url = self.try_advanced_urls()
            
            if chat_url:
                print(f"✅ Chat encontrado ou criado em: {chat_url}")
                self.current_chat_url = chat_url
                self.take_interaction_screenshot("chat_page_found")
                return True
            else:
                print("❌ Não foi possível encontrar ou criar um novo chat.")
                return False
        except Exception as e:
            print(f"❌ Erro ao criar novo chat: {e}")
            return False
    
    def find_message_input(self):
        """Encontra campo de entrada de mensagem"""
        try:
            print("🔍 Procurando campo de mensagem...")
            
            # Seletores para campo de texto
            input_selectors = [
                # Seletores específicos do AI Studio
                "textarea[placeholder*='message']",
                "textarea[placeholder*='pergunt']",
                "textarea[placeholder*='question']",
                "textarea[placeholder*='prompt']",
                "textarea[placeholder*='type']",
                "textarea[placeholder*='enter']",
                "textarea[placeholder*='ask']",
                
                # Seletores genéricos
                "textarea",
                "input[type='text']",
                "[contenteditable='true']",
                
                # Por classes comuns
                ".chat-input",
                ".message-input",
                ".prompt-input",
                ".text-input",
                
                # Por atributos
                "[data-testid*='input']",
                "[data-testid*='message']",
                "[data-testid*='prompt']",
                "[role='textbox']",
                "[aria-label*='message']",
                "[aria-label*='prompt']",
                "[aria-label*='input']"
            ]
            
            found_input = None
            
            for selector in input_selectors:
                try:
                    if self.page.is_visible(selector, timeout=2000):
                        print(f"✅ Campo encontrado: {selector}")
                        found_input = selector
                        break
                except:
                    continue
            
            if not found_input:
                # Busca via JavaScript
                print("🔧 Buscando campo via JavaScript...")
                
                input_info = self.page.evaluate("""
                    () => {
                        const inputs = Array.from(document.querySelectorAll('textarea, input[type="text"], [contenteditable="true"]'));
                        
                        for (const input of inputs) {
                            if (input.offsetParent !== null) { // Elemento visível
                                const rect = input.getBoundingClientRect();
                                if (rect.width > 50 && rect.height > 20) { // Tamanho razoável
                                    return {
                                        tagName: input.tagName,
                                        type: input.type,
                                        placeholder: input.placeholder,
                                        id: input.id,
                                        className: input.className,
                                        ariaLabel: input.getAttribute('aria-label'),
                                        selector: input.id ? `#${input.id}` :
                                                 input.className ? `.${input.className.split(' ')[0]}` :
                                                 input.tagName.toLowerCase()
                                    };
                                }
                            }
                        }
                        return null;
                    }
                """)
                
                if input_info:
                    print(f"✅ Campo encontrado via JS: {input_info['tagName']}")
                    found_input = input_info['selector']
            
            return found_input
            
        except Exception as e:
            print(f"❌ Erro ao procurar campo: {e}")
            return None
    
    def send_message(self, message):
        """Envia uma mensagem no chat"""
        try:
            print(f"💬 Enviando mensagem: '{message[:50]}...'")
            
            # Encontrar campo de entrada
            input_field = self.find_message_input()
            
            if not input_field:
                print("❌ Campo de mensagem não encontrado")
                self.take_interaction_screenshot("send_message_error_no_field")
                return False
            
            # Clicar no campo para focar
            self.page.click(input_field)
            time.sleep(0.5)
            
            # Limpar campo se houver texto
            self.page.evaluate(f"""
                () => {{
                    const field = document.querySelector('{input_field}');
                    if (field) {{
                        field.value = '';
                        if (field.textContent !== undefined) field.textContent = '';
                    }}
                }}
            """)
            
            time.sleep(0.3)
            
            # Digitar mensagem de forma humana (com delays)
            print("⌨️ Digitando mensagem...")
            for i, char in enumerate(message):
                self.page.type(input_field, char, delay=50 + (i % 3) * 20)  # Variação no delay
            
            time.sleep(1)
            
            # Screenshot antes de enviar
            self.take_interaction_screenshot("before_send")
            
            # Procurar botão de envio
            send_selectors = [
                # Textos comuns
                "text=Send",
                "text=Enviar",
                "text=Submit",
                "text=Go",
                
                # Botões por tipo
                "button[type='submit']",
                
                # Por atributos
                "[aria-label*='send']",
                "[aria-label*='enviar']",
                "[aria-label*='submit']",
                "[data-testid*='send']",
                "[data-testid*='submit']",
                
                # Classes comuns
                ".send-button",
                ".submit-button",
                
                # Botões com ícones (comum em chats)
                "button svg",
                "button [role='img']",
                "[role='button'] svg",
                
                # Botões próximos ao input
                f"{input_field} + button",
                f"{input_field} ~ button"
            ]
            
            sent = False
            for selector in send_selectors:
                try:
                    if self.page.is_visible(selector, timeout=2000):
                        print(f"📤 Enviando via: {selector}")
                        self.page.click(selector)
                        sent = True
                        break
                except:
                    continue
            
            if not sent:
                # Tentar Enter
                print("⌨️ Tentando enviar com Enter...")
                self.page.press(input_field, "Enter")
                sent = True
            
            if not sent:
                # Tentar Ctrl+Enter (comum em algumas interfaces)
                print("⌨️ Tentando enviar com Ctrl+Enter...")
                self.page.press(input_field, "Control+Enter")
                sent = True
            
            if sent:
                print("✅ Mensagem enviada!")
                time.sleep(2)  # Aguardar processamento
                
                # Screenshot após envio
                self.take_interaction_screenshot("after_send")
                
                # Salvar no histórico
                self.conversation_history.append({
                    'type': 'user_message',
                    'content': message,
                    'timestamp': datetime.now().isoformat()
                })
                
                self.save_interaction_log("send_message", {
                    "message": message[:100],
                    "input_field": input_field,
                    "success": True
                })
                
                return True
            else:
                print("❌ Não foi possível enviar mensagem")
                self.take_interaction_screenshot("send_failed")
                return False
            
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem: {e}")
            self.take_interaction_screenshot("send_message_error")
            return False
    
    def wait_for_ai_response(self, timeout=60):
        """Aguarda e captura resposta do AI"""
        try:
            print("🤖 Aguardando resposta do AI...")
            
            start_time = time.time()
            last_screenshot_time = 0
            
            while time.time() - start_time < timeout:
                current_time = time.time()
                
                # Capturar screenshot periodicamente durante a espera
                if current_time - last_screenshot_time > 10:  # A cada 10 segundos
                    self.take_interaction_screenshot(f"waiting_response_{int(current_time - start_time)}s")
                    last_screenshot_time = current_time
                
                # Procurar indicadores de resposta
                response_indicators = [
                    # Elementos comuns de resposta
                    ".ai-response",
                    ".assistant-message", 
                    ".bot-message",
                    ".response-content",
                    ".ai-message",
                    
                    # Por atributos
                    "[data-testid*='response']",
                    "[data-testid*='ai']",
                    "[data-testid*='assistant']",
                    "[role='article']",
                    
                    # Mensagens em geral (pegar a última)
                    ".message:last-child",
                    ".chat-message:last-child"
                ]
                
                for indicator in response_indicators:
                    try:
                        if self.page.is_visible(indicator, timeout=1000):
                            # Aguardar um pouco mais para garantir que a resposta terminou
                            time.sleep(3)
                            
                            # Verificar se há indicadores de que ainda está digitando
                            typing_indicators = [
                                ".typing",
                                ".loading",
                                ".generating",
                                "[data-testid*='typing']",
                                "[data-testid*='loading']"
                            ]
                            
                            still_typing = False
                            for typing_ind in typing_indicators:
                                try:
                                    if self.page.is_visible(typing_ind, timeout=500):
                                        still_typing = True
                                        break
                                except:
                                    continue
                            
                            if still_typing:
                                print("⏳ AI ainda está digitando...")
                                time.sleep(5)
                                continue
                            
                            # Capturar texto da resposta
                            response_text = self.page.evaluate(f"""
                                () => {{
                                    const element = document.querySelector('{indicator}');
                                    if (element) {{
                                        return element.textContent.trim();
                                    }}
                                    return '';
                                }}
                            """)
                            
                            if response_text and len(response_text) > 10:
                                print(f"✅ Resposta recebida ({len(response_text)} caracteres)")
                                print(f"📝 Início: {response_text[:100]}...")
                                
                                # Screenshot da resposta completa
                                self.take_interaction_screenshot("ai_response_received")
                                
                                # Salvar no histórico
                                self.conversation_history.append({
                                    'type': 'ai_response',
                                    'content': response_text,
                                    'timestamp': datetime.now().isoformat()
                                })
                                
                                self.save_interaction_log("receive_response", {
                                    "response_length": len(response_text),
                                    "response_preview": response_text[:200]
                                })
                                
                                return response_text
                    except:
                        continue
                
                time.sleep(2)  # Aguardar antes da próxima verificação
            
            print("⏰ Timeout aguardando resposta")
            self.take_interaction_screenshot("response_timeout")
            return None
            
        except Exception as e:
            print(f"❌ Erro ao aguardar resposta: {e}")
            return None
    
    def save_conversation(self, filename=None):
        """Salva conversa atual em arquivo"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"conversation_{timestamp}.json"
            
            conversation_file = f"{self.interactions_dir}/conversations/{filename}"
            
            conversation_data = {
                'timestamp': datetime.now().isoformat(),
                'chat_url': self.current_chat_url,
                'history': self.conversation_history,
                'total_messages': len([h for h in self.conversation_history if h['type'] == 'user_message']),
                'total_responses': len([h for h in self.conversation_history if h['type'] == 'ai_response'])
            }
            
            with open(conversation_file, 'w', encoding='utf-8') as f:
                json.dump(conversation_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Conversa salva: {conversation_file}")
            return conversation_file
            
        except Exception as e:
            print(f"❌ Erro ao salvar conversa: {e}")
            return None
    
    def click_get_started_button(self):
        """Clica no botão 'Get started' na página welcome"""
        try:
            print("🎯 Procurando botão 'Get started'...")

            # Aguardar a página carregar
            time.sleep(3)

            # Diferentes seletores possíveis para o botão Get started
            get_started_selectors = [
                "text=Get started",
                "button:has-text('Get started')",
                "a:has-text('Get started')",
                "[data-testid*='get-started']",
                ".get-started",
                "#get-started",
                "button[aria-label*='Get started']",
                "a[aria-label*='Get started']"
            ]

            for selector in get_started_selectors:
                try:
                    print(f"🔍 Tentando seletor: {selector}")

                    # Verificar se elemento existe e está visível
                    if self.page.is_visible(selector, timeout=2000):
                        print(f"✅ Botão encontrado: {selector}")

                        # Rolar até o elemento
                        self.page.evaluate(f'document.querySelector("{selector}").scrollIntoView()')
                        time.sleep(1)

                        # Clicar
                        self.page.click(selector)
                        print("🖱️ Clique realizado!")

                        # Aguardar navegação
                        time.sleep(5)

                        new_url = self.page.url
                        print(f"🔗 Nova URL: {new_url}")

                        # Verificar se saiu da página welcome
                        if "welcome" not in new_url and "accounts.google.com" not in new_url:
                            print("✅ Navegação bem-sucedida!")
                            return True
                        else:
                            print("⚠️ Ainda na welcome ou redirecionado para login")

                except Exception as e:
                    print(f"❌ Erro com seletor {selector}: {e}")
                    continue

            # Busca mais ampla via JavaScript
            print("🔍 Busca JavaScript por 'Get started'...")

            js_result = self.page.evaluate("""
                () => {
                    const elements = document.querySelectorAll('*');

                    for (const el of elements) {
                        const text = el.textContent.trim();
                        const isClickable = el.tagName === 'BUTTON' || el.tagName === 'A' ||
                                          el.onclick || el.href || el.getAttribute('role') === 'button';

                        if (text.toLowerCase().includes('get started') && isClickable && el.offsetParent) {
                            el.click();
                            return {
                                success: true,
                                text: text,
                                tag: el.tagName
                            };
                        }
                    }

                    return {success: false};
                }
            """)

            if js_result['success']:
                print(f"✅ Clicado via JavaScript: {js_result['tag']} - '{js_result['text']}'")
                time.sleep(5)

                new_url = self.page.url
                print(f"🔗 URL após JS: {new_url}")

                if "welcome" not in new_url and "accounts.google.com" not in new_url:
                    return True

            print("❌ Botão 'Get started' não encontrado")
            return False

        except Exception as e:
            print(f"❌ Erro clicando em Get started: {e}")
            return False

    def try_advanced_urls(self):
        """Tenta URLs mais avançadas e específicas"""
        try:
            print("\n🎯 TENTANDO URLS AVANÇADAS")
            print("=" * 30)

            # Primeiro, verificar se estamos na welcome e clicar Get started
            current_url = self.page.url
            if "welcome" in current_url:
                print("📍 Ainda na welcome - tentando Get started novamente...")
                if self.click_get_started_button():
                    time.sleep(5)
                    current_url = self.page.url
                    print(f"🔗 Nova URL após Get started: {current_url}")

                    # Verificar se agora temos acesso a chat
                    input_check = self.page.evaluate("""
                        () => {
                            const inputs = document.querySelectorAll('textarea, input[type="text"], [contenteditable="true"]');
                            for (const input of inputs) {
                                if (input.offsetParent) {
                                    const rect = input.getBoundingClientRect();
                                    if (rect.width > 200 && rect.height > 30) {
                                        return {
                                            found: true,
                                            tag: input.tagName,
                                            placeholder: input.placeholder || '',
                                            width: rect.width,
                                            height: rect.height
                                        };
                                    }
                                }
                            }
                            return {found: false};
                        }
                    """)

                    if input_check['found']:
                        print(f"✅ SUCESSO! Interface de chat encontrada após Get started!")
                        print(f"   Campo: {input_check['tag']} - {input_check['width']}x{input_check['height']}")
                        return current_url

            # URLs mais específicas para testar
            urls_to_test = [
                "https://aistudio.google.com/app/prompts/new",
                "https://makersuite.google.com/app/prompts/new",
                "https://aistudio.google.com/prompt/new",
                "https://aistudio.google.com/create",
                "https://aistudio.google.com/workspace/new",
                "https://bard.google.com/",  # Alternativa
                "https://gemini.google.com/app"  # Nova interface Gemini
            ]

            for url in urls_to_test:
                print(f"\n🔗 Testando: {url}")

                try:
                    self.page.goto(url, timeout=15000)
                    time.sleep(4)

                    final_url = self.page.url
                    print(f"   Final: {final_url}")

                    # Se não redirecionou para login
                    if "accounts.google.com" not in final_url:
                        # Verificar se tem campo de input
                        input_check = self.page.evaluate("""
                            () => {
                                const inputs = document.querySelectorAll('textarea, input[type="text"], [contenteditable="true"]');
                                let found = null;

                                for (const input of inputs) {
                                    if (input.offsetParent) {
                                        const rect = input.getBoundingClientRect();
                                        if (rect.width > 200 && rect.height > 30) {
                                            found = {
                                                tag: input.tagName,
                                                placeholder: input.placeholder || '',
                                                className: Array.from(input.classList).join(' ').slice(0, 50),
                                                width: rect.width,
                                                height: rect.height
                                            };
                                            break;
                                        }
                                    }
                                }

                                return found;
                            }
                        """)

                        if input_check:
                            print(f"   ✅ SUCESSO! Campo encontrado:")
                            print(f"      {input_check['tag']} - {input_check['width']}x{input_check['height']}")
                            print(f"      Placeholder: '{input_check['placeholder']}'")

                            return final_url
                        else:
                            print(f"   ⚠️ Página carregou mas sem campo de input adequado")
                    else:
                        print(f"   ❌ Redirecionado para login")

                except Exception as e:
                    print(f"   ❌ Erro: {e}")
                    continue

            return None

        except Exception as e:
            print(f"❌ Erro nas URLs avançadas: {e}")
            return None

    def complete_interaction(self, message):
        """Executa interação completa: login + navegação + envio + resposta"""
        try:
            print("🚀 INTERAÇÃO COMPLETA COM AI STUDIO")
            print("=" * 45)
            
            # 1. Verificar/fazer login
            self.initialize_browser()
            
            if not self.check_if_logged_in():
                print("🔑 Fazendo login...")
                if not self.quick_login():
                    print("❌ Login falhou")
                    return None
            
            print("✅ Login confirmado!")
            
            # 2. Navegar para AI Studio
            if not self.navigate_to_studio_home():
                print("❌ Falha ao navegar para AI Studio")
                return None
            
            # 3. Criar novo chat
            if not self.create_new_chat():
                print("⚠️ Falha ao criar novo chat, tentando usar página atual")
            
            # 4. Enviar mensagem
            if not self.send_message(message):
                print("❌ Falha ao enviar mensagem")
                return None
            
            # 5. Aguardar resposta
            response = self.wait_for_ai_response(timeout=90)
            
            if response:
                # 6. Salvar conversa
                conversation_file = self.save_conversation()
                
                print("\n🎉 INTERAÇÃO CONCLUÍDA COM SUCESSO!")
                print("=" * 45)
                print(f"💬 Sua pergunta: {message}")
                print(f"🤖 Resposta ({len(response)} chars): {response[:200]}...")
                print(f"💾 Conversa salva: {conversation_file}")
                
                return {
                    'question': message,
                    'response': response,
                    'conversation_file': conversation_file,
                    'chat_url': self.current_chat_url
                }
            else:
                print("⚠️ Mensagem enviada mas resposta não foi capturada")
                return {
                    'question': message,
                    'response': None,
                    'chat_url': self.current_chat_url
                }
                
        except Exception as e:
            print(f"❌ Erro na interação completa: {e}")
            self.take_interaction_screenshot("complete_interaction_error")
            return None

def demo_interaction():
    """Demonstração de interação completa"""
    print("🎯 DEMO: Interação Completa com AI Studio")
    print("=" * 45)
    
    ai_interaction = AIStudioInteraction(headless=True)
    
    try:
        # Solicitar mensagem do usuário
        message = input("\n💬 Digite sua pergunta para o AI (ou Enter para exemplo): ").strip()
        
        if not message:
            message = "Olá! Explique como você pode me ajudar com programação Python. Seja específico sobre suas capacidades."
        
        print(f"\n🎯 Pergunta: '{message}'")
        
        # Executar interação completa
        result = ai_interaction.complete_interaction(message)
        
        if result and result['response']:
            print("\n" + "="*60)
            print("🎉 SUCESSO COMPLETO!")
            print(f"📁 Arquivos salvos em: {ai_interaction.interactions_dir}")
            print("🔗 Próximas interações serão mais rápidas!")
        else:
            print("\n❌ Interação não foi completamente concluída")
            print("💡 Verifique os screenshots e logs")
        
    except KeyboardInterrupt:
        print("\n⚠️ Interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro na demo: {e}")
    finally:
        ai_interaction.cleanup()

if __name__ == "__main__":
    demo_interaction()
