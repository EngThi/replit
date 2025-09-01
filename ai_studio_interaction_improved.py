"""
Sistema de Interação com Google AI Studio (Versão Melhorada)
Foca em URLs diretas e detecção robusta de elementos
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
        """Acessa chat via URLs diretas com login automático se necessário"""
        try:
            print("🎯 Tentando acessar chat diretamente...")
            
            # URL específica que sabemos que funciona
            target_url = "https://aistudio.google.com/u/3/prompts/new_chat"
            
            print(f"🔗 Tentando: {target_url}")
            
            self.page.goto(target_url, timeout=20000)
            time.sleep(5)  # Aguardar carregamento
            
            final_url = self.page.url
            print(f"🔗 URL final: {final_url}")
            
            # Se foi redirecionado para login, fazer login na mesma sessão
            if "accounts.google.com" in final_url:
                print("🔑 Redirecionado para login - fazendo login...")
                
                # Fazer login usando a mesma página atual
                if self.do_login_on_current_page():
                    print("✅ Login realizado na página atual")
                    
                    # Tentar novamente após login
                    print(f"🔄 Tentando acessar chat novamente...")
                    self.page.goto(target_url, timeout=20000)
                    time.sleep(5)
                    
                    final_url = self.page.url
                    print(f"🔗 URL final após login: {final_url}")
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
                    print(f"⚠️ URL carregou mas sem campo de input")
                    self.take_screenshot("no_input_found")
            else:
                print(f"⚠️ Ainda redirecionado para login após tentativa")
            
            return False
            
        except Exception as e:
            print(f"❌ Erro geral: {e}")
            return False
    
    def do_login_on_current_page(self):
        """Faz login na página atual (sem inicializar novo navegador)"""
        try:
            print("🔑 Fazendo login na página atual...")
            
            # Verificar se estamos na página de login do Google
            current_url = self.page.url
            if "accounts.google.com" not in current_url:
                print("❌ Não estamos na página de login")
                return False
            
            # Aguardar página carregar completamente
            time.sleep(3)
            
            # Verificar que tipo de página de login temos
            page_type = self.page.evaluate("""
                () => {
                    const body = document.body.textContent.toLowerCase();
                    if (body.includes('choose an account') || body.includes('escolher uma conta')) {
                        return 'account_chooser';
                    } else if (document.querySelector('input[type="email"]')) {
                        return 'email_input';
                    } else if (document.querySelector('input[type="password"]')) {
                        return 'password_input';
                    }
                    return 'unknown';
                }
            """)
            
            print(f"🔍 Tipo de página detectado: {page_type}")
            
            # Se é página de escolha de conta, tentar clicar na conta
            if page_type == 'account_chooser':
                print("👥 Página de escolha de conta detectada...")
                
                # Procurar pela conta configurada
                email = self.credentials_manager.get_email()
                if email:
                    # Tentar encontrar e clicar na conta
                    account_clicked = self.page.evaluate(f"""
                        () => {{
                            const email = '{email}';
                            // Procurar por elementos que contenham o email
                            const elements = document.querySelectorAll('*');
                            for (const el of elements) {{
                                if (el.textContent.includes(email) && el.offsetParent) {{
                                    el.click();
                                    return true;
                                }}
                            }}
                            
                            // Fallback: procurar por qualquer elemento clicável que pareça uma conta
                            const clickableElements = document.querySelectorAll('[data-identifier], [role="button"], div[jsaction]');
                            for (const el of clickableElements) {{
                                const text = el.textContent.toLowerCase();
                                if (text.includes('@') || text.includes('conta') || text.includes('account')) {{
                                    el.click();
                                    return true;
                                }}
                            }}
                            
                            return false;
                        }}
                    """)
                    
                    if account_clicked:
                        print("✅ Conta selecionada")
                        time.sleep(3)
                        
                        # Verificar se precisa de senha
                        has_password_field = self.page.evaluate("""
                            () => {
                                return document.querySelector('input[type="password"]') !== null;
                            }
                        """)
                        
                        if has_password_field:
                            print("🔒 Campo de senha apareceu...")
                            return self.fill_password_and_login()
                        else:
                            # Verificar se já logou
                            time.sleep(3)
                            final_url = self.page.url
                            if "accounts.google.com" not in final_url:
                                print("✅ Login concluído sem senha adicional!")
                                return True
                    else:
                        print("⚠️ Não foi possível selecionar conta automaticamente")
                
            # Se tem campo de email, preencher
            elif page_type == 'email_input':
                return self.fill_email_and_continue()
            
            # Se tem campo de senha, preencher
            elif page_type == 'password_input':
                return self.fill_password_and_login()
            
            # Página desconhecida - aguardar manual
            else:
                print("⚠️ Tipo de página de login não reconhecido")
                self.take_screenshot("unknown_login_page")
                print("📸 Screenshot salvo para análise")
                print("⏳ Aguardando 30 segundos para login manual...")
                time.sleep(30)
                
                final_url = self.page.url
                if "accounts.google.com" not in final_url:
                    print("✅ Login manual concluído!")
                    return True
                else:
                    print("⚠️ Ainda na página de login")
                    return False
                
        except Exception as e:
            print(f"❌ Erro no login: {e}")
            return False
    
    def fill_email_and_continue(self):
        """Preenche email e continua"""
        try:
                # Verificar se temos credenciais configuradas
                email = self.credentials_manager.get_email()
                password = self.credentials_manager.get_password()
                
                if email and password:
                    print(f"✅ Usando credenciais configuradas para: {email}")
                    
                    # Preencher email
                    print("📧 Preenchendo email...")
                    self.page.fill('input[type="email"]', email)
                    time.sleep(1)
                    
                    # Clicar em Next
                    print("➡️ Clicando em Avançar...")
                    time.sleep(2)  # Aguardar um pouco mais
                    
                    # Tentar múltiplos seletores para o botão Next
                    next_selectors = [
                        '#identifierNext',
                        'button:has-text("Next")',
                        'button:has-text("Avançar")',
                        'button:has-text("Próxima")',
                        'button[id*="next"]',
                        'button[id*="Next"]',
                        'input[type="submit"]',
                        'button[type="submit"]',
                        '.VfPpkd-LgbsSe'  # Classe comum dos botões Google
                    ]
                    
                    button_clicked = False
                    for selector in next_selectors:
                        try:
                            # Verificar se botão existe e está visível
                            button_exists = self.page.evaluate(f"""
                                () => {{
                                    const btn = document.querySelector('{selector}');
                                    return btn && btn.offsetParent !== null;
                                }}
                            """)
                            
                            if button_exists:
                                print(f"   🎯 Usando seletor: {selector}")
                                self.page.click(selector)
                                button_clicked = True
                                break
                        except Exception as e:
                            print(f"   ⚠️ Seletor {selector} falhou: {str(e)[:50]}...")
                            continue
                    
                    if not button_clicked:
                        print("❌ Nenhum botão Avançar encontrado")
                        
                        # Tentar Enter como fallback
                        print("⚠️ Tentando Enter como alternativa...")
                        try:
                            self.page.press('input[type="email"]', 'Enter')
                            button_clicked = True
                        except:
                            print("❌ Enter também falhou")
                            return False
                    
                    if button_clicked:
                        time.sleep(4)  # Aguardar navegação
                    else:
                        return False
                    
                    # Aguardar página de senha e preencher
                    print("🔒 Aguardando página de senha...")
                    time.sleep(3)
                    
                    # Verificar se chegou na página de senha
                    has_password_field = self.page.evaluate("""
                        () => {
                            return document.querySelector('input[type="password"]') !== null;
                        }
                    """)
                    
                    if has_password_field:
                        print("🔒 Preenchendo senha...")
                        self.page.fill('input[type="password"]', password)
                        time.sleep(1)
                        
                        # Clicar em entrar
                        print("🔑 Fazendo login...")
                        time.sleep(2)
                        
                        # Tentar múltiplos seletores para botão de login
                        login_selectors = [
                            '#passwordNext',
                            'button:has-text("Next")',
                            'button:has-text("Entrar")',
                            'button:has-text("Sign in")',
                            'button[id*="next"]',
                            'button[id*="password"]',
                            'input[type="submit"]',
                            'button[type="submit"]',
                            '.VfPpkd-LgbsSe'
                        ]
                        
                        login_clicked = False
                        for selector in login_selectors:
                            try:
                                button_exists = self.page.evaluate(f"""
                                    () => {{
                                        const btn = document.querySelector('{selector}');
                                        return btn && btn.offsetParent !== null;
                                    }}
                                """)
                                
                                if button_exists:
                                    print(f"   🎯 Usando seletor: {selector}")
                                    self.page.click(selector)
                                    login_clicked = True
                                    break
                            except Exception as e:
                                print(f"   ⚠️ Seletor {selector} falhou: {str(e)[:50]}...")
                                continue
                        
                        if not login_clicked:
                            print("⚠️ Tentando Enter como alternativa...")
                            try:
                                self.page.press('input[type="password"]', 'Enter')
                                login_clicked = True
                            except:
                                print("❌ Botão de login não encontrado")
                                return False
                        
                        if login_clicked:
                            time.sleep(3)  # Aguardar um pouco menos primeiro
                            
                            # SCREENSHOT IMEDIATAMENTE após login
                            print("📸 Capturando tela após envio da senha...")
                            screenshot_path = self.take_screenshot("after_password_submit")
                            print(f"📸 Screenshot salvo: {screenshot_path}")
                            print("👀 VERIFIQUE A IMAGEM PARA VER SE APARECEU 2FA!")
                            print("⏳ Aguardando mais um momento para processar...")
                            
                            time.sleep(3)  # Aguardar mais um pouco
                        else:
                            return False
                        
                        # Verificar se login foi bem-sucedido ou se tem 2FA
                        final_url = self.page.url
                        print(f"🔗 URL após login: {final_url}")
                        
                        # Capturar screenshot do estado atual
                        print("📸 Capturando tela do estado atual...")
                        screenshot_path2 = self.take_screenshot("login_result_state")
                        print(f"📸 Screenshot estado: {screenshot_path2}")
                        
                        if "accounts.google.com" not in final_url:
                            print("✅ Login automático concluído com sucesso!")
                            return True
                        elif "challenge" in final_url or "2fa" in final_url.lower() or "verify" in final_url.lower():
                            print("🔐 2FA/Verificação detectada!")
                            print("📱 Verifique seu telefone ou o screenshot para autorizar")
                            
                            # Aguardar resolução manual do 2FA
                            print("⏳ Aguardando 90 segundos para você resolver 2FA...")
                            
                            # Verificar a cada 10 segundos se 2FA foi resolvido
                            for i in range(9):  # 9 x 10 = 90 segundos
                                time.sleep(10)
                                current_url = self.page.url
                                
                                if "accounts.google.com" not in current_url:
                                    print(f"✅ 2FA resolvido após {(i+1)*10} segundos!")
                                    # Screenshot de sucesso
                                    self.take_screenshot("2fa_resolved_success")
                                    return True
                                
                                # Screenshot a cada 30 segundos para acompanhar
                                if (i+1) % 3 == 0:
                                    self.take_screenshot(f"2fa_waiting_{(i+1)*10}s")
                                    print(f"⏳ Ainda aguardando 2FA... ({(i+1)*10}s)")
                            
                            # Verificação final
                            final_check_url = self.page.url
                            if "accounts.google.com" not in final_check_url:
                                print("✅ 2FA resolvido no tempo limite!")
                                return True
                            else:
                                print("⚠️ 2FA ainda pendente após 90 segundos")
                                self.take_screenshot("2fa_timeout")
                                return False
                        else:
                            print("⚠️ Login pode ter falhado - ainda na página de login")
                            return False
                    else:
                        print("❌ Página de senha não carregou")
                        return False
                else:
                    print("⚠️ Credenciais não configuradas - aguardando login manual")
                    print("ℹ️ Configure credenciais ou faça login manualmente")
                    
                    # Aguardar login manual
                    print("⏳ Aguardando 30 segundos para login manual...")
                    time.sleep(30)
                    
                    # Verificar se login foi concluído
                    final_url = self.page.url
                    if "accounts.google.com" not in final_url:
                        print("✅ Login manual concluído!")
                        return True
                    else:
                        print("⚠️ Ainda na página de login")
                        return False
            else:
                print("✅ Email já preenchido, continuando...")
            
            # Clicar em Next/Avançar
            print("➡️ Clicando em Avançar...")
            try:
                next_button = self.page.locator('button:has-text("Next"), button:has-text("Avançar"), #identifierNext')
                next_button.click()
                time.sleep(3)
            except:
                print("❌ Botão Avançar não encontrado")
                return False
            
            # Aguardar página de senha
            print("🔒 Aguardando página de senha...")
            time.sleep(3)
            
            # Verificar se chegou na página de senha
            has_password_field = self.page.evaluate("""
                () => {
                    return document.querySelector('input[type="password"]') !== null;
                }
            """)
            
            if has_password_field:
                print("🔒 Campo de senha encontrado")
                print("⚠️ Senha automática não implementada por segurança")
                print("ℹ️ Complete o login manualmente ou configure credenciais")
                
                # Aguardar um tempo para login manual
                print("⏳ Aguardando 30 segundos para login manual...")
                time.sleep(30)
                
                # Verificar se login foi concluído
                final_url = self.page.url
                if "accounts.google.com" not in final_url:
                    print("✅ Login parece ter sido concluído!")
                    return True
                else:
                    print("⚠️ Ainda na página de login")
                    return False
            else:
                print("❌ Página de senha não carregou")
                return False
                
        except Exception as e:
            print(f"❌ Erro no login: {e}")
            return False
    
    def find_input_field(self):
        """Encontra campo de input robusto"""
        try:
            print("🔍 Procurando campo de entrada...")
            
            # Aguardar um pouco
            time.sleep(2)
            
            # Usar JavaScript para encontrar o melhor campo
            input_info = self.page.evaluate("""
                () => {
                    const selectors = [
                        'textarea',
                        'input[type="text"]',
                        '[contenteditable="true"]',
                        '[role="textbox"]'
                    ];
                    
                    const candidates = [];
                    
                    for (const selector of selectors) {
                        const elements = document.querySelectorAll(selector);
                        for (const el of elements) {
                            if (el.offsetParent) { // Visível
                                const rect = el.getBoundingClientRect();
                                if (rect.width > 100 && rect.height > 20) {
                                    candidates.push({
                                        element: el,
                                        selector: selector,
                                        width: rect.width,
                                        height: rect.height,
                                        id: el.id,
                                        className: el.className,
                                        placeholder: el.placeholder || ''
                                    });
                                }
                            }
                        }
                    }
                    
                    // Escolher o maior campo (mais provável de ser o principal)
                    if (candidates.length > 0) {
                        candidates.sort((a, b) => (b.width * b.height) - (a.width * a.height));
                        const best = candidates[0];
                        
                        // Criar seletor específico
                        let specific_selector = best.selector;
                        if (best.id) {
                            specific_selector = `#${best.id}`;
                        } else if (best.className) {
                            const firstClass = best.className.split(' ')[0];
                            if (firstClass) {
                                specific_selector = `.${firstClass}`;
                            }
                        }
                        
                        return {
                            selector: specific_selector,
                            placeholder: best.placeholder,
                            width: best.width,
                            height: best.height
                        };
                    }
                    
                    return null;
                }
            """)
            
            if input_info:
                print(f"✅ Campo encontrado: {input_info['selector']}")
                print(f"   📐 Tamanho: {input_info['width']}x{input_info['height']}")
                print(f"   📝 Placeholder: '{input_info['placeholder']}'")
                return input_info['selector']
            else:
                print("❌ Nenhum campo adequado encontrado")
                return None
                
        except Exception as e:
            print(f"❌ Erro ao procurar campo: {e}")
            return None
    
    def send_message_robust(self, message):
        """Envia mensagem de forma robusta"""
        try:
            print(f"💬 Enviando: '{message[:50]}...'")
            
            # Encontrar campo
            input_selector = self.find_input_field()
            if not input_selector:
                print("❌ Campo não encontrado")
                return False
            
            # Focar e limpar
            print(f"🎯 Usando campo: {input_selector}")
            self.page.click(input_selector)
            time.sleep(0.5)
            
            # Limpar qualquer texto existente
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
            
            time.sleep(0.5)
            
            # Digitar mensagem
            print("⌨️ Digitando...")
            self.page.type(input_selector, message, delay=50)
            time.sleep(1)
            
            # Screenshot antes de enviar
            self.take_screenshot("before_send")
            
            # Enviar com Enter
            print("📤 Enviando com Enter...")
            self.page.press(input_selector, "Enter")
            time.sleep(3)
            
            # Verificar se campo foi limpo (indica sucesso)
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
                print("✅ Mensagem enviada (campo limpo)")
                
                # Adicionar ao histórico
                self.conversation_history.append({
                    'type': 'user',
                    'content': message,
                    'timestamp': datetime.now().isoformat()
                })
                
                self.take_screenshot("after_send")
                return True
            else:
                print("⚠️ Campo não foi limpo - possível falha")
                return False
            
        except Exception as e:
            print(f"❌ Erro ao enviar: {e}")
            return False
    
    def wait_for_ai_response(self, timeout=60):
        """Aguarda resposta do AI"""
        try:
            print("🤖 Aguardando resposta...")
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                time.sleep(3)
                
                # Procurar resposta na página
                response = self.page.evaluate("""
                    () => {
                        // Selectors comuns para respostas de AI
                        const responseSelectors = [
                            '[data-message-author-role="model"]',
                            '.model-response',
                            '.ai-response',
                            '[data-testid*="response"]',
                            '.response-content'
                        ];
                        
                        // Tentar seletores específicos primeiro
                        for (const selector of responseSelectors) {
                            const element = document.querySelector(selector);
                            if (element && element.textContent.trim().length > 10) {
                                return element.textContent.trim();
                            }
                        }
                        
                        // Fallback: procurar por blocos de texto que parecem respostas
                        const allElements = document.querySelectorAll('div, p, span');
                        for (const el of allElements) {
                            const text = el.textContent.trim();
                            // Critérios para identificar uma resposta:
                            // - Texto longo o suficiente
                            // - Não é nossa mensagem original
                            // - Contém palavras comuns de resposta
                            if (text.length > 30 && text.length < 10000) {
                                const hasResponseWords = /\\b(hello|olá|i|eu|can|posso|help|ajud|yes|sim|no|não)\\b/i.test(text);
                                if (hasResponseWords && !text.includes('Digite') && !text.includes('Enviando')) {
                                    return text;
                                }
                            }
                        }
                        
                        return null;
                    }
                """)
                
                if response:
                    print(f"✅ Resposta encontrada ({len(response)} chars)")
                    print(f"📝 Início: {response[:100]}...")
                    
                    # Adicionar ao histórico
                    self.conversation_history.append({
                        'type': 'assistant',
                        'content': response,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    self.take_screenshot("response_received")
                    return response
                
                elapsed = int(time.time() - start_time)
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
            print(f"❌ Erro ao salvar: {e}")
            return None
    
    def complete_interaction(self, message):
        """Executa interação completa"""
        try:
            print("🚀 INTERAÇÃO COMPLETA COM AI STUDIO")
            print("=" * 45)
            
            # 1. Inicializar
            self.initialize_browser()
            
            # 2. Acessar chat (que fará login se necessário)
            if not self.access_chat_directly():
                print("❌ Não foi possível acessar chat")
                return None
            
            print("✅ Chat acessível")
            
            # 3. Enviar mensagem
            if not self.send_message_robust(message):
                print("❌ Falha ao enviar mensagem")
                return None
            
            print("✅ Mensagem enviada")
            
            # 4. Aguardar resposta
            response = self.wait_for_ai_response()
            
            # 5. Salvar
            conversation_file = self.save_conversation()
            
            if response:
                print("\n🎉 INTERAÇÃO CONCLUÍDA!")
                print("=" * 30)
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
    """Função principal para teste"""
    print("🎯 TESTE DE INTERAÇÃO AI STUDIO")
    print("=" * 35)
    
    interaction = AIStudioInteraction(headless=True)
    
    try:
        # Solicitar mensagem
        message = input("\n💬 Sua pergunta (Enter para exemplo): ").strip()
        if not message:
            message = "Olá! Me explique brevemente como você funciona."
        
        print(f"\n🎯 Pergunta: '{message}'")
        
        # Executar
        result = interaction.complete_interaction(message)
        
        if result and result['success']:
            print(f"\n🎉 SUCESSO!")
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
