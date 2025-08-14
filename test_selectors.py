"""
Script de teste para encontrar o botão de login no Google AI Studio
Este script ajuda a identificar o seletor correto para automação
"""

# Teste apenas se o Playwright estiver disponível
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("❌ Playwright não está disponível")

def test_login_button():
    """
    Testa diferentes seletores para encontrar o botão de login
    """
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright não está instalado. Instale com:")
        print("pip install playwright && playwright install chromium")
        return
    
    with sync_playwright() as p:
        print("🚀 Iniciando teste de seletores...")
        
        browser = p.chromium.launch(headless=False)  # headless=False para debug
        page = browser.new_page()
        
        try:
            # Navegar para o site
            print("🌐 Navegando para Google AI Studio...")
            page.goto("https://aistudio.google.com/")
            page.wait_for_load_state('networkidle')
            
            print("🔍 Procurando botões de login...")
            
            # Lista de seletores para testar
            selectors_to_test = [
                "text=Get started",
                "text=Sign in", 
                "text=Começar",
                "text=Entrar",
                "button:has-text('Get started')",
                "a:has-text('Get started')",
                "[data-testid*='get-started']",
                "[data-testid*='sign-in']",
                ".mdc-button:has-text('Get started')",
                "button[aria-label*='Get started']",
                "button[aria-label*='Sign in']"
            ]
            
            found_selectors = []
            
            for selector in selectors_to_test:
                try:
                    if page.is_visible(selector):
                        text = page.text_content(selector)
                        found_selectors.append({
                            'selector': selector,
                            'text': text.strip(),
                            'visible': True
                        })
                        print(f"✅ ENCONTRADO: {selector} → '{text.strip()}'")
                    else:
                        print(f"❌ Não visível: {selector}")
                except Exception as e:
                    print(f"❌ Erro com {selector}: {str(e)}")
            
            # Busca geral por botões
            print("\n🔍 Buscando todos os botões na página...")
            all_buttons = page.evaluate("""
                () => {
                    const buttons = Array.from(document.querySelectorAll('button, a, [role="button"]'));
                    return buttons.map(btn => ({
                        tag: btn.tagName,
                        text: btn.textContent.trim(),
                        id: btn.id,
                        className: btn.className,
                        ariaLabel: btn.getAttribute('aria-label'),
                        href: btn.href
                    })).filter(btn => btn.text && btn.text.length > 0);
                }
            """)
            
            print(f"\n📋 Encontrados {len(all_buttons)} botões/links:")
            for i, btn in enumerate(all_buttons[:10]):  # Mostrar apenas os primeiros 10
                print(f"  {i+1}. {btn['tag']} → '{btn['text']}' (class: {btn['className']})")
            
            # Procurar especificamente por termos de login
            login_buttons = [btn for btn in all_buttons 
                           if any(term in btn['text'].lower() 
                                 for term in ['get started', 'sign in', 'login', 'entrar', 'começar'])]
            
            print(f"\n🎯 Botões relacionados a login ({len(login_buttons)}):")
            for btn in login_buttons:
                print(f"  📌 {btn['tag']} → '{btn['text']}' (class: {btn['className']})")
            
            # Capturar screenshot
            screenshot_path = "debug_page.png"
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"\n📸 Screenshot salvo em: {screenshot_path}")
            
            # Aguardar para inspeção manual
            print("\n⏸️ Aguardando 10 segundos para inspeção manual...")
            page.wait_for_timeout(10000)
            
        except Exception as e:
            print(f"❌ Erro durante o teste: {str(e)}")
            page.screenshot(path="error_debug.png")
            
        finally:
            browser.close()
            print("✅ Teste concluído!")

if __name__ == "__main__":
    test_login_button()
