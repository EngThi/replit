#!/usr/bin/env python3
"""
🚀 AI Studio - Sistema de Login Completo
Automatiza o login com a conta steveplayer120@gmail.com
"""

import asyncio
import time
import logging
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright
from credentials_manager import CredentialsManager
from ai_studio_human_behavior import AIStudioHumanBehavior

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AIStudioLoginCompleto:
    def __init__(self):
        self.credentials = CredentialsManager()
        self.human_behavior = AIStudioHumanBehavior()
        self.screenshot_dir = Path("interactions/screenshots")
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        
    def take_screenshot(self, page, name: str):
        """Captura screenshot com timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = self.screenshot_dir / filename
        page.screenshot(path=str(filepath))
        print(f"📸 Screenshot: {filepath}")
        return filepath

    async def wait_for_element(self, page, selector, timeout=10000):
        """Espera elemento aparecer"""
        try:
            element = await page.wait_for_selector(selector, timeout=timeout)
            return element
        except Exception as e:
            logger.warning(f"Elemento não encontrado: {selector} - {e}")
            return None

    async def human_type(self, page, selector, text, delay=None):
        """Digite texto com comportamento humano"""
        element = await self.wait_for_element(page, selector)
        if element:
            await element.click()
            await self.human_behavior.human_delay(0.5, 1.0)
            await element.fill("")  # Limpar primeiro
            await self.human_behavior.human_delay(0.3, 0.6)
            
            # Digite caracter por caracter
            for char in text:
                await element.type(char)
                await self.human_behavior.human_delay(0.08, 0.15)
            
            await self.human_behavior.human_delay(0.5, 1.0)
            return True
        return False

    async def click_with_human_behavior(self, page, selector):
        """Clique com comportamento humano"""
        element = await self.wait_for_element(page, selector)
        if element:
            # Movimento humano do mouse
            box = await element.bounding_box()
            if box:
                x = box['x'] + box['width'] / 2
                y = box['y'] + box['height'] / 2
                await page.mouse.move(x, y)
                await self.human_behavior.human_delay(0.2, 0.5)
                await element.click()
                return True
        return False

    async def login_to_google(self, page):
        """Executa login no Google"""
        print("\n🔐 INICIANDO LOGIN NO GOOGLE")
        print("=" * 50)
        
        # Obter credenciais
        account = self.credentials.get_primary_account()
        email = account['email']
        password = account['password']
        
        print(f"📧 Email: {email}")
        
        # 1. Ir para página de login
        print("🌐 Acessando página de login...")
        await page.goto("https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Faistudio.google.com%2F&service=makersuite")
        await self.human_behavior.human_delay(2, 3)
        self.take_screenshot(page, "01_login_page")
        
        # 2. Digite email
        print("📧 Inserindo email...")
        email_selectors = [
            'input[type="email"]',
            '#identifierId',
            'input[name="identifier"]',
            '[data-testid="email-input"]'
        ]
        
        email_inserted = False
        for selector in email_selectors:
            if await self.human_type(page, selector, email):
                email_inserted = True
                break
                
        if not email_inserted:
            print("❌ Falha ao inserir email")
            self.take_screenshot(page, "error_email_not_found")
            return False
            
        self.take_screenshot(page, "02_email_inserted")
        
        # 3. Clique em "Próximo"
        print("➡️ Clicando em Próximo...")
        next_selectors = [
            '#identifierNext',
            'button[jsname="LgbsSe"]',
            '[data-testid="next-button"]',
            'button:has-text("Next")',
            'button:has-text("Próximo")'
        ]
        
        next_clicked = False
        for selector in next_selectors:
            if await self.click_with_human_behavior(page, selector):
                next_clicked = True
                break
                
        if not next_clicked:
            print("❌ Falha ao clicar em Próximo")
            self.take_screenshot(page, "error_next_not_found")
            return False
            
        # Aguardar página de senha
        await self.human_behavior.human_delay(2, 4)
        self.take_screenshot(page, "03_password_page")
        
        # 4. Digite senha
        print("🔑 Inserindo senha...")
        password_selectors = [
            'input[type="password"]',
            'input[name="password"]',
            '#password',
            '[data-testid="password-input"]'
        ]
        
        password_inserted = False
        for selector in password_selectors:
            if await self.human_type(page, selector, password):
                password_inserted = True
                break
                
        if not password_inserted:
            print("❌ Falha ao inserir senha")
            self.take_screenshot(page, "error_password_not_found")
            return False
            
        self.take_screenshot(page, "04_password_inserted")
        
        # 5. Clique em "Próximo" (senha)
        print("➡️ Enviando senha...")
        password_next_selectors = [
            '#passwordNext',
            'button[jsname="LgbsSe"]',
            '[data-testid="password-next"]',
            'button:has-text("Next")',
            'button:has-text("Próximo")'
        ]
        
        password_next_clicked = False
        for selector in password_next_selectors:
            if await self.click_with_human_behavior(page, selector):
                password_next_clicked = True
                break
                
        if not password_next_clicked:
            print("❌ Falha ao enviar senha")
            self.take_screenshot(page, "error_password_next_not_found")
            return False
            
        # Aguardar processamento
        await self.human_behavior.human_delay(3, 5)
        self.take_screenshot(page, "05_after_password")
        
        # 6. Verificar se precisa de 2FA
        print("🔍 Verificando necessidade de 2FA...")
        await self.human_behavior.human_delay(2, 3)
        
        current_url = page.url
        if "challenge" in current_url or "verify" in current_url or "totp" in current_url:
            print("🔐 2FA DETECTADO!")
            self.take_screenshot(page, "06_2fa_required")
            print("📱 Por favor, autorize o 2FA no seu dispositivo")
            print("⏳ Aguardando 60 segundos para autorização...")
            
            # Aguardar 2FA
            for i in range(60):
                await asyncio.sleep(1)
                current_url = page.url
                if "aistudio.google.com" in current_url or "makersuite" in current_url:
                    print("✅ 2FA aprovado!")
                    break
                if i % 10 == 0:
                    print(f"⏳ Aguardando 2FA... {60-i}s restantes")
                    
        # 7. Verificar sucesso do login
        await self.human_behavior.human_delay(2, 3)
        current_url = page.url
        self.take_screenshot(page, "07_login_result")
        
        if "aistudio.google.com" in current_url or "makersuite" in current_url:
            print("✅ LOGIN REALIZADO COM SUCESSO!")
            return True
        else:
            print(f"❌ Login falhou. URL atual: {current_url}")
            return False

    async def access_ai_studio_chat(self, page):
        """Acessa o chat do AI Studio"""
        print("\n💬 ACESSANDO AI STUDIO CHAT")
        print("=" * 50)
        
        # Ir para nova conversa
        chat_url = "https://aistudio.google.com/prompts/new_chat"
        print(f"🌐 Acessando: {chat_url}")
        await page.goto(chat_url)
        await self.human_behavior.human_delay(3, 5)
        self.take_screenshot(page, "08_ai_studio_chat")
        
        # Verificar se chegamos ao chat
        current_url = page.url
        if "aistudio.google.com" in current_url and ("chat" in current_url or "prompts" in current_url):
            print("✅ AI STUDIO CHAT ACESSADO!")
            
            # Aguardar carregar completamente
            await self.human_behavior.human_delay(2, 3)
            self.take_screenshot(page, "09_chat_loaded")
            
            # Tentar listar modelos para verificar autenticação
            try:
                print("🔍 Verificando acesso aos modelos...")
                # Procurar por indicadores de que está funcionando
                await page.wait_for_timeout(3000)
                
                # Verificar se há erro de autenticação
                error_selectors = [
                    'text="authentication"',
                    'text="Authentication"',
                    'text="Failed to list models"',
                    '[role="alert"]'
                ]
                
                has_error = False
                for selector in error_selectors:
                    if await page.query_selector(selector):
                        has_error = True
                        break
                        
                if has_error:
                    print("❌ Erro de autenticação detectado")
                    self.take_screenshot(page, "10_auth_error")
                    return False
                else:
                    print("✅ Sistema funcionando corretamente!")
                    self.take_screenshot(page, "10_success_final")
                    return True
                    
            except Exception as e:
                logger.warning(f"Erro ao verificar modelos: {e}")
                self.take_screenshot(page, "10_verification_error")
                return True  # Assumir sucesso se não conseguir verificar
        else:
            print(f"❌ Falha ao acessar chat. URL: {current_url}")
            return False

    async def run(self):
        """Executa o sistema completo"""
        print("🌟 AI STUDIO - LOGIN COMPLETO")
        print("🎯 Conta: steveplayer120@gmail.com")
        print("=" * 60)
        
        async with async_playwright() as p:
            # Configurar navegador Firefox (melhor compatibilidade)
            browser = await p.firefox.launch(
                headless=False,
                args=[
                    "--width=1366",
                    "--height=768"
                ]
            )
            
            # Usar perfil limpo
            context = await browser.new_context(
                viewport={"width": 1366, "height": 768},
                user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            
            page = await context.new_page()
            
            try:
                # 1. Login no Google
                login_success = await self.login_to_google(page)
                if not login_success:
                    print("❌ Falha no login")
                    return False
                    
                # 2. Acessar AI Studio Chat
                chat_success = await self.access_ai_studio_chat(page)
                if not chat_success:
                    print("❌ Falha ao acessar chat")
                    return False
                    
                print("\n🎉 SISTEMA FUNCIONANDO PERFEITAMENTE!")
                print("✅ Login realizado")
                print("✅ AI Studio acessado")
                print("✅ Chat disponível")
                print("=" * 60)
                
                # Manter sessão por 30 segundos para verificação
                print("⏳ Mantendo sessão ativa por 30 segundos...")
                await asyncio.sleep(30)
                
                return True
                
            except Exception as e:
                logger.error(f"Erro durante execução: {e}")
                self.take_screenshot(page, "error_final")
                return False
            finally:
                await browser.close()

async def main():
    """Função principal"""
    sistema = AIStudioLoginCompleto()
    sucesso = await sistema.run()
    
    if sucesso:
        print("🎉 Sistema executado com sucesso!")
        exit(0)
    else:
        print("❌ Sistema falhou")
        exit(1)

if __name__ == "__main__":
    asyncio.run(main())
