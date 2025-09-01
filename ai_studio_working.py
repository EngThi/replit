#!/usr/bin/env python3
"""
Sistema AI Studio com solução para o loop infinito
Usa Keyboard Enter em vez de click na escolha de conta
"""

import sys
import time
sys.path.append('/workspaces/replit')

from ai_studio_login_2fa import AIStudioLogin2FA
from credentials_manager import CredentialsManager

class AIStudioFixed(AIStudioLogin2FA):
    
    def handle_account_chooser_fixed(self):
        """
        Versão corrigida para escolha de conta usando Keyboard Enter
        """
        print("👥 Página de escolha de conta detectada")
        
        # Capturar screenshot da página de escolha
        screenshot_path = f"/workspaces/replit/account_chooser_page_{int(time.time())}.png"
        self.page.screenshot(path=screenshot_path)
        print(f"📸 Screenshot: {screenshot_path}")
        
        try:
            # Procurar pela conta específica
            account_text = "thiago.edu511@gmail.com"
            account_locator = self.page.locator(f'text={account_text}').first
            
            if account_locator.count() > 0:
                print(f"✅ Conta encontrada: {account_text}")
                
                # SOLUÇÃO: Usar Keyboard Enter em vez de click
                print("🎯 Usando Keyboard Enter para selecionar conta...")
                account_locator.focus()
                time.sleep(1)
                self.page.keyboard.press('Enter')
                
                print("✅ Enter pressionado na conta")
                
                # Aguardar navegação
                time.sleep(5)
                
                new_url = self.page.url
                print(f"📍 Nova URL: {new_url}")
                
                if "challenge/pwd" in new_url:
                    print("🎉 Progrediu para página de senha!")
                    screenshot_path = f"/workspaces/replit/password_page_reached_{int(time.time())}.png"
                    self.page.screenshot(path=screenshot_path)
                    print(f"📸 Screenshot: {screenshot_path}")
                    return True
                elif "accountchooser" in new_url:
                    print("⚠️ Ainda na página de escolha - problema persiste")
                    return False
                else:
                    print(f"📍 Nova página detectada: {new_url}")
                    return True
                    
            else:
                print(f"❌ Conta {account_text} não encontrada na página")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao selecionar conta: {e}")
            return False

    def complete_google_login_fixed(self):
        """
        Processo completo de login com correção para escolha de conta
        """
        try:
            credentials_manager = CredentialsManager()
            
            if not credentials_manager.has_valid_credentials():
                print("❌ Credenciais não encontradas")
                return False
            
            email = credentials_manager.get_email()
            password = credentials_manager.get_password()
            
            if not email or not password:
                print("❌ Email ou senha não encontrados nas credenciais")
                return False
            
            print(f"🔑 Iniciando login com: {email}")
            
            current_url = self.page.url
            print(f"📍 URL atual: {current_url}")
            
            # Verificar se está na página de escolha de conta
            if "accountchooser" in current_url:
                print("👥 Na página de escolha de conta")
                if not self.handle_account_chooser_fixed():
                    print("❌ Falha na escolha de conta")
                    return False
                
                # Aguardar carregar nova página
                time.sleep(3)
                current_url = self.page.url
            
            # Verificar se está na página de senha
            if "challenge/pwd" in current_url:
                print("🔐 Na página de senha")
                
                # Inserir senha
                password_field = self.page.locator('input[type="password"]').first
                if password_field.count() > 0:
                    print("✅ Campo de senha encontrado")
                    password_field.fill(password)
                    print("✅ Senha inserida")
                    
                    # Capturar screenshot antes de continuar
                    screenshot_path = f"/workspaces/replit/before_password_submit_{int(time.time())}.png"
                    self.page.screenshot(path=screenshot_path)
                    print(f"📸 Screenshot: {screenshot_path}")
                    
                    # Pressionar Enter ou clicar no botão
                    self.page.keyboard.press('Enter')
                    print("✅ Enter pressionado para enviar senha")
                    
                    # Aguardar processamento
                    time.sleep(5)
                    
                    # Capturar screenshot após envio
                    screenshot_path = f"/workspaces/replit/after_password_submit_{int(time.time())}.png"
                    self.page.screenshot(path=screenshot_path)
                    print(f"📸 Screenshot: {screenshot_path}")
                    
                    new_url = self.page.url
                    print(f"📍 URL após senha: {new_url}")
                    
                    # Verificar se precisa de 2FA
                    if self.check_2fa_needed():
                        print("🔐 2FA necessário - aguardando autorização manual")
                        return self.handle_2fa_manual()
                    
                    # Verificar se login foi bem-sucedido
                    if "aistudio.google.com" in new_url:
                        print("🎉 Login bem-sucedido!")
                        return True
                    else:
                        print(f"⚠️ Login pode ter falhado. URL: {new_url}")
                        return False
                else:
                    print("❌ Campo de senha não encontrado")
                    return False
            
            # Se chegou aqui, pode estar em outra página
            print(f"⚠️ Página inesperada: {current_url}")
            screenshot_path = f"/workspaces/replit/unexpected_page_{int(time.time())}.png"
            self.page.screenshot(path=screenshot_path)
            print(f"📸 Screenshot: {screenshot_path}")
            return False
            
        except Exception as e:
            print(f"❌ Erro no login: {e}")
            return False

    def run_complete_interaction(self):
        """
        Executa interação completa com AI Studio usando solução corrigida
        """
        print("🚀 INICIANDO SISTEMA AI STUDIO CORRIGIDO")
        print("=" * 50)
        
        try:
            self.initialize_browser()
            
            # Ir para AI Studio
            target_url = "https://aistudio.google.com/u/3/prompts/new_chat"
            print(f"🔗 Acessando: {target_url}")
            
            self.page.goto(target_url, timeout=30000)
            time.sleep(3)
            
            # Verificar se precisa fazer login
            current_url = self.page.url
            if "accounts.google.com" in current_url:
                print("🔑 Login necessário")
                if not self.complete_google_login_fixed():
                    print("❌ Falha no login")
                    return False
            
            # Verificar se chegou ao AI Studio
            time.sleep(5)
            final_url = self.page.url
            print(f"📍 URL final: {final_url}")
            
            if "aistudio.google.com" in final_url:
                print("🎉 AI STUDIO ACESSADO COM SUCESSO!")
                screenshot_path = f"/workspaces/replit/ai_studio_success_{int(time.time())}.png"
                self.page.screenshot(path=screenshot_path)
                print(f"📸 Screenshot: {screenshot_path}")
                
                # Aqui você pode adicionar interações com o AI Studio
                print("💬 Pronto para interagir com AI Studio")
                return True
            else:
                print("❌ Não chegou ao AI Studio")
                return False
                
        except Exception as e:
            print(f"❌ Erro na execução: {e}")
            return False
        finally:
            print("\n🔄 Mantendo navegador aberto para possível 2FA...")
            # Não fechar o navegador para permitir 2FA manual se necessário
            # self.cleanup()

if __name__ == "__main__":
    system = AIStudioFixed(headless=True)
    success = system.run_complete_interaction()
    
    if success:
        print("\n🎉 SISTEMA FUNCIONANDO PERFEITAMENTE!")
        print("📱 Se 2FA foi solicitado, autorize no seu telefone")
    else:
        print("\n😞 Sistema não funcionou como esperado")
        print("📸 Verifique os screenshots para debug")
