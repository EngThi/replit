"""
Sistema de login interativo e completo para Google AI Studio
Combinando detecção inteligente com processo de login robusto
"""

import time
import os
from smart_login import SmartLoginDetection

class InteractiveLoginComplete(SmartLoginDetection):
    def __init__(self):
        super().__init__()
    
    def handle_2fa_interactive_improved(self):
        """Lida com 2FA de forma interativa melhorada"""
        try:
            print("\n📱 VERIFICANDO 2FA...")
            time.sleep(3)
            
            # Verificar se há campo de código
            code_selectors = [
                "input[type='tel']",
                "input[name='totpPin']", 
                "input[id*='code']",
                "input[id*='pin']",
                "input[autocomplete='one-time-code']",
                "input[inputmode='numeric']"
            ]
            
            code_field = None
            for selector in code_selectors:
                try:
                    if self.page.is_visible(selector, timeout=2000):
                        code_field = selector
                        break
                except:
                    continue
            
            if code_field:
                self.page.screenshot(path="2fa_interactive.png")
                print("\n📱 2FA DETECTADO!")
                print("🔍 Verifique seu celular para escolher o número correto")
                print("📸 Screenshot salvo: 2fa_interactive.png")
                
                while True:
                    try:
                        code = input("\n🔢 Digite o código 2FA (ou 'skip' para pular): ")
                        
                        if code.lower() == 'skip':
                            print("⏭️ Pulando 2FA...")
                            break
                        
                        if len(code) >= 6 and code.isdigit():
                            self.page.fill(code_field, code)
                            time.sleep(1)
                            
                            # Submeter
                            submit_selectors = ["text=Next", "text=Verify", "button[type='submit']"]
                            for selector in submit_selectors:
                                try:
                                    if self.page.is_visible(selector):
                                        self.page.click(selector)
                                        break
                                except:
                                    continue
                            
                            time.sleep(5)
                            
                            # Verificar se saiu da página de 2FA
                            if not self.page.is_visible(code_field):
                                print("✅ 2FA concluído!")
                                break
                            else:
                                print("❌ Código incorreto. Tente novamente.")
                                self.page.screenshot(path="2fa_interactive.png")
                        else:
                            print("❌ Código deve ter pelo menos 6 dígitos")
                            
                    except KeyboardInterrupt:
                        print("\n⚠️ Interrompido pelo usuário")
                        break
            else:
                print("ℹ️ Nenhum 2FA detectado")
                
        except Exception as e:
            print(f"❌ Erro no 2FA: {e}")
    
    def complete_interactive_login(self, email, password):
        """Processo completo de login interativo"""
        try:
            print("\n🔑 PROCESSO COMPLETO DE LOGIN")
            print("=" * 40)
            
            # 1. Navegar para AI Studio
            print("1. 🌐 Navegando para Google AI Studio...")
            self.page.goto("https://aistudio.google.com/", timeout=30000)
            time.sleep(3)
            self.page.screenshot(path="step1_homepage.png")
            
            # 2. Clicar em Get started
            print("2. ▶️ Clicando em 'Get started'...")
            
            get_started_selectors = [
                "text=Get started",
                "button:has-text('Get started')",
                "a:has-text('Get started')"
            ]
            
            clicked = False
            for selector in get_started_selectors:
                try:
                    if self.page.is_visible(selector, timeout=3000):
                        self.page.click(selector)
                        clicked = True
                        print(f"✅ Clicou: {selector}")
                        break
                except:
                    continue
            
            if not clicked:
                print("❌ Não encontrou 'Get started'")
                return False
            
            time.sleep(5)
            self.page.screenshot(path="step2_after_get_started.png")
            
            # 3. Inserir email
            print("3. 📧 Inserindo email...")
            
            email_selectors = [
                "input[type='email']",
                "input[name='identifier']", 
                "#identifierId"
            ]
            
            email_inserted = False
            for selector in email_selectors:
                try:
                    if self.page.is_visible(selector, timeout=5000):
                        self.page.click(selector)
                        time.sleep(0.5)
                        self.page.fill(selector, "")
                        time.sleep(0.3)
                        
                        # Digitar email devagar
                        for char in email:
                            self.page.type(selector, char, delay=50)
                        
                        time.sleep(1)
                        
                        # Clicar Next
                        next_selectors = ["text=Next", "#identifierNext"]
                        for next_sel in next_selectors:
                            try:
                                if self.page.is_visible(next_sel):
                                    self.page.click(next_sel)
                                    break
                            except:
                                continue
                        
                        email_inserted = True
                        print(f"✅ Email inserido: {selector}")
                        break
                except:
                    continue
            
            if not email_inserted:
                print("❌ Não conseguiu inserir email")
                return False
            
            time.sleep(3)
            self.page.screenshot(path="step3_after_email.png")
            
            # 4. Inserir senha
            print("4. 🔒 Inserindo senha...")
            
            password_selectors = [
                "input[type='password']",
                "input[name='password']", 
                "#password"
            ]
            
            password_inserted = False
            for selector in password_selectors:
                try:
                    if self.page.is_visible(selector, timeout=10000):
                        self.page.click(selector)
                        time.sleep(0.5)
                        self.page.fill(selector, "")
                        time.sleep(0.3)
                        
                        # Digitar senha devagar
                        for char in password:
                            self.page.type(selector, char, delay=60)
                        
                        time.sleep(1)
                        
                        # Clicar Next
                        next_selectors = ["text=Next", "#passwordNext"]
                        for next_sel in next_selectors:
                            try:
                                if self.page.is_visible(next_sel):
                                    self.page.click(next_sel)
                                    break
                            except:
                                continue
                        
                        password_inserted = True
                        print(f"✅ Senha inserida: {selector}")
                        break
                except:
                    continue
            
            if not password_inserted:
                print("❌ Não conseguiu inserir senha")
                return False
            
            time.sleep(5)
            self.page.screenshot(path="step4_after_password.png")
            
            # 5. Lidar com 2FA se necessário
            print("5. 📱 Verificando 2FA...")
            self.handle_2fa_interactive_improved()
            
            # 6. Aguardar conclusão
            print("6. ⏳ Aguardando conclusão do login...")
            time.sleep(10)
            
            # 7. Verificar se login foi bem-sucedido
            final_url = self.page.url
            print(f"🔗 URL final: {final_url}")
            
            self.page.screenshot(path="step7_final_result.png")
            
            # Verificar se chegou ao AI Studio
            if "aistudio.google.com" in final_url and "accounts.google.com" not in final_url:
                print("✅ LOGIN APARENTA TER SIDO BEM-SUCEDIDO!")
                
                # Verificação adicional
                is_logged = self.check_login_status_smart()
                if is_logged:
                    print("✅ CONFIRMADO: Login bem-sucedido!")
                    return True
                else:
                    print("⚠️ Login pode precisar de verificação manual")
                    return False
            else:
                print("❌ Login não foi concluído - ainda em página de autenticação")
                return False
                
        except Exception as e:
            print(f"❌ Erro no login completo: {e}")
            self.page.screenshot(path="login_error.png")
            return False
    
    def full_system_with_interaction(self):
        """Sistema completo com interação"""
        try:
            print("🎯 SISTEMA COMPLETO DE LOGIN INTERATIVO")
            print("=" * 50)
            
            # Inicializar
            self.initialize_with_profile()
            
            # Teste rápido
            if self.quick_test_access():
                print("🎉 JÁ ESTÁ LOGADO! Sistema funcionando")
                return True
            
            # Obter credenciais
            email = os.getenv("SEU_EMAIL", "")
            password = os.getenv("SUA_SENHA", "")
            
            if not email:
                email = input("\n📧 Digite seu email: ")
            else:
                print(f"\n📧 Email configurado: {email}")
                
            if not password:
                password = input("🔒 Digite sua senha: ")
            else:
                print("🔒 Senha: [configurada nas variáveis]")
            
            # Executar login completo
            success = self.complete_interactive_login(email, password)
            
            if success:
                print("\n🎉 LOGIN CONCLUÍDO COM SUCESSO!")
                print("💾 Sessão salva no perfil do navegador")
                print("🚀 Google AI Studio pronto para uso!")
                
                # Teste final
                time.sleep(5)
                final_test = self.quick_test_access()
                if final_test:
                    print("✅ TESTE FINAL PASSOU!")
                else:
                    print("⚠️ Teste final falhou, mas login aparenta estar OK")
                
                return True
            else:
                print("\n❌ FALHA NO LOGIN")
                print("💡 Verifique os screenshots para debug:")
                print("   - step1_homepage.png")
                print("   - step2_after_get_started.png") 
                print("   - step3_after_email.png")
                print("   - step4_after_password.png")
                print("   - step7_final_result.png")
                return False
                
        except Exception as e:
            print(f"❌ Erro no sistema: {e}")
            return False

def main():
    """Função principal"""
    login_system = InteractiveLoginComplete()
    
    try:
        success = login_system.full_system_with_interaction()
        
        if success:
            print("\n🏆 SISTEMA CONCLUÍDO COM SUCESSO!")
            input("\n⏸️ Pressione Enter para fechar...")
        else:
            print("\n❌ Sistema falhou")
            input("\n⏸️ Pressione Enter para fechar...")
            
    finally:
        login_system.cleanup()

if __name__ == "__main__":
    main()
