"""
Script para capturar screenshot do 2FA e mostrar número
"""

import time
from automation import GoogleAIStudioAutomation

def capture_2fa_screenshot():
    """Captura screenshot quando detectar 2FA"""
    try:
        print("📱 DETECTOR DE 2FA ATIVO")
        print("=" * 30)
        
        automation = GoogleAIStudioAutomation(headless=True, timeout_2fa=180)
        automation.initialize_browser()
        
        # Navegar para AI Studio
        automation.page.goto("https://aistudio.google.com/")
        time.sleep(3)
        
        # Verificar se está na página de 2FA ou precisa fazer login
        current_url = automation.page.url
        print(f"🔗 URL atual: {current_url}")
        
        if "accounts.google.com" in current_url:
            print("🔍 Detectada página de login/2FA do Google")
            
            # Capturar screenshot imediato
            screenshot_path = "2fa_current_screen.png"
            automation.page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Screenshot capturado: {screenshot_path}")
            
            # Verificar se há campo de código 2FA
            code_selectors = [
                "input[type='tel']",
                "input[name='totpPin']", 
                "input[id*='code']",
                "input[id*='pin']",
                "input[autocomplete='one-time-code']",
                "input[inputmode='numeric']"
            ]
            
            code_field_found = False
            for selector in code_selectors:
                try:
                    if automation.page.is_visible(selector, timeout=2000):
                        print(f"✅ Campo de código 2FA encontrado: {selector}")
                        code_field_found = True
                        
                        # Capturar screenshot específico do campo 2FA
                        automation.page.screenshot(path="2fa_code_field.png")
                        print("📸 Screenshot do campo 2FA: 2fa_code_field.png")
                        break
                except:
                    continue
            
            if code_field_found:
                # Aguardar código ser inserido
                print("\n💬 INSTRUÇÕES:")
                print("1. Verifique o screenshot: 2fa_code_field.png")
                print("2. Veja seu celular para o número que aparece")
                print("3. Digite o código quando solicitar")
                
                code = input("\n🔢 Digite o código 2FA que você vê: ")
                
                if code and len(code) >= 6:
                    # Inserir código
                    for selector in code_selectors:
                        try:
                            if automation.page.is_visible(selector):
                                automation.page.fill(selector, code)
                                time.sleep(1)
                                
                                # Tentar submeter
                                submit_selectors = ["text=Next", "text=Verify", "button[type='submit']"]
                                for submit_sel in submit_selectors:
                                    try:
                                        if automation.page.is_visible(submit_sel):
                                            automation.page.click(submit_sel)
                                            print("✅ Código enviado!")
                                            time.sleep(5)
                                            break
                                    except:
                                        continue
                                break
                        except:
                            continue
                    
                    # Screenshot final
                    automation.page.screenshot(path="after_2fa_submit.png")
                    print("📸 Screenshot após envio: after_2fa_submit.png")
                    
                    # Verificar se deu certo
                    final_url = automation.page.url
                    print(f"🔗 URL final: {final_url}")
                    
                    if "aistudio.google.com" in final_url and "accounts.google.com" not in final_url:
                        print("🎉 LOGIN CONCLUÍDO COM SUCESSO!")
                        automation.page.screenshot(path="login_success_final.png")
                        print("📸 Screenshot de sucesso: login_success_final.png")
                    else:
                        print("⚠️ Login pode não ter sido concluído")
                        
            else:
                print("ℹ️ Nenhum campo de 2FA detectado na página atual")
                
                # Extrair texto da página para análise
                page_text = automation.page.evaluate("""
                    () => {
                        return document.body.textContent.slice(0, 1000);
                    }
                """)
                
                print("📄 Texto da página atual:")
                print(page_text[:300] + "...")
        else:
            print("ℹ️ Não está na página de login do Google")
            automation.page.screenshot(path="current_page.png")
            print("📸 Screenshot da página atual: current_page.png")
        
        input("\nPressione Enter para finalizar...")
        automation.close_browser()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        try:
            automation.page.screenshot(path="error_screenshot.png")
            print("📸 Screenshot de erro: error_screenshot.png")
        except:
            pass

if __name__ == "__main__":
    capture_2fa_screenshot()
