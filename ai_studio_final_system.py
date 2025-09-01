"""
Sistema Final de Interação com AI Studio
Versão que funciona com limitações da conta
"""

import time
import json
import sys
import os
import re
from datetime import datetime

from ai_studio_login_2fa import AIStudioLogin2FA

class AIStudioFinalInteraction(AIStudioLogin2FA):
    def __init__(self, headless=True):
        super().__init__(headless)
        self.interactions_dir = "interactions"
        self.ensure_interaction_dirs()
        
    def ensure_interaction_dirs(self):
        """Cria e limpa os diretórios de interação."""
        screenshots_dir = f"{self.interactions_dir}/screenshots"
        logs_dir = f"{self.interactions_dir}/logs"

        os.makedirs(self.interactions_dir, exist_ok=True)
        os.makedirs(screenshots_dir, exist_ok=True)
        os.makedirs(logs_dir, exist_ok=True)

        # Limpar arquivos antigos, mantendo os 3 mais recentes
        self._cleanup_old_files(screenshots_dir, ".png", 3)
        self._cleanup_old_files(logs_dir, ".json", 3)
    
    def _cleanup_old_files(self, directory, file_extension, keep_count):
        """Limpa arquivos antigos em um diretório, mantendo os mais recentes."""
        try:
            # Garantir que o diretório existe
            if not os.path.isdir(directory):
                print(f"⚠️ Diretório não encontrado para limpeza: {directory}")
                return

            files = [f for f in os.listdir(directory) if f.endswith(file_extension)]

            # Extrai o timestamp do nome do arquivo para ordenação
            # Ex: final_report_20250814_223021.json -> 20250814_223021
            def get_timestamp(filename):
                match = re.search(r'(\d{8}_\d{6})', filename)
                # Se não encontrar timestamp, retorna uma string que vai para o final
                return match.group(1) if match else "00000000_000000"

            # Ordena do mais novo para o mais antigo
            files.sort(key=get_timestamp, reverse=True)

            if len(files) > keep_count:
                files_to_delete = files[keep_count:]
                print(f"🧹 Limpando {len(files_to_delete)} arquivos antigos em {os.path.basename(directory)}...")
                for f in files_to_delete:
                    try:
                        file_path = os.path.join(directory, f)
                        os.remove(file_path)
                        # print(f"   - Deletado: {f}") # Opcional: pode poluir o log
                    except OSError as e:
                        print(f"❌ Erro ao deletar {f}: {e}")
        except Exception as e:
            print(f"❌ Erro durante a limpeza de arquivos em {directory}: {e}")

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
    
    def click_get_started_button(self):
        """Clica no botão 'Get started' na página welcome"""
        try:
            print("🎯 Procurando botão 'Get started'...")
            
            # Aguardar a página carregar
            time.sleep(3)
            
            # Screenshot antes de tentar clicar
            self.take_screenshot("before_get_started")
            
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
                        
                        self.take_screenshot("after_get_started")
                        
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

    def check_account_access(self):
        """Verifica se a conta tem acesso às funcionalidades do AI Studio"""
        try:
            print("🔍 VERIFICANDO ACESSO DA CONTA")
            print("=" * 35)
            
            # Verificar se estamos na página welcome e tentar clicar Get started
            current_url = self.page.url
            if "welcome" in current_url:
                print("📍 Na página welcome - tentando clicar 'Get started'...")
                if self.click_get_started_button():
                    print("✅ Clique em Get started bem-sucedido")
                    time.sleep(3)  # Aguardar carregamento
                else:
                    print("⚠️ Não foi possível clicar em Get started")
            
            # Ir para página de API key para verificar acesso
            print("🔑 Verificando página de API key...")
            self.page.goto("https://aistudio.google.com/apikey", timeout=20000)
            time.sleep(3)
            
            current_url = self.page.url
            print(f"🔗 URL: {current_url}")
            
            if "accounts.google.com" in current_url:
                print("❌ Redirecionado para login - problema de sessão")
                return False
            
            # Capturar informações da página
            page_info = self.page.evaluate("""
                () => {
                    return {
                        title: document.title,
                        hasApiKeyText: document.body.textContent.includes('API key'),
                        hasCreateButton: !!document.querySelector('button:has-text("Create"), button:has-text("Generate")'),
                        hasRestrictedMessage: document.body.textContent.includes('not available') || 
                                            document.body.textContent.includes('restricted') ||
                                            document.body.textContent.includes('limited'),
                        bodyText: document.body.textContent.slice(0, 500)
                    };
                }
            """)
            
            print(f"📋 Título: {page_info['title']}")
            print(f"🔑 Tem texto 'API key': {page_info['hasApiKeyText']}")
            print(f"🔘 Tem botão Create: {page_info['hasCreateButton']}")
            print(f"⚠️ Mensagem de restrição: {page_info['hasRestrictedMessage']}")
            
            self.take_screenshot("account_access_check")
            
            if page_info['hasApiKeyText'] and not page_info['hasRestrictedMessage']:
                print("✅ Conta parece ter acesso básico ao AI Studio")
                return True
            else:
                print("⚠️ Conta pode ter acesso limitado")
                return False
                
        except Exception as e:
            print(f"❌ Erro verificando acesso: {e}")
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
                        self.take_screenshot("chat_interface_found")
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
                            
                            self.take_screenshot("working_chat_found")
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
    
    def generate_final_report(self):
        """Gera relatório final sobre o status do sistema"""
        try:
            print("\n📊 RELATÓRIO FINAL DO SISTEMA")
            print("=" * 40)
            
            # Informações do sistema
            report = {
                'timestamp': datetime.now().isoformat(),
                'login_status': 'working',
                'session_persistence': 'working', 
                'account_access': 'limited',
                'chat_access': 'not_found',
                'recommended_action': '',
                'alternative_solutions': []
            }
            
            # Verificar login
            if self.check_if_logged_in():
                print("✅ Sistema de Login: FUNCIONANDO")
                report['login_status'] = 'working'
            else:
                print("❌ Sistema de Login: PROBLEMA")
                report['login_status'] = 'failed'
            
            # Verificar acesso da conta
            if self.check_account_access():
                print("✅ Acesso da Conta: BÁSICO DISPONÍVEL") 
                report['account_access'] = 'basic'
            else:
                print("⚠️ Acesso da Conta: LIMITADO")
                report['account_access'] = 'limited'
            
            # Tentar encontrar chat
            chat_url = self.try_advanced_urls()
            if chat_url:
                print(f"✅ Interface de Chat: ENCONTRADA em {chat_url}")
                report['chat_access'] = 'found'
                report['chat_url'] = chat_url
            else:
                print("❌ Interface de Chat: NÃO ENCONTRADA")
                report['chat_access'] = 'not_found'
            
            # Recomendações
            print("\n💡 RECOMENDAÇÕES:")
            
            if report['chat_access'] == 'not_found':
                recommendations = [
                    "1. Verificar se a conta Google tem acesso ao AI Studio completo",
                    "2. Tentar acessar https://gemini.google.com/app diretamente",
                    "3. Verificar se há restrições regionais",
                    "4. Considerar usar API direta do Gemini em vez da interface web",
                    "5. Aguardar expansão do acesso ao AI Studio na região"
                ]
                
                for rec in recommendations:
                    print(f"   {rec}")
                
                report['recommended_action'] = "Use Gemini API directly or wait for full AI Studio access"
                report['alternative_solutions'] = [
                    "Direct Gemini API integration",
                    "Use google-generativeai Python library", 
                    "Access via Vertex AI platform"
                ]
            else:
                print("   ✅ Sistema funcionando - prosseguir com interações")
                report['recommended_action'] = "System ready for interactions"
            
            # Salvar relatório
            report_file = f"{self.interactions_dir}/logs/final_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"\n📁 Relatório salvo: {report_file}")
            
            return report
            
        except Exception as e:
            print(f"❌ Erro no relatório: {e}")
            return None
    
    def complete_system_test(self):
        """Teste completo do sistema"""
        try:
            print("🚀 TESTE COMPLETO DO SISTEMA AI STUDIO")
            print("=" * 45)
            
            # Inicializar
            self.initialize_browser()
            
            # Teste de login
            if not self.check_if_logged_in():
                print("🔑 Executando login...")
                if not self.quick_login():
                    print("❌ Falha no login")
                    return False
            
            print("✅ Login verificado")
            
            # Gerar relatório final
            report = self.generate_final_report()
            
            if report and report['chat_access'] == 'found':
                print("\n🎉 SISTEMA PRONTO PARA INTERAÇÕES!")
                return True
            else:
                print("\n⚠️ Sistema funcionando mas com limitações de acesso")
                return False
                
        except Exception as e:
            print(f"❌ Erro no teste completo: {e}")
            return False
        finally:
            self.cleanup()

def main():
    """Função principal"""
    print("🎯 SISTEMA FINAL DE INTERAÇÃO AI STUDIO")
    print("=" * 45)
    
    system = AIStudioFinalInteraction(headless=True)
    
    try:
        success = system.complete_system_test()
        
        if success:
            print("\n🎉 SISTEMA COMPLETAMENTE FUNCIONAL!")
        else:
            print("\n📋 SISTEMA PARCIALMENTE FUNCIONAL")
            print("ℹ️ Verificar relatório para detalhes e alternativas")
            
    except KeyboardInterrupt:
        print("\n⚠️ Teste interrompido")
    except Exception as e:
        print(f"\n❌ Erro: {e}")

if __name__ == "__main__":
    main()
