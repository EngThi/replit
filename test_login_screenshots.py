#!/usr/bin/env python3
"""
Teste de Login com Screenshots para 2FA
"""

import sys
sys.path.append('/workspaces/replit')

from ai_studio_interaction_improved import AIStudioInteraction

def test_login_with_screenshots():
    """Testa login com capturas de tela para 2FA"""
    print("🔐 TESTE DE LOGIN COM SCREENSHOTS PARA 2FA")
    print("=" * 50)
    
    interaction = AIStudioInteraction(headless=True)
    
    try:
        print("1️⃣ Inicializando navegador...")
        interaction.initialize_browser()
        
        print("2️⃣ Acessando AI Studio...")
        target_url = "https://aistudio.google.com/u/3/prompts/new_chat"
        interaction.page.goto(target_url, timeout=20000)
        
        import time
        time.sleep(3)
        
        final_url = interaction.page.url
        print(f"🔗 URL: {final_url[:80]}...")
        
        if "accounts.google.com" in final_url:
            print("3️⃣ Redirecionado para login - iniciando processo...")
            
            # Fazer login com screenshots
            login_success = interaction.do_login_on_current_page()
            
            if login_success:
                print("\n🎉 LOGIN REALIZADO COM SUCESSO!")
                print("✅ Agora tentando acessar chat...")
                
                # Tentar acessar chat novamente
                interaction.page.goto(target_url, timeout=20000)
                time.sleep(5)
                
                new_url = interaction.page.url
                print(f"🔗 Nova URL: {new_url}")
                
                if "accounts.google.com" not in new_url:
                    print("✅ Chat acessível após login!")
                    
                    # Screenshot final de sucesso
                    interaction.take_screenshot("chat_access_success")
                    
                    # Verificar campo de input
                    has_input = interaction.page.evaluate("""
                        () => {
                            const inputs = document.querySelectorAll('textarea, input[type="text"], [contenteditable="true"]');
                            for (const input of inputs) {
                                if (input.offsetParent && input.getBoundingClientRect().width > 200) {
                                    return true;
                                }
                            }
                            return false;
                        }
                    """)
                    
                    if has_input:
                        print("✅ Campo de entrada encontrado no chat!")
                        interaction.take_screenshot("chat_input_ready")
                        
                        print("\n🎉 SISTEMA COMPLETAMENTE FUNCIONAL!")
                        print("🚀 Pronto para enviar mensagens para o AI Studio!")
                        return True
                    else:
                        print("⚠️ Chat carregou mas campo de entrada não encontrado")
                        interaction.take_screenshot("chat_no_input")
                        return False
                else:
                    print("⚠️ Ainda redirecionando para login")
                    return False
            else:
                print("❌ Login não foi concluído")
                return False
        else:
            print("⚠️ Não foi redirecionado para login")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False
    finally:
        print(f"\n📁 Screenshots salvos em: {interaction.interactions_dir}/screenshots/")
        interaction.cleanup()

def main():
    """Executa teste de login"""
    print("🚀 TESTE DE LOGIN COM 2FA VISUAL")
    print("=" * 35)
    
    success = test_login_with_screenshots()
    
    if success:
        print("\n🎉 TESTE COMPLETO: SUCESSO!")
        print("✅ Sistema de login funcionando")
        print("✅ Acesso ao chat funcionando")
        print("✅ Pronto para interações automáticas")
    else:
        print("\n⚠️ TESTE PARCIAL")
        print("ℹ️ Verifique os screenshots para ver o que aconteceu")
        print("📸 Screenshots em: /workspaces/replit/interactions/screenshots/")

if __name__ == "__main__":
    main()
