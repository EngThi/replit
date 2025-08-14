"""
Monitor 2FA Inteligente para AI Studio
- Detecta automaticamente quando 2FA é solicitado
- Captura screenshots em alta qualidade
- Destaca campos importantes
- Fornece instruções claras
- Salva logs detalhados
"""

import time
import os
from datetime import datetime
from ai_studio_login_2fa import AIStudioLogin2FA

class Monitor2FA:
    def __init__(self):
        self.login_system = AIStudioLogin2FA(headless=True)
        self.screenshots_dir = "/workspaces/replit/screenshots_2fa"
        self.ensure_directories()
        
    def ensure_directories(self):
        """Cria diretórios necessários"""
        os.makedirs(self.screenshots_dir, exist_ok=True)
        
    def capture_enhanced_screenshot(self, name_prefix="2fa"):
        """Captura screenshot com informações detalhadas"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Screenshot completo
            full_screenshot = f"{self.screenshots_dir}/{name_prefix}_full_{timestamp}.png"
            self.login_system.page.screenshot(path=full_screenshot, full_page=True)
            
            # Screenshot da viewport atual
            viewport_screenshot = f"{self.screenshots_dir}/{name_prefix}_viewport_{timestamp}.png"
            self.login_system.page.screenshot(path=viewport_screenshot)
            
            print(f"📸 Screenshots salvos:")
            print(f"   📄 Página completa: {full_screenshot}")
            print(f"   🖼️ Área visível: {viewport_screenshot}")
            
            return full_screenshot, viewport_screenshot
            
        except Exception as e:
            print(f"❌ Erro ao capturar screenshot: {e}")
            return None, None
    
    def extract_page_info(self):
        """Extrai informações úteis da página"""
        try:
            # Informações básicas
            url = self.login_system.page.url
            title = self.login_system.page.title()
            
            # Texto da página (primeiros 500 caracteres)
            page_text = self.login_system.page.evaluate("() => document.body.textContent")[:500]
            
            # Procurar por campos de input visíveis
            input_fields = self.login_system.page.evaluate("""
                () => {
                    const inputs = Array.from(document.querySelectorAll('input'));
                    return inputs.filter(input => input.offsetParent !== null).map(input => ({
                        type: input.type,
                        name: input.name,
                        id: input.id,
                        placeholder: input.placeholder,
                        ariaLabel: input.getAttribute('aria-label'),
                        maxLength: input.maxLength
                    }));
                }
            """)
            
            # Procurar por botões visíveis
            buttons = self.login_system.page.evaluate("""
                () => {
                    const buttons = Array.from(document.querySelectorAll('button, [role="button"]'));
                    return buttons.filter(btn => btn.offsetParent !== null).map(btn => ({
                        text: btn.textContent.trim(),
                        ariaLabel: btn.getAttribute('aria-label'),
                        type: btn.type
                    }));
                }
            """)
            
            return {
                'url': url,
                'title': title,
                'page_text': page_text,
                'input_fields': input_fields,
                'buttons': buttons
            }
            
        except Exception as e:
            print(f"❌ Erro ao extrair informações: {e}")
            return None
    
    def highlight_2fa_elements(self):
        """Destaca elementos relacionados ao 2FA"""
        try:
            # Script para destacar campos de código e botões importantes
            highlight_script = """
                () => {
                    // Campos que podem ser de 2FA
                    const codeSelectors = [
                        'input[type="tel"]',
                        'input[name*="code"]',
                        'input[name*="pin"]',
                        'input[autocomplete="one-time-code"]',
                        'input[inputmode="numeric"]',
                        'input[maxlength="6"]',
                        'input[maxlength="8"]'
                    ];
                    
                    // Destacar campos de código
                    codeSelectors.forEach(selector => {
                        const elements = document.querySelectorAll(selector);
                        elements.forEach(el => {
                            el.style.border = '3px solid #ff0000';
                            el.style.backgroundColor = '#fff0f0';
                            el.style.boxShadow = '0 0 10px rgba(255,0,0,0.5)';
                        });
                    });
                    
                    // Destacar botões de submit/next/verify
                    const submitButtons = Array.from(document.querySelectorAll('button, [role="button"]'));
                    submitButtons.forEach(btn => {
                        const text = btn.textContent.toLowerCase();
                        if (text.includes('next') || text.includes('verify') || text.includes('submit') || 
                            text.includes('continue') || text.includes('próximo') || text.includes('verificar')) {
                            btn.style.border = '3px solid #00ff00';
                            btn.style.backgroundColor = '#f0fff0';
                            btn.style.boxShadow = '0 0 10px rgba(0,255,0,0.5)';
                        }
                    });
                    
                    return 'Elementos destacados';
                }
            """
            
            result = self.login_system.page.evaluate(highlight_script)
            print("✨ Elementos 2FA destacados na página")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao destacar elementos: {e}")
            return False
    
    def detect_2fa_context(self):
        """Detecta contexto específico do 2FA"""
        try:
            # Verificar se está em página do Google Accounts
            url = self.login_system.page.url
            is_google_accounts = "accounts.google.com" in url
            
            # Procurar por textos específicos de 2FA
            page_text = self.login_system.page.evaluate("() => document.body.textContent.toLowerCase()")
            
            twofa_keywords = [
                "verification code",
                "2-step verification", 
                "authenticator",
                "código de verificação",
                "verificação em 2 etapas",
                "enter the code",
                "6-digit code",
                "app code"
            ]
            
            detected_keywords = [kw for kw in twofa_keywords if kw in page_text]
            
            # Procurar campos específicos de 2FA
            twofa_fields = self.login_system.page.evaluate("""
                () => {
                    const selectors = [
                        'input[type="tel"]',
                        'input[name*="code"]', 
                        'input[autocomplete="one-time-code"]',
                        'input[inputmode="numeric"]'
                    ];
                    
                    const fields = [];
                    selectors.forEach(selector => {
                        const elements = document.querySelectorAll(selector);
                        elements.forEach(el => {
                            if (el.offsetParent !== null) {
                                fields.push({
                                    selector: selector,
                                    id: el.id,
                                    name: el.name,
                                    placeholder: el.placeholder
                                });
                            }
                        });
                    });
                    return fields;
                }
            """)
            
            return {
                'is_google_accounts': is_google_accounts,
                'detected_keywords': detected_keywords,
                'twofa_fields': twofa_fields,
                'likely_2fa': len(detected_keywords) > 0 or len(twofa_fields) > 0
            }
            
        except Exception as e:
            print(f"❌ Erro ao detectar contexto 2FA: {e}")
            return None
    
    def create_detailed_report(self, context, page_info, screenshots):
        """Cria relatório detalhado da situação"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            report = f"""
