#!/usr/bin/env python3
"""
Sistema AI Studio - Fluxo completo para conta desconectada
1. Clica na conta (mesmo desconectada)
2. Insere senha
3. Lida com 2FA se necessário
"""

import sys
import time
import os
import re
from datetime import datetime
sys.path.append('.')

from ai_studio_login_2fa import AIStudioLogin2FA
from credentials_manager import CredentialsManager

class AIStudioDisconnectedAccount(AIStudioLogin2FA):
    
    def _sanitize_filename(self, name):
        """Remove caracteres inválidos de um nome de arquivo."""
        return re.sub(r'[^a-zA-Z0-9_.-]', '_', name)

    def take_screenshot(self, name):
        """Captura screenshot com nome personalizado"""
        try:
            # Criar diretório se não existir
            screenshot_dir = "interactions/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            
            # Gerar nome do arquivo com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)
            
            # Capturar screenshot
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
            
            # Indicadores de 2FA
            twofa_indicators = [
                "challenge/dp",
                "challenge/az", 
                "challenge/ipp",
                "challenge/sl",
                "2-step",
                "verification",
                "verificação",
                "código",
                "code"
            ]
            
            for indicator in twofa_indicators:
                if indicator in current_url.lower() or indicator in page_content.lower():
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Erro ao verificar 2FA: {e}")
            return False
    
    def handle_disconnected_account(self):
        """
        Lida com conta que aparece como desconectada
        """
        print("🔄 Detectada conta desconectada - continuando fluxo...")
        
        try:
            # Procurar conta mesmo desconectada
            email = "thiago.edu511@gmail.com"
            
            # Tentar diferentes seletores para conta desconectada
            selectors = [
                f'text={email}',
                f'[data-email="{email}"]',
                f'*:has-text("{email}")',
                '*:has-text("Thiago")',
                '[data-identifier]',
                '.BHzsHc',  # Seletor comum para contas
                '[role="button"]'
            ]
            
            account_clicked = False
            
            for selector in selectors:
                try:
                    elements = self.page.locator(selector)
                    count = elements.count()
                    
                    if count > 0:
                        print(f"✅ Encontrado {count} elemento(s) com seletor: {selector}")
                        
                        # Tentar clicar em cada elemento encontrado
                        for i in range(min(count, 3)):  # Máximo 3 tentativas
                            try:
                                element = elements.nth(i)
                                
                                # Verificar se é visível
                                if element.is_visible():
                                    print(f"   👆 Clicando no elemento {i+1}")
                                    
                                    # Capturar screenshot antes do clique
                                    sanitized_selector = self._sanitize_filename(selector)
                                    self.take_screenshot(f"before_click_{sanitized_selector}")
                                    
                                    # Tentar diferentes métodos de clique
                                    try:
                                        element.click(timeout=5000)
                                        print(f"   ✅ Clique normal realizado")
                                    except:
                                        try:
                                            element.click(force=True)
                                            print(f"   ✅ Force click realizado")
                                        except:
                                            # Usar JavaScript como último recurso
                                            element.evaluate("el => el.click()")
                                            print(f"   ✅ JavaScript click realizado")
                                    
                                    # Aguardar resposta
                                    time.sleep(3)
                                    
                                    # Verificar se URL mudou
                                    current_url = self.page.url
                                    print(f"   📍 URL após clique: {current_url}")
                                    
                                    if "challenge" in current_url or "password" in current_url or "pwd" in current_url:
                                        print("   🎉 Progrediu para página de senha!")
                                        self.take_screenshot("progressed_to_password")
                                        account_clicked = True
                                        break
                                    elif current_url != self.page.url:
                                        print("   ✅ URL mudou - provável progresso")
                                        account_clicked = True
                                        break
                                        
                            except Exception as e:
                                print(f"   ❌ Erro no elemento {i+1}: {e}")
                                continue
                        
                        if account_clicked:
                            break
                            
                except Exception as e:
                    print(f"❌ Erro com seletor {selector}: {e}")
                    continue
            
            if account_clicked:
                print("✅ Conta clicada com sucesso!")
                return True
            else:
                print("❌ Não foi possível clicar na conta")
                # Capturar screenshot para debug
                self.take_screenshot("failed_to_click_account")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao lidar com conta desconectada: {e}")
            return False

    def handle_password_entry(self):
        """
        Insere senha na página de challenge/password
        """
        print("🔐 Inserindo senha...")
        
        try:
            credentials_manager = CredentialsManager()
            password = credentials_manager.get_password()
            
            if not password:
                print("❌ Senha não encontrada")
                return False
            
            # Capturar screenshot da página de senha
            self.take_screenshot("password_page")
            
            # Procurar campo de senha
            password_selectors = [
                'input[type="password"]',
                '#password',
                '[name="password"]',
                '[autocomplete="current-password"]',
                '.whsOnd',  # Seletor comum do Google
                'input[aria-label*="password"]',
                'input[aria-label*="senha"]'
            ]
            
            password_entered = False
            
            for selector in password_selectors:
                try:
                    field = self.page.locator(selector).first
                    if field.count() > 0 and field.is_visible():
                        print(f"✅ Campo de senha encontrado: {selector}")
                        
                        # Limpar campo e inserir senha
                        field.clear()
                        field.fill(password)
                        print("✅ Senha inserida")
                        
                        # Capturar screenshot com senha inserida
                        self.take_screenshot("password_entered")
                        
                        # Enviar formulário
                        self.page.keyboard.press('Enter')
                        print("✅ Enter pressionado")
                        
                        password_entered = True
                        break
                        
                except Exception as e:
                    print(f"❌ Erro com seletor {selector}: {e}")
                    continue
            
            if not password_entered:
                print("❌ Não foi possível inserir senha")
                return False
            
            # Aguardar processamento
            time.sleep(5)
            
            # Verificar resultado
            current_url = self.page.url
            print(f"📍 URL após senha: {current_url}")
            
            # Capturar screenshot após envio da senha
            self.take_screenshot("after_password_submit")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao inserir senha: {e}")
            return False

    def complete_login_flow(self):
        """
        Fluxo completo de login para conta desconectada
        """
        print("🚀 INICIANDO FLUXO PARA CONTA DESCONECTADA")
        print("=" * 50)
        
        try:
            # Ir para AI Studio
            target_url = "https://aistudio.google.com/u/3/prompts/new_chat"
            print(f"🔗 Acessando: {target_url}")
            
            self.page.goto(target_url, timeout=30000)
            time.sleep(3)
            
            current_url = self.page.url
            print(f"📍 URL inicial: {current_url}")
            
            # Capturar screenshot inicial
            self.take_screenshot("initial_page")
            
            # ETAPA 1: Lidar com página de escolha de conta
            if "accountchooser" in current_url:
                print("👥 Na página de escolha de conta")
                
                if not self.handle_disconnected_account():
                    print("❌ Falha ao clicar na conta")
                    return False
                
                # Aguardar nova página carregar
                time.sleep(5)
                current_url = self.page.url
                print(f"📍 URL após clicar na conta: {current_url}")
            
            # ETAPA 2: Inserir senha se necessário
            if "challenge" in current_url or "password" in current_url or "pwd" in current_url:
                print("🔐 Página de senha detectada")
                
                if not self.handle_password_entry():
                    print("❌ Falha ao inserir senha")
                    return False
                
                # Aguardar após senha
                time.sleep(5)
                current_url = self.page.url
                print(f"📍 URL após senha: {current_url}")
            
            # ETAPA 3: Verificar 2FA
            if self.check_2fa_needed():
                print("🔐 2FA NECESSÁRIO!")
                print("📱 Por favor, autorize no seu telefone")
                print("⏳ Aguardando autorização...")
                
                # Capturar screenshot da página de 2FA
                self.take_screenshot("2fa_required")
                
                # Aguardar 2FA (até 60 segundos)
                for i in range(12):  # 12 * 5 = 60 segundos
                    time.sleep(5)
                    current_url = self.page.url
                    
                    if "aistudio.google.com" in current_url:
                        print("✅ 2FA aprovado! Acesso ao AI Studio")
                        break
                    
                    print(f"⏳ Aguardando 2FA... ({(i+1)*5}s)")
                
                self.take_screenshot("after_2fa_check")
            
            # ETAPA 4: Verificar sucesso final
            final_url = self.page.url
            print(f"📍 URL final: {final_url}")
            
            if "aistudio.google.com" in final_url:
                print("🎉 SUCESSO TOTAL! AI STUDIO ACESSADO!")
                self.take_screenshot("final_success")
                
                # Aguardar página carregar completamente
                time.sleep(5)
                
                print("💬 Sistema pronto para interagir com AI Studio")
                return True
            else:
                print("⚠️ Login pode não ter sido completado")
                print(f"URL atual: {final_url}")
                return False
                
        except Exception as e:
            print(f"❌ Erro no fluxo completo: {e}")
            return False

if __name__ == "__main__":
    system = AIStudioDisconnectedAccount(headless=True)
    
    try:
        system.initialize_browser()
        success = system.complete_login_flow()
        
        if success:
            print("\n🎉 SISTEMA FUNCIONANDO PERFEITAMENTE!")
            print("🔓 Login completo realizado")
            print("📱 Se houve 2FA, ele foi aprovado")
            print("💬 AI Studio pronto para uso")
            
            # Manter navegador aberto brevemente para verificação
            print("\n⏳ Mantendo sessão ativa por 30 segundos...")
            time.sleep(30)
        else:
            print("\n😞 Algo deu errado no processo")
            print("📸 Verifique os screenshots gerados")
            print("🔍 Analise as mensagens de erro acima")
            
    except Exception as e:
        print(f"\n❌ Erro geral: {e}")
    finally:
        print("\n🔄 Finalizando...")
        system.cleanup()
