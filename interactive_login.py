"""
Automação interativa que permite inserir código 2FA manualmente
"""

import os
import time
from automation import GoogleAIStudioAutomation

def interactive_login():
    """
    Login interativo que permite inserir código 2FA
    """
    print("🚀 Automação Interativa do Google AI Studio")
    print("=" * 50)
    
    # Verificar credenciais
    email = os.getenv("SEU_EMAIL", "")
    password = os.getenv("SUA_SENHA", "")
    
    if not email:
        email = input("📧 Digite seu email: ")
    else:
        print(f"📧 Email: {email}")
        
    if not password:
        password = input("🔒 Digite sua senha: ")
    else:
        print("🔒 Senha: [configurada via variável de ambiente]")
    
    automation = GoogleAIStudioAutomation(headless=True, timeout_2fa=120)  # 2 minutos para 2FA
    
    try:
        print("\n1. ✅ Inicializando navegador...")
        automation.initialize_browser()
        
        print("2. ✅ Navegando para Google AI Studio...")
        automation.navigate_to_ai_studio()
        
        print("3. ✅ Clicando em Get started...")
        automation.start_login()
        
        print("4. ✅ Inserindo email...")
        automation.enter_email(email)
        
        print("5. ✅ Inserindo senha...")
        automation.enter_password(password)
        
        print("6. 🔍 Verificando 2FA...")
        
        # Verificar se chegou na página de 2FA
        time.sleep(3)
        
        # Capturar screenshot para o usuário ver
        automation.take_screenshot("current_page.png")
        print("📸 Screenshot da página atual salvo em: current_page.png")
        
        # Verificar se há campo de código
        code_field = None
        code_selectors = [
            "input[type='tel']",
            "input[name='totpPin']", 
            "input[id*='code']",
            "input[id*='pin']",
            "input[autocomplete='one-time-code']",
            "input[inputmode='numeric']"
        ]
        
        for selector in code_selectors:
            try:
                if automation.page.is_visible(selector):
                    code_field = selector
                    print(f"✅ Campo de código 2FA encontrado!")
                    break
            except:
                continue
        
        if code_field:
            print("\n📱 2FA DETECTADO!")
            print("=" * 30)
            print("🔍 Verifique seu celular para o código de verificação")
            print("📸 Ou olhe o arquivo 'current_page.png' para ver a tela atual")
            
            # Aguardar código do usuário
            while True:
                try:
                    code = input("\n🔢 Digite o código 2FA (ou 'screenshot' para nova captura): ")
                    
                    if code.lower() == 'screenshot':
                        automation.take_screenshot("current_page.png")
                        print("📸 Novo screenshot salvo!")
                        continue
                    
                    if len(code) >= 6 and code.isdigit():
                        print(f"✅ Inserindo código: {code}")
                        
                        # Inserir código
                        automation.page.fill(code_field, code)
                        automation.page.wait_for_timeout(1000)
                        
                        # Clicar em Next/Verify
                        submit_selectors = [
                            "text=Next",
                            "text=Próximo", 
                            "text=Verify",
                            "text=Verificar",
                            "button[type='submit']"
                        ]
                        
                        for selector in submit_selectors:
                            try:
                                if automation.page.is_visible(selector):
                                    automation.page.click(selector)
                                    print("✅ Código submetido!")
                                    break
                            except:
                                continue
                        
                        # Aguardar resultado
                        time.sleep(5)
                        
                        # Verificar se foi aceito
                        current_url = automation.page.url
                        if "accounts.google.com" not in current_url:
                            print("🎉 LOGIN CONCLUÍDO COM SUCESSO!")
                            automation.take_screenshot("login_success.png")
                            break
                        else:
                            # Verificar se ainda está na página de código
                            if automation.page.is_visible(code_field):
                                print("❌ Código incorreto. Tente novamente.")
                                automation.take_screenshot("current_page.png")
                            else:
                                print("✅ Código aceito! Continuando...")
                                break
                    else:
                        print("❌ Código deve ter pelo menos 6 dígitos")
                        
                except KeyboardInterrupt:
                    print("\n⚠️ Operação cancelada pelo usuário")
                    break
        else:
            print("ℹ️ Nenhum 2FA detectado - login pode ter sido concluído")
            automation.take_screenshot("final_page.png")
        
        print("\n✅ Processo concluído!")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        try:
            automation.take_screenshot("error_page.png")
            print("📸 Screenshot do erro salvo em: error_page.png")
        except:
            pass
            
    finally:
        input("\nPressione Enter para fechar...")
        automation.close_browser()

if __name__ == "__main__":
    interactive_login()