=== RELATÓRIO DE DETECÇÃO 2FA ===
Data/Hora: {timestamp}
URL: {page_info['url']}
Título: {page_info['title']}

=== STATUS 2FA ===
Página do Google: {context['is_google_accounts']}
Provável 2FA: {context['likely_2fa']}
Palavras-chave encontradas: {', '.join(context['detected_keywords'])}

=== CAMPOS DETECTADOS ===
"""
            
            if context['twofa_fields']:
                for field in context['twofa_fields']:
                    report += f"- {field['selector']}"
                    if field['id']:
                        report += f" (ID: {field['id']})"
                    if field['placeholder']:
                        report += f" (Placeholder: {field['placeholder']})"
                    report += "\n"
            else:
                report += "Nenhum campo de 2FA detectado\n"
            
            report += f"""
=== CAMPOS DE INPUT ===
"""
            for field in page_info['input_fields'][:5]:  # Primeiros 5
                report += f"- Tipo: {field['type']}, Nome: {field['name']}, ID: {field['id']}\n"
            
            report += f"""
=== BOTÕES DISPONÍVEIS ===
"""
            for button in page_info['buttons'][:5]:  # Primeiros 5
                report += f"- Texto: '{button['text'][:30]}', Tipo: {button['type']}\n"
            
            report += f"""
=== SCREENSHOTS ===
Página completa: {screenshots[0]}
Área visível: {screenshots[1]}

