"""
Teste da automação em modo não-headless para contornar bloqueios de segurança
"""

import os
from automation import GoogleAIStudioAutomation

def test_visible_browser():
    """
    Testa a automação com navegador visível para evitar detecção
    """
    print("🔍 Testando automação com navegador visível...")
    
    # Email e senha de teste (substitua pelos seus)
    email = os.getenv("SEU_EMAIL", "")
    password = os.getenv("SUA_SENHA", "")
    
    if not email or not password:
        print("❌ Configure as variáveis de ambiente SEU_EMAIL e SUA_SENHA")
        return
    
    automation = GoogleAIStudioAutomation(headless=False, timeout_2fa=60)  # Modo visível
    
    try:
        print("1. Inicializando navegador visível...")
        automation.initialize_browser()
        
        print("2. Navegando para Google AI Studio...")
        automation.navigate_to_ai_studio()
        
        print("3. Clicando em Get started...")
        automation.start_login()
        
        print("4. Inserindo email...")
        automation.enter_email(email)
        
        print("5. Inserindo senha...")
        automation.enter_password(password)
        
        print("6. Aguardando 2FA...")
        automation.wait_for_2fa()
        
        print("✅ Login concluído!")
        automation.take_screenshot("login_sucesso.png")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        try:
            automation.take_screenshot("erro_login.png")
        except:
            pass
            
    finally:
        input("Pressione Enter para fechar o navegador...")
        automation.close_browser()

if __name__ == "__main__":
    test_visible_browser()
