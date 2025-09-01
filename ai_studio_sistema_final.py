#!/usr/bin/env python3
"""
🎉 SISTEMA AI STUDIO - VERSÃO FINAL FUNCIONANDO
✅ Resolve loop infinito da conta desconectada
✅ Login completo com 2FA automático
✅ Acesso garantido ao AI Studio
"""

import sys
import time
import os
from datetime import datetime
sys.path.append('/workspaces/replit')

from ai_studio_login_2fa import AIStudioLogin2FA
from credentials_manager import CredentialsManager

class AIStudioFinalWorking(AIStudioLogin2FA):
    
    def take_screenshot(self, name):
        """Captura screenshot com nome personalizado"""
        try:
            screenshot_dir = "/workspaces/replit/interactions/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)
            
            self.page.screenshot(path=filepath)
            print(f"📸 Screenshot: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Erro ao capturar screenshot: {e}")
            return None
    
    def check_2fa_needed(self):
        """Verifica se 2FA é necessário"""
        try:
            current_url = self.page.url
            page_content = self.page.content()
            
            twofa_indicators = [
                "challenge/dp",
                "challenge/az", 
                "challenge/ipp",
                "challenge/sl",
                "2-step",
                "verification",
                "verificação"
            ]
            
            for indicator in twofa_indicators:
                if indicator in current_url.lower() or indicator in page_content.lower():
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Erro ao verificar 2FA: {e}")
            return False

    def login_to_ai_studio(self):
        """
        🚀 LOGIN COMPLETO PARA AI STUDIO
        Fluxo testado e funcionando:
        1. Clica na conta (mesmo desconectada)
        2. Insere senha
        3. Aprova 2FA se necessário
        4. Acessa AI Studio
        """
        print("🚀 INICIANDO LOGIN AI STUDIO")
        print("=" * 40)
        
        try:
            # ETAPA 1: Ir para AI Studio
            target_url = "https://aistudio.google.com/u/3/prompts/new_chat"
            print(f"🔗 Acessando: {target_url}")
            
            self.page.goto(target_url, timeout=30000)
            time.sleep(3)
            
            current_url = self.page.url
            print(f"📍 URL inicial: {current_url}")
            self.take_screenshot("01_initial_page")
            
            # ETAPA 2: Clicar na conta (se necessário)
            if "accountchooser" in current_url:
                print("👥 Página de escolha de conta detectada")
                
                # Procurar e clicar na conta
                email = "thiago.edu511@gmail.com"
                selectors = [
                    f'text={email}',
                    f'*:has-text("{email}")',
                    '*:has-text("Thiago")'
                ]
                
                clicked = False
                for selector in selectors:
                    try:
                        elements = self.page.locator(selector)
                        if elements.count() > 0:
                            print(f"✅ Encontrada conta com seletor: {selector}")
                            self.take_screenshot(f"02_before_click_account")
                            
                            elements.first.click()
                            print("✅ Conta clicada")
                            
                            time.sleep(5)
                            current_url = self.page.url
                            
                            if "challenge/pwd" in current_url:
                                print("🎉 Progrediu para página de senha!")
                                clicked = True
                                break
                                
                    except Exception as e:
                        print(f"❌ Erro com seletor {selector}: {e}")
                        continue
                
                if not clicked:
                    print("❌ Não foi possível clicar na conta")
                    return False
            
            # ETAPA 3: Inserir senha
            if "challenge/pwd" in current_url or "password" in current_url:
                print("🔐 Inserindo senha...")
                
                credentials_manager = CredentialsManager()
                password = credentials_manager.get_password()
                
                if not password:
                    print("❌ Senha não encontrada")
                    return False
                
                self.take_screenshot("03_password_page")
                
                # Inserir senha
                password_field = self.page.locator('input[type="password"]').first
                if password_field.count() > 0:
                    password_field.clear()
                    password_field.fill(password)
                    print("✅ Senha inserida")
                    
                    self.take_screenshot("04_password_entered")
                    
                    # Enviar formulário
                    self.page.keyboard.press('Enter')
                    print("✅ Formulário enviado")
                    
                    # Aguardar processamento
                    time.sleep(5)
                    current_url = self.page.url
                    print(f"📍 URL após senha: {current_url}")
                    
                    self.take_screenshot("05_after_password")
                else:
                    print("❌ Campo de senha não encontrado")
                    return False
            
            # ETAPA 4: Verificar 2FA e aguardar se necessário
            if self.check_2fa_needed():
                print("🔐 2FA DETECTADO!")
                print("📱 Por favor, aprove no seu telefone")
                print("⏳ Aguardando aprovação automática...")
                
                self.take_screenshot("06_2fa_page")
                
                # Aguardar até 60 segundos para 2FA
                for i in range(12):  # 12 * 5 = 60 segundos
                    time.sleep(5)
                    current_url = self.page.url
                    
                    if "aistudio.google.com" in current_url:
                        print("✅ 2FA aprovado automaticamente!")
                        break
                    
                    print(f"⏳ Aguardando... ({(i+1)*5}s/60s)")
                
                self.take_screenshot("07_after_2fa")
            
            # ETAPA 5: Verificar sucesso final
            final_url = self.page.url
            print(f"📍 URL final: {final_url}")
            
            if "aistudio.google.com" in final_url:
                print("🎉 SUCESSO! AI STUDIO ACESSADO!")
                self.take_screenshot("08_success_ai_studio")
                
                # Aguardar página carregar
                time.sleep(5)
                
                # Tentar ir para o chat específico
                try:
                    chat_url = "https://aistudio.google.com/u/3/prompts/new_chat"
                    self.page.goto(chat_url, timeout=15000)
                    time.sleep(3)
                    
                    final_chat_url = self.page.url
                    print(f"📍 URL do chat: {final_chat_url}")
                    self.take_screenshot("09_final_chat")
                    
                except Exception as e:
                    print(f"⚠️ Erro ao acessar chat: {e}")
                
                return True
            else:
                print("❌ Não chegou ao AI Studio")
                print(f"URL atual: {final_url}")
                return False
                
        except Exception as e:
            print(f"❌ Erro no login: {e}")
            return False

def main():
    """Função principal - executa login completo"""
    print("🌟 SISTEMA AI STUDIO - VERSÃO FINAL")
    print("🚀 Login automático com resolução de conta desconectada")
    print("=" * 60)
    
    system = AIStudioFinalWorking(headless=True)
    
    try:
        # Inicializar navegador
        system.initialize_browser()
        print("✅ Navegador inicializado")
        
        # Executar login
        success = system.login_to_ai_studio()
        
        if success:
            print("\n" + "="*60)
            print("🎉 SISTEMA FUNCIONANDO PERFEITAMENTE!")
            print("✅ Login realizado com sucesso")
            print("✅ Conta desconectada resolvida")
            print("✅ Senha inserida automaticamente")
            print("✅ 2FA aprovado (se necessário)")
            print("✅ AI Studio acessado")
            print("💬 Sistema pronto para interações!")
            print("="*60)
            
            # Manter sessão ativa brevemente
            print("\n⏳ Mantendo sessão ativa por 30 segundos...")
            time.sleep(30)
            
        else:
            print("\n" + "="*60)
            print("😞 Login não foi completado")
            print("📸 Screenshots capturados para análise:")
            print("   • Verifique pasta /interactions/screenshots/")
            print("   • Analise as mensagens de erro acima")
            print("="*60)
            
    except Exception as e:
        print(f"\n❌ Erro geral do sistema: {e}")
        
    finally:
        try:
            system.cleanup()
            print("🔄 Navegador fechado")
        except:
            pass

if __name__ == "__main__":
    main()
