"""
Detector automático de 2FA - Monitora e captura screenshot
"""

import time
import os
from automation import GoogleAIStudioAutomation

def monitor_for_2fa():
    """Monitora a página e detecta quando chegar na tela de 2FA"""
    print("🎯 MONITOR DE 2FA ATIVO")
    print("Vou monitorar a página e capturar screenshot quando detectar 2FA")
    print("=" * 55)
    
    # Obter credenciais
    email = os.getenv("SEU_EMAIL", "")
    password = os.getenv("SUA_SENHA", "")
    
    if not email:
        email = input("📧 Email: ")
    else:
        print(f"📧 Email: {email}")
        
    if not password:
        password = input("🔒 Senha: ")
    else:
        print("🔒 Senha: [configurada]")
    
    automation = GoogleAIStudioAutomation(headless=True, timeout_2fa=300)
    
    try:
        print("\n1. 🚀 Inicializando navegador...")
        automation.initialize_browser()
        
        print("2. 🌐 Navegando para AI Studio...")
        automation.navigate_to_ai_studio()
        
        print("3. 🔑 Iniciando login...")
        automation.start_login()
        
        print("4. 📧 Inserindo email...")
        automation.enter_email(email)
        
        print("5. 🔒 Inserindo senha...")
        automation.enter_password(password)
        
        print("6. 👀 MONITORANDO PARA 2FA...")
        
        # Monitorar por 2FA durante 3 minutos
        start_time = time.time()
        screenshot_count = 0
        
        while time.time() - start_time < 180:  # 3 minutos
            current_url = automation.page.url
            
            # Verificar indicadores de 2FA
            two_fa_indicators = [
                "2-Step Verification",
                "Verificação em duas etapas",
                "Enter code",
                "Digite o código",
                "Choose a number",
                "Escolha um número"
            ]
            
            page_text = ""
            try:
                page_text = automation.page.evaluate("""
                    () => document.body.textContent
                """)
            except:
                pass
            
            # Verificar se há indicadores de 2FA no texto
            has_2fa_text = any(indicator.lower() in page_text.lower() for indicator in two_fa_indicators)
            
            # Verificar campos de código
            code_fields = [
                "input[type='tel']",
                "input[name='totpPin']", 
                "input[id*='code']",
                "input[id*='pin']",
                "input[autocomplete='one-time-code']"
            ]
            
            has_code_field = False
            for field in code_fields:
                try:
                    if automation.page.is_visible(field, timeout=1000):
                        has_code_field = True
                        break
                except:
                    continue
            
            # Se detectou 2FA
            if has_2fa_text or has_code_field:
                screenshot_count += 1
                screenshot_name = f"2fa_detected_{screenshot_count}.png"
                
                print(f"\n🎯 2FA DETECTADO! Capturando screenshot #{screenshot_count}")
                automation.page.screenshot(path=screenshot_name, full_page=True)
                print(f"📸 Screenshot salvo: {screenshot_name}")
                
                # Extrair texto específico sobre números
                numbers_text = automation.page.evaluate("""
                    () => {
                        const text = document.body.textContent;
                        const lines = text.split('\\n');
                        const numberLines = lines.filter(line => 
                            line.includes('number') || 
                            line.includes('número') ||
                            /\\b\\d{1,2}\\b/.test(line)
                        );
                        return numberLines.join('\\n');
                    }
                """)
                
                if numbers_text:
                    print("🔢 TEXTO COM NÚMEROS DETECTADO:")
                    print("-" * 30)
                    print(numbers_text)
                    print("-" * 30)
                
                # Aguardar input do usuário
                print("\n📱 VERIFIQUE SEU CELULAR!")
                print("📸 Olhe o screenshot capturado acima")
                print("🔢 Escolha o número que aparece na tela e no seu celular")
                
                try:
                    choice = input("\n💬 Digite o número escolhido (ou 'c' para capturar novo screenshot): ")
                    
                    if choice.lower() == 'c':
                        continue
                    
                    if choice.isdigit():
                        print(f"✅ Você escolheu o número: {choice}")
                        
                        # Tentar clicar no número ou inserir código
                        try:
                            # Procurar pelo número na página
                            number_clicked = automation.page.evaluate(f"""
                                () => {{
                                    const elements = Array.from(document.querySelectorAll('*'));
                                    for (const el of elements) {{
                                        if (el.textContent.trim() === '{choice}' && el.offsetParent !== null) {{
                                            el.click();
                                            return true;
                                        }}
                                    }}
                                    return false;
                                }}
                            """)
                            
                            if number_clicked:
                                print(f"✅ Clicou no número {choice}")
                                time.sleep(3)
                                
                                # Screenshot após clicar
                                automation.page.screenshot(path=f"after_click_{choice}.png")
                                print(f"📸 Screenshot após clicar: after_click_{choice}.png")
                                
                                # Verificar se mudou de página
                                new_url = automation.page.url
                                if new_url != current_url:
                                    print("🎉 Redirecionado! 2FA pode ter sido concluído")
                                    automation.page.screenshot(path="2fa_success.png")
                                    print("📸 Screenshot final: 2fa_success.png")
                                    break
                            else:
                                print(f"⚠️ Não conseguiu clicar no número {choice}")
                                
                        except Exception as e:
                            print(f"❌ Erro ao processar número: {e}")
                    
                except KeyboardInterrupt:
                    break
            
            # Aguardar um pouco antes de verificar novamente
            time.sleep(2)
        
        print("\n⏰ Monitoramento finalizado")
        input("Pressione Enter para fechar...")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        try:
            automation.page.screenshot(path="error_final.png")
        except:
            pass
    finally:
        automation.close_browser()

if __name__ == "__main__":
    monitor_for_2fa()
