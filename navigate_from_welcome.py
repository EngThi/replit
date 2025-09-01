"""
Tentativa de Navegação Interna no AI Studio
Navegando através dos elementos da página de boas-vindas
"""

import time
import sys
sys.path.append('/workspaces/replit')

from ai_studio_login_2fa import AIStudioLogin2FA

class AIStudioNavigator(AIStudioLogin2FA):
    def __init__(self):
        super().__init__(headless=True)
    
    def navigate_from_welcome_page(self):
        """Navega a partir da página de boas-vindas"""
        try:
            print("🏠 NAVEGAÇÃO A PARTIR DA PÁGINA DE BOAS-VINDAS")
            print("=" * 50)
            
            # Inicializar
            self.initialize_browser()
            
            # Verificar login
            if not self.check_if_logged_in():
                print("🔑 Fazendo login...")
                self.quick_login()
            
            print("✅ Login confirmado")
            
            # Ir para a página de boas-vindas
            print("\n📍 Navegando para página principal...")
            self.page.goto("https://aistudio.google.com/", timeout=20000)
            time.sleep(3)
            
            current_url = self.page.url
            print(f"🔗 URL atual: {current_url}")
            
            # Procurar por elementos de navegação que possam levar ao app
            print("\n🔍 Procurando elementos de navegação...")
            
            navigation_elements = self.page.evaluate("""
                () => {
                    const elements = [];
                    
                    // Procurar por todos os links e botões
                    document.querySelectorAll('a, button, [role="button"]').forEach(el => {
                        if (el.offsetParent) {
                            const text = el.textContent.trim();
                            const href = el.href || '';
                            
                            // Ignorar links externos e de login
                            if (!href.includes('accounts.google.com') && 
                                !href.includes('ai.google.dev') && 
                                text.length > 0 && text.length < 100) {
                                
                                elements.push({
                                    text: text,
                                    href: href,
                                    tag: el.tagName,
                                    className: Array.from(el.classList).join(' '),
                                    id: el.id,
                                    onclick: el.onclick ? el.onclick.toString().slice(0, 100) : ''
                                });
                            }
                        }
                    });
                    
                    return elements;
                }
            """)
            
            print(f"✅ Encontrados {len(navigation_elements)} elementos de navegação:")
            
            for i, elem in enumerate(navigation_elements[:10]):
                print(f"\n{i+1}. {elem['tag']}: '{elem['text']}'")
                if elem['href'] and not elem['href'].startswith('javascript:'):
                    print(f"   🔗 URL: {elem['href']}")
                if elem['onclick']:
                    print(f"   🖱️ onClick: {elem['onclick'][:50]}...")
                if elem['className']:
                    print(f"   🎨 Class: {elem['className'][:50]}")
            
            # Procurar especificamente por menu de navegação
            print("\n🔍 Procurando menu de navegação...")
            
            menu_found = self.page.evaluate("""
                () => {
                    // Procurar por menus, navegação, etc
                    const menuSelectors = [
                        'nav', '[role="navigation"]', '.menu', '.navbar', 
                        '.header', '.navigation', '[data-testid*="nav"]',
                        'header', '.topbar'
                    ];
                    
                    for (const selector of menuSelectors) {
                        const menu = document.querySelector(selector);
                        if (menu && menu.offsetParent) {
                            // Procurar links dentro do menu
                            const links = menu.querySelectorAll('a, button');
                            const menuLinks = [];
                            
                            links.forEach(link => {
                                if (link.offsetParent) {
                                    const text = link.textContent.trim();
                                    const href = link.href || '';
                                    
                                    if (text && !href.includes('accounts.google.com')) {
                                        menuLinks.push({
                                            text: text,
                                            href: href,
                                            selector: link.tagName.toLowerCase() + (link.id ? '#' + link.id : '') + (link.className ? '.' + Array.from(link.classList).join('.') : '')
                                        });
                                    }
                                }
                            });
                            
                            if (menuLinks.length > 0) {
                                return {
                                    found: true,
                                    selector: selector,
                                    links: menuLinks
                                };
                            }
                        }
                    }
                    
                    return {found: false};
                }
            """)
            
            if menu_found['found']:
                print(f"✅ Menu encontrado: {menu_found['selector']}")
                print(f"📋 Links no menu ({len(menu_found['links'])}):")
                
                for link in menu_found['links'][:8]:
                    print(f"  🔗 '{link['text']}' -> {link['href']}")
                
                # Tentar clicar em links promissores
                promising_keywords = ['studio', 'app', 'workspace', 'chat', 'new', 'create', 'start']
                
                for link in menu_found['links']:
                    text_lower = link['text'].lower()
                    href_lower = link['href'].lower()
                    
                    if any(keyword in text_lower or keyword in href_lower for keyword in promising_keywords):
                        print(f"\n🎯 Tentando link promissor: '{link['text']}'")
                        
                        try:
                            # Tentar clicar no link
                            if link['href'] and not link['href'].startswith('javascript:'):
                                print(f"🔗 Navegando para: {link['href']}")
                                self.page.goto(link['href'], timeout=15000)
                            else:
                                # Clicar no elemento
                                print(f"🖱️ Clicando no elemento...")
                                self.page.click(f"text={link['text']}")
                            
                            time.sleep(5)
                            
                            new_url = self.page.url
                            print(f"🔗 Nova URL: {new_url}")
                            
                            # Verificar se não foi redirecionado para login
                            if "accounts.google.com" not in new_url:
                                # Procurar por campo de input
                                has_input = self.page.evaluate("""
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
                                    print("🎉 SUCESSO! Encontrou página com campo de input!")
                                    
                                    # Screenshot de sucesso
                                    self.page.screenshot(path="/workspaces/replit/navigation_success.png", full_page=True)
                                    print("📸 Screenshot: navigation_success.png")
                                    
                                    return new_url
                                else:
                                    print("⚠️ Página carregou mas sem campo de input")
                            else:
                                print("⚠️ Redirecionado para login")
                                
                        except Exception as e:
                            print(f"❌ Erro clicando no link: {e}")
                            
                        # Voltar para página inicial para tentar próximo link
                        try:
                            self.page.goto("https://aistudio.google.com/", timeout=15000)
                            time.sleep(2)
                        except:
                            pass
            else:
                print("❌ Menu de navegação não encontrado")
            
            # Se chegou aqui, tentar abordagem mais agressiva
            print("\n🔍 Tentando abordagem alternativa...")
            
            # Procurar por qualquer elemento que possa ter JavaScript para navegação
            js_elements = self.page.evaluate("""
                () => {
                    const elements = [];
                    document.querySelectorAll('*').forEach(el => {
                        if (el.onclick || el.getAttribute('data-href') || el.getAttribute('data-url')) {
                            const text = el.textContent.trim();
                            if (text && text.length < 50 && el.offsetParent) {
                                elements.push({
                                    text: text,
                                    tag: el.tagName,
                                    onclick: el.onclick ? true : false,
                                    dataHref: el.getAttribute('data-href') || '',
                                    dataUrl: el.getAttribute('data-url') || ''
                                });
                            }
                        }
                    });
                    return elements;
                }
            """)
            
            if js_elements:
                print(f"✅ Encontrados {len(js_elements)} elementos com JavaScript:")
                for elem in js_elements[:5]:
                    print(f"  {elem['tag']}: '{elem['text']}'")
                    if elem['dataHref']:
                        print(f"    data-href: {elem['dataHref']}")
                    if elem['dataUrl']:
                        print(f"    data-url: {elem['dataUrl']}")
            
            print("\n❌ Navegação através da página de boas-vindas não foi bem-sucedida")
            return None
            
        except Exception as e:
            print(f"❌ Erro na navegação: {e}")
            return None
        finally:
            self.cleanup()

def main():
    navigator = AIStudioNavigator()
    result = navigator.navigate_from_welcome_page()
    
    if result:
        print(f"\n🎉 NAVEGAÇÃO SUCESSO! Chat em: {result}")
    else:
        print(f"\n❌ Navegação não conseguiu alcançar interface de chat")
        print("ℹ️ Pode ser necessário verificar se a conta tem acesso ao AI Studio completo")

if __name__ == "__main__":
    main()
