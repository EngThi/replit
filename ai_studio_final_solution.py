#!/usr/bin/env python3
"""
SOLUÇÃO FINAL: Sistema AI Studio sem loop infinito
Estratégia: Acesso direto sem escolha de conta
"""

import sys
import time
sys.path.append('/workspaces/replit')

from ai_studio_login_2fa import AIStudioLogin2FA
from credentials_manager import CredentialsManager

class AIStudioFinalSolution(AIStudioLogin2FA):
    
    def bypass_account_chooser(self):
        """
        Estratégia para contornar a página de escolha de conta
        Tenta acessar diretamente a página de login
        """
        print("🔄 Tentando contornar página de escolha de conta...")
        
        try:
            # Estratégia 1: URL direta de login
            login_url = "https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Faistudio.google.com%2Fu%2F3%2Fprompts%2Fnew_chat&service=wise&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
            
            print(f"🔗 Tentando URL direta de login...")
            self.page.goto(login_url, timeout=20000)
            time.sleep(3)
            
            new_url = self.page.url
            print(f"📍 Nova URL: {new_url}")
            
            # Verificar se saiu da página de escolha
            if "accountchooser" not in new_url:
                print("✅ Contornou página de escolha!")
                return True
            else:
                print("⚠️ Ainda na página de escolha")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao contornar: {e}")
            return False
    
    def direct_email_login(self):
        """
        Login direto inserindo email na página
        """
        try:
            credentials_manager = CredentialsManager()
            
            if not credentials_manager.has_valid_credentials():
                print("❌ Credenciais não encontradas")
                return False
            
            email = credentials_manager.get_email()
            password = credentials_manager.get_password()
            
            print(f"🔑 Login direto com: {email}")
            
            current_url = self.page.url
            print(f"📍 URL atual: {current_url}")
            
            # Verificar se está na página de email
            if "signin/v2/identifier" in current_url or "email" in current_url.lower():
                print("📧 Na página de inserir email")
                
                # Procurar campo de email
                email_field = self.page.locator('input[type="email"]').first
                if email_field.count() == 0:
                    email_field = self.page.locator('input[name="identifier"]').first
                if email_field.count() == 0:
                    email_field = self.page.locator('#identifierId').first
                
                if email_field.count() > 0:
                    print("✅ Campo de email encontrado")
                    email_field.fill(email)
                    print("✅ Email inserido")
                    
                    # Screenshot antes de continuar
                    screenshot_path = f"/workspaces/replit/email_inserted_{int(time.time())}.png"
                    self.page.screenshot(path=screenshot_path)
                    print(f"📸 Screenshot: {screenshot_path}")
                    
                    # Pressionar Enter ou clicar em Próximo
                    self.page.keyboard.press('Enter')
                    print("✅ Enter pressionado")
                    
                    # Aguardar carregar página de senha
                    time.sleep(5)
                    
                    new_url = self.page.url
                    print(f"📍 URL após email: {new_url}")
                    
                    if "challenge/pwd" in new_url or "password" in new_url.lower():
                        print("🔐 Progrediu para página de senha!")
                        return self.handle_password_page(password)
                    else:
                        print(f"⚠️ Página inesperada: {new_url}")
                        return False
                else:
                    print("❌ Campo de email não encontrado")
                    return False
            else:
                print(f"⚠️ Não está na página de email: {current_url}")
                return False
                
        except Exception as e:
            print(f"❌ Erro no login direto: {e}")
            return False
    
    def handle_password_page(self, password):
        """
        Manipula a página de senha
        """
        try:
            print("🔐 Inserindo senha...")
            
            # Procurar campo de senha
            password_field = self.page.locator('input[type="password"]').first
            if password_field.count() > 0:
                print("✅ Campo de senha encontrado")
                password_field.fill(password)
                print("✅ Senha inserida")
                
                # Screenshot antes de enviar
                screenshot_path = f"/workspaces/replit/password_inserted_{int(time.time())}.png"
                self.page.screenshot(path=screenshot_path)
                print(f"📸 Screenshot: {screenshot_path}")
                
                # Enviar senha
                self.page.keyboard.press('Enter')
                print("✅ Senha enviada")
                
                # Aguardar processamento
                time.sleep(5)
                
                # Screenshot após envio
                screenshot_path = f"/workspaces/replit/after_password_{int(time.time())}.png"
                self.page.screenshot(path=screenshot_path)
                print(f"📸 Screenshot: {screenshot_path}")
                
                new_url = self.page.url
                print(f"📍 URL após senha: {new_url}")
                
                # Verificar se precisa de 2FA
                if "challenge" in new_url and "pwd" not in new_url:
                    print("🔐 2FA detectado")
                    print("📱 AUTORIZE NO SEU TELEFONE AGORA!")
                    print("⏳ Aguardando autorização por 60 segundos...")
                    
                    # Aguardar 2FA
                    for i in range(12):  # 60 segundos
                        time.sleep(5)
                        current_url = self.page.url
                        if "aistudio.google.com" in current_url:
                            print("🎉 2FA autorizado! Acesso ao AI Studio!")
                            return True
                        print(f"⏳ Aguardando... {(i+1)*5}s")
                    
                    print("⏰ Timeout de 2FA")
                    return False
                
                elif "aistudio.google.com" in new_url:
                    print("🎉 Login bem-sucedido sem 2FA!")
                    return True
                else:
                    print(f"⚠️ Resultado inesperado: {new_url}")
                    return False
            else:
                print("❌ Campo de senha não encontrado")
                return False
                
        except Exception as e:
            print(f"❌ Erro na página de senha: {e}")
            return False
    
    def run_final_solution(self):
        """
        Executa solução completa para acesso ao AI Studio
        """
        print("🚀 SOLUÇÃO FINAL - AI STUDIO SEM LOOP")
        print("=" * 50)
        
        try:
            self.initialize_browser()
            
            # Estratégia 1: Tentar URL direta do AI Studio
            print("🎯 ESTRATÉGIA 1: Acesso direto")
            target_url = "https://aistudio.google.com/u/3/prompts/new_chat"
            self.page.goto(target_url, timeout=30000)
            time.sleep(3)
            
            current_url = self.page.url
            print(f"📍 URL: {current_url}")
            
            # Se foi para página de escolha, tentar contornar
            if "accountchooser" in current_url:
                print("🔄 Detectada página de escolha - tentando contornar...")
                if self.bypass_account_chooser():
                    current_url = self.page.url
                    print(f"📍 Nova URL: {current_url}")
            
            # Se está em página de login, fazer login direto
            if "accounts.google.com" in current_url:
                print("🔑 Fazendo login direto...")
                if self.direct_email_login():
                    print("✅ Login bem-sucedido!")
                    
                    # Verificar se chegou ao AI Studio
                    time.sleep(3)
                    final_url = self.page.url
                    print(f"📍 URL final: {final_url}")
                    
                    if "aistudio.google.com" in final_url:
                        print("🎉 AI STUDIO ACESSADO COM SUCESSO!")
                        screenshot_path = f"/workspaces/replit/ai_studio_final_success_{int(time.time())}.png"
                        self.page.screenshot(path=screenshot_path)
                        print(f"📸 Screenshot: {screenshot_path}")
                        print("💬 Sistema pronto para interação!")
                        return True
                    else:
                        print("❌ Não chegou ao AI Studio")
                        return False
                else:
                    print("❌ Falha no login")
                    return False
            
            elif "aistudio.google.com" in current_url:
                print("🎉 Já logado! AI Studio acessível!")
                screenshot_path = f"/workspaces/replit/already_logged_{int(time.time())}.png"
                self.page.screenshot(path=screenshot_path)
                print(f"📸 Screenshot: {screenshot_path}")
                return True
            
            else:
                print(f"⚠️ Página inesperada: {current_url}")
                screenshot_path = f"/workspaces/replit/unexpected_{int(time.time())}.png"
                self.page.screenshot(path=screenshot_path)
                print(f"📸 Screenshot: {screenshot_path}")
                return False
                
        except Exception as e:
            print(f"❌ Erro na solução: {e}")
            return False
        finally:
            print("\n⏳ Deixando navegador aberto para possível 2FA...")
            # Manter aberto para 2FA se necessário

if __name__ == "__main__":
    solution = AIStudioFinalSolution(headless=True)
    success = solution.run_final_solution()
    
    if success:
        print("\n🎉 SUCESSO TOTAL!")
        print("🤖 AI Studio acessível e funcionando")
        print("📱 Se aparecer notificação de 2FA, autorize no telefone")
    else:
        print("\n😞 Solução não funcionou")
        print("📸 Verifique screenshots para debug")
        print("🔍 Tente executar novamente em alguns minutos")