=== TEXTO DA PÁGINA (INÍCIO) ===
{page_info['page_text']}
"""
            
            # Salvar relatório
            report_file = f"{self.screenshots_dir}/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"📊 Relatório detalhado salvo: {report_file}")
            return report_file
            
        except Exception as e:
            print(f"❌ Erro ao criar relatório: {e}")
            return None
    
    def monitor_login_process(self, email=None, password=None):
        """Monitora processo de login e detecta 2FA"""
        try:
            print("🕵️ MONITOR 2FA ATIVO")
            print("=" * 30)
            
            # Inicializar sistema de login
            self.login_system.initialize_browser()
            
            # Verificar se já está logado
            if self.login_system.check_if_logged_in():
                print("✅ Já está logado, nenhum 2FA necessário")
                return True
            
            # Obter credenciais se não fornecidas
            if not email:
                email = os.getenv("GOOGLE_EMAIL") or input("📧 Email: ")
            if not password:
                password = os.getenv("GOOGLE_PASSWORD") or input("🔒 Senha: ")
            
            # Iniciar processo de login
            print("🔑 Iniciando login...")
            if not self.login_system.start_login_process(email, password):
                print("❌ Falha no processo de login inicial")
                return False
            
            # Aguardar e monitorar
            print("🔍 Monitorando por 2FA...")
            
            for attempt in range(12):  # 60 segundos total (12 x 5s)
                time.sleep(5)
                
                # Capturar estado atual
                screenshots = self.capture_enhanced_screenshot(f"monitor_attempt_{attempt}")
                page_info = self.extract_page_info()
                context = self.detect_2fa_context()
                
                print(f"\n--- Tentativa {attempt + 1}/12 ---")
                print(f"URL: {page_info['url'][:60]}...")
                
                if context['likely_2fa']:
                    print("🎯 2FA DETECTADO!")
                    
                    # Destacar elementos
                    self.highlight_2fa_elements()
                    
                    # Capturar screenshot final com destaques
                    final_screenshots = self.capture_enhanced_screenshot("2fa_detected")
                    
                    # Criar relatório
                    report_file = self.create_detailed_report(context, page_info, final_screenshots)
                    
                    print("\n🎯 INSTRUÇÕES PARA 2FA:")
                    print("=" * 40)
                    print("📱 1. Abra seu app autenticador (Google Authenticator)")
                    print("🔍 2. Procure por 'Google' ou conta associada")
                    print("🔢 3. Anote o código de 6 dígitos")
                    print(f"📸 4. Verifique os screenshots em: {self.screenshots_dir}")
                    print(f"📊 5. Leia o relatório: {report_file}")
                    print("=" * 40)
                    
                    # Solicitar código
                    while True:
                        code = input("\n🔢 Digite o código 2FA (ou 'skip' para pular): ").strip()
                        
                        if code.lower() == 'skip':
                            print("⏭️ Pularei inserção automática")
                            break
                        
                        if len(code) == 6 and code.isdigit():
                            # Tentar inserir código
                            if self.insert_2fa_code(code, context['twofa_fields']):
                                print("✅ Código inserido com sucesso!")
                                time.sleep(5)
                                
                                # Verificar se login foi concluído
                                if self.login_system.check_if_logged_in():
                                    print("🎉 LOGIN CONCLUÍDO!")
                                    return True
                                else:
                                    print("⚠️ Código pode estar incorreto, tente novamente")
                            break
                        else:
                            print("❌ Código deve ter 6 dígitos numéricos")
                
                elif "aistudio.google.com" in page_info['url'] and "accounts.google.com" not in page_info['url']:
                    print("✅ Login concluído sem 2FA!")
                    return True
                
                else:
                    print(f"⏳ Aguardando... (palavras-chave: {len(context['detected_keywords'])})")
            
            print("⏰ Timeout do monitor - processo pode ter falhado")
            return False
            
        except Exception as e:
            print(f"❌ Erro no monitor: {e}")
            return False
    
    def insert_2fa_code(self, code, twofa_fields):
        """Insere código 2FA automaticamente"""
        try:
            if not twofa_fields:
                print("⚠️ Nenhum campo de 2FA encontrado para inserção automática")
                return False
            
            # Tentar inserir no primeiro campo encontrado
            field = twofa_fields[0]
            selector = field['selector']
            
            if field['id']:
                selector = f"#{field['id']}"
            elif field['name']:
                selector = f"input[name='{field['name']}']"
            
            print(f"⌨️ Inserindo código no campo: {selector}")
            
            # Limpar e inserir código
            self.login_system.page.fill(selector, "")
            time.sleep(0.5)
            self.login_system.page.fill(selector, code)
            time.sleep(1)
            
            # Tentar submeter
            submit_selectors = [
                "text=Next",
                "text=Verify", 
                "text=Continue",
                "button[type='submit']"
            ]
            
            for submit_sel in submit_selectors:
                try:
                    if self.login_system.page.is_visible(submit_sel, timeout=2000):
                        self.login_system.page.click(submit_sel)
                        print(f"📤 Enviado via: {submit_sel}")
                        return True
                except:
                    continue
            
            # Se não encontrou botão, tentar Enter
            self.login_system.page.press(selector, "Enter")
            print("📤 Enviado via Enter")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao inserir código: {e}")
            return False
    
    def cleanup(self):
        """Limpa recursos"""
        self.login_system.cleanup()

def main():
    """Função principal do monitor"""
    print("🕵️ MONITOR 2FA INTELIGENTE")
    print("=" * 35)
    
    monitor = Monitor2FA()
    
    try:
        # Executar monitoramento
        success = monitor.monitor_login_process()
        
        if success:
            print("\n🎉 PROCESSO CONCLUÍDO COM SUCESSO!")
            print("💾 Sessão salva para próximos acessos")
        else:
            print("\n❌ Processo não foi concluído")
            print("💡 Verifique os screenshots e relatórios")
        
        print(f"\n📁 Arquivos salvos em: {monitor.screenshots_dir}")
        
    except KeyboardInterrupt:
        print("\n⚠️ Interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    finally:
        monitor.cleanup()

if __name__ == "__main__":
    main()
