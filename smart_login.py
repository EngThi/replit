"""
Sistema de detecção inteligente de login no Google AI Studio
Corrige o problema de detecção falsa de login
"""

import time
import os
from persistent_login import PersistentGoogleLogin

class SmartLoginDetection(PersistentGoogleLogin):
    def __init__(self):
        super().__init__()
    
    def check_login_status_smart(self):
        """Detecção inteligente e mais precisa do status de login"""
        try:
            print("🔍 VERIFICAÇÃO INTELIGENTE DE LOGIN...")
            
            # Navegar para página principal
            self.page.goto("https://aistudio.google.com/", timeout=30000)
            time.sleep(5)
            
            # Capturar screenshot para análise
            self.page.screenshot(path="login_status_check.png")
            print("📸 Screenshot para análise: login_status_check.png")
            
            # Verificar URL final após redirecionamentos
            current_url = self.page.url
            print(f"🔗 URL atual: {current_url}")
            
            # Método 1: Verificar se há redirecionamento para login
            if "accounts.google.com" in current_url:
                print("❌ Redirecionado para Google Accounts - NÃO está logado")
                return False
            
            # Método 2: Procurar indicadores NEGATIVOS (que indicam que NÃO está logado)
            not_logged_indicators = [
                "text=Get started",
                "text=Sign in", 
                "text=Sign up",
                "text=Login",
                "button:has-text('Get started')",
                "a:has-text('Get started')",
                "[aria-label*='get started']",
                "[aria-label*='sign in']"
            ]
            
            print("🔍 Procurando indicadores de NÃO logado...")
            for indicator in not_logged_indicators:
                try:
                    if self.page.is_visible(indicator, timeout=3000):
                        print(f"❌ Encontrado indicador de NÃO logado: {indicator}")
                        return False
                except:
                    continue
            
            # Método 3: Procurar indicadores POSITIVOS (que confirmam login)
            logged_in_indicators = [
                # Elementos específicos do dashboard logado
                "text=New chat",
                "text=Create new",
                "text=Dashboard", 
                "text=History",
                "text=Build",
                "text=Documentation",
                # Elementos de usuário logado
                "[data-testid*='user']",
                "[data-testid*='avatar']",
                ".user-menu",
                ".profile-button",
                # Elementos específicos do AI Studio logado
                "text=Chat",
                "text=Stream", 
                "text=Generate Media",
                # Botões/links que só aparecem quando logado
                "a[href*='/app/']",
                "button:has-text('Run')",
                "button:has-text('New')"
            ]
            
            print("✅ Procurando indicadores de logado...")
            positive_indicators_found = []
            
            for indicator in logged_in_indicators:
                try:
                    if self.page.is_visible(indicator, timeout=2000):
                        positive_indicators_found.append(indicator)
                        print(f"✅ Encontrado indicador positivo: {indicator}")
                except:
                    continue
            
            # Método 4: Verificar conteúdo da página
            page_content = self.page.evaluate("""
                () => {
                    const bodyText = document.body.textContent.toLowerCase();
                    return {
                        hasGetStarted: bodyText.includes('get started'),
                        hasSignIn: bodyText.includes('sign in'),
                        hasDashboard: bodyText.includes('dashboard'),
                        hasNewChat: bodyText.includes('new chat'),
                        hasUserContent: bodyText.includes('history') || bodyText.includes('prompts')
                    };
                }
            """)
            
            print(f"📄 Análise do conteúdo: {page_content}")
            
            # Lógica de decisão
            if page_content['hasGetStarted'] or page_content['hasSignIn']:
                print("❌ DECISÃO: NÃO está logado (encontrou 'Get started' ou 'Sign in')")
                return False
            
            if len(positive_indicators_found) >= 2:
                print(f"✅ DECISÃO: ESTÁ logado (encontrou {len(positive_indicators_found)} indicadores positivos)")
                return True
            
            if page_content['hasDashboard'] or page_content['hasNewChat'] or page_content['hasUserContent']:
                print("✅ DECISÃO: ESTÁ logado (conteúdo de usuário detectado)")
                return True
            
            # Se chegou até aqui, assumir que não está logado para segurança
            print("⚠️ DECISÃO: Assumindo NÃO logado (indicadores inconclusivos)")
            return False
            
        except Exception as e:
            print(f"❌ Erro na verificação: {e}")
            return False
    
    def smart_login_or_access(self):
        """Login inteligente que só faz login se realmente necessário"""
        try:
            print("🎯 SISTEMA DE LOGIN INTELIGENTE")
            print("=" * 45)
            
            # Verificar status real de login (sem reinicializar navegador)
            is_logged_in = self.check_login_status_smart()
            
            if is_logged_in:
                print("\n🎉 JÁ ESTÁ LOGADO!")
                print("✅ Sessão persistente funcionando corretamente")
                print("🚀 Pronto para usar o AI Studio")
                
                # Navegar para área principal se necessário
                try:
                    if "/app/" not in self.page.url:
                        print("🔄 Navegando para área principal...")
                        self.page.goto("https://aistudio.google.com/app/", timeout=30000)
                        time.sleep(3)
                except:
                    pass
                
                self.page.screenshot(path="logged_in_confirmed.png")
                print("📸 Screenshot confirmação: logged_in_confirmed.png")
                return True
                
            else:
                print("\n🔑 PRECISA FAZER LOGIN")
                print("🔄 Iniciando processo de login completo...")
                
                # Obter credenciais
                email = os.getenv("SEU_EMAIL", "")
                password = os.getenv("SUA_SENHA", "")
                
                if not email:
                    email = input("📧 Digite seu email: ")
                else:
                    print(f"📧 Email: {email}")
                    
                if not password:
                    password = input("🔒 Digite sua senha: ")
                else:
                    print("🔒 Senha: [configurada]")
                
                # Executar login completo
                success = self.execute_complete_login(email, password)
                
                if success:
                    print("\n🎉 LOGIN CONCLUÍDO COM SUCESSO!")
                    print("💾 Sessão salva para próximas vezes")
                    return True
                else:
                    print("\n❌ FALHA NO LOGIN")
                    return False
                    
        except Exception as e:
            print(f"❌ Erro no sistema inteligente: {e}")
            return False
    
    def execute_complete_login(self, email, password):
        """Executa o processo completo de login"""
        try:
            from automation import GoogleAIStudioAutomation
            
            # Usar o sistema de automação existente
            automation = GoogleAIStudioAutomation(headless=True, timeout_2fa=120)
            automation.context = self.context
            automation.page = self.page 
            automation.playwright = self.playwright
            
            print("1. 🌐 Navegando para AI Studio...")
            automation.navigate_to_ai_studio()
            
            print("2. ▶️ Iniciando login...")
            automation.start_login()
            
            print("3. 📧 Inserindo email...")
            automation.enter_email(email)
            
            print("4. 🔒 Inserindo senha...")
            automation.enter_password(password)
            
            print("5. 📱 Verificando 2FA...")
            automation.wait_for_2fa()
            
            print("6. ⏳ Finalizando login...")
            time.sleep(5)
            
            # Verificar se login foi bem-sucedido
            final_check = self.check_login_status_smart()
            
            if final_check:
                print("✅ Login confirmado!")
                self.page.screenshot(path="login_success_smart.png")
                return True
            else:
                print("❌ Login pode não ter sido concluído")
                self.page.screenshot(path="login_failed_smart.png")
                return False
                
        except Exception as e:
            print(f"❌ Erro no login: {e}")
            return False
    
    def quick_test_access(self):
        """Teste rápido de acesso para verificar se funciona"""
        try:
            # Ir direto para área de chat
            print("🧪 Teste rápido: navegando para área de chat...")
            self.page.goto("https://aistudio.google.com/app/prompts/new", timeout=30000)
            time.sleep(5)
            
            current_url = self.page.url
            print(f"🔗 URL alcançada: {current_url}")
            
            # Se conseguiu chegar na área de chat sem redirecionamento para login
            if "app/prompts" in current_url or "app/" in current_url:
                print("✅ ACESSO CONFIRMADO! Está logado e funcionando")
                self.page.screenshot(path="quick_test_success.png")
                return True
            else:
                print("❌ Redirecionado - não está logado")
                self.page.screenshot(path="quick_test_failed.png")
                return False
                
        except Exception as e:
            print(f"❌ Erro no teste: {e}")
            return False

def main():
    """Função principal do sistema inteligente"""
    print("🧠 SISTEMA DE LOGIN INTELIGENTE DO AI STUDIO")
    print("=" * 55)
    
    smart_login = SmartLoginDetection()
    
    try:
        # Inicializar navegador apenas uma vez
        smart_login.initialize_with_profile()
        
        # Teste rápido primeiro
        print("🧪 Executando teste rápido de acesso...")
        if smart_login.quick_test_access():
            print("\n🎉 TESTE PASSOU! Sistema funcionando")
            return True
        
        print("\n🔧 Teste falhou, executando sistema completo...")
        
        # Sistema completo (já tem navegador inicializado)
        success = smart_login.smart_login_or_access()
        
        if success:
            print("\n🏆 SISTEMA INTELIGENTE CONCLUÍDO COM SUCESSO!")
            print("🚀 Google AI Studio pronto para uso")
        else:
            print("\n❌ Sistema não conseguiu estabelecer acesso")
            
        return success
        
    except Exception as e:
        print(f"\n❌ Erro geral: {e}")
        return False
    finally:
        smart_login.cleanup()

if __name__ == "__main__":
    main()
