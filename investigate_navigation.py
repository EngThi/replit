"""
Investigação de Navegação no AI Studio
Para entender melhor como acessar o chat
"""

import time
import sys
sys.path.append('/workspaces/replit')

from ai_studio_login_2fa import AIStudioLogin2FA

class AIStudioInvestigation(AIStudioLogin2FA):
    def __init__(self):
        super().__init__(headless=True)
    
    def investigate_navigation(self):
        """Investiga como navegar pelo AI Studio"""
        try:
            print("🔍 INVESTIGAÇÃO DE NAVEGAÇÃO")
            print("=" * 35)
            
            # Inicializar
            self.initialize_browser()
            
            # Verificar login
            if not self.check_if_logged_in():
                print("🔑 Fazendo login...")
                self.quick_login()
            
            print("✅ Login confirmado")
            
            # Ir para página principal
            print("\n📍 Indo para página principal...")
            self.page.goto("https://aistudio.google.com/", timeout=20000)
            time.sleep(3)
            
            current_url = self.page.url
            print(f"🔗 URL atual: {current_url}")
            
            # Capturar screenshot
            self.page.screenshot(path="/workspaces/replit/investigation_main.png", full_page=True)
            print("📸 Screenshot: investigation_main.png")
            
            # Analisar elementos na página
            print("\n🔍 Analisando elementos na página...")
            
            elements_info = self.page.evaluate("""
                () => {
                    const info = {
                        links: [],
                        buttons: [],
                        forms: [],
                        special_elements: []
                    };
                    
                    // Links
                    document.querySelectorAll('a[href]').forEach((link, i) => {
                        if (i < 20) { // Limitar quantidade
                            const href = link.href;
                            const text = link.textContent.trim();
                            if (text.length > 0 && text.length < 100) {
                                info.links.push({href, text});
                            }
                        }
                    });
                    
                    // Botões
                    document.querySelectorAll('button').forEach((btn, i) => {
                        if (i < 15) {
                            const text = btn.textContent.trim();
                            const onclick = btn.onclick ? btn.onclick.toString() : '';
                            if (text.length > 0 && text.length < 50) {
                                info.buttons.push({text, onclick: onclick.substring(0, 100)});
                            }
                        }
                    });
                    
                    // Elementos especiais (que podem levar ao chat)
                    const chatKeywords = ['chat', 'new', 'create', 'prompt', 'conversation'];
                    document.querySelectorAll('*').forEach((el) => {
                        const text = el.textContent.trim().toLowerCase();
                        const classList = Array.from(el.classList).join(' ');
                        const id = el.id;
                        
                        for (const keyword of chatKeywords) {
                            if ((text.includes(keyword) || classList.includes(keyword) || id.includes(keyword)) 
                                && text.length < 100 && el.offsetParent) {
                                info.special_elements.push({
                                    tag: el.tagName,
                                    text: el.textContent.trim(),
                                    className: classList,
                                    id: id,
                                    href: el.href || ''
                                });
                                break;
                            }
                        }
                    });
                    
                    return info;
                }
            """)
            
            # Mostrar resultados
            print(f"\n📋 LINKS ENCONTRADOS ({len(elements_info['links'])}):")
            for link in elements_info['links'][:10]:
                print(f"  🔗 {link['text']} -> {link['href']}")
            
            print(f"\n🔘 BOTÕES ENCONTRADOS ({len(elements_info['buttons'])}):")
            for btn in elements_info['buttons'][:8]:
                print(f"  🔘 '{btn['text']}'")
            
            print(f"\n⭐ ELEMENTOS ESPECIAIS ({len(elements_info['special_elements'])}):")
            for elem in elements_info['special_elements'][:8]:
                print(f"  {elem['tag']}: '{elem['text'][:50]}' (class: {elem['className'][:30]})")
                if elem['href']:
                    print(f"      -> {elem['href']}")
            
            # Tentar encontrar botão/link para criar chat
            print("\n🎯 PROCURANDO FORMA DE CRIAR CHAT...")
            
            # Procurar por elementos que possam levar ao chat
            chat_buttons = self.page.evaluate("""
                () => {
                    const candidates = [];
                    const elements = document.querySelectorAll('*');
                    
                    for (const el of elements) {
                        const text = el.textContent.trim().toLowerCase();
                        const isClickable = el.tagName === 'BUTTON' || el.tagName === 'A' || el.onclick || el.href;
                        
                        if (isClickable && el.offsetParent) {
                            // Palavras-chave que indicam criação de chat
                            const keywords = ['new chat', 'create', 'start', 'new prompt', 'chat', 'begin'];
                            
                            for (const keyword of keywords) {
                                if (text.includes(keyword) && text.length < 100) {
                                    candidates.push({
                                        text: el.textContent.trim(),
                                        tag: el.tagName,
                                        href: el.href || '',
                                        className: Array.from(el.classList).join(' '),
                                        id: el.id
                                    });
                                    break;
                                }
                            }
                        }
                    }
                    
                    return candidates;
                }
            """)
            
            if chat_buttons:
                print(f"✅ Encontrados {len(chat_buttons)} candidatos para criar chat:")
                for i, btn in enumerate(chat_buttons[:5]):
                    print(f"  {i+1}. {btn['tag']}: '{btn['text']}'")
                    if btn['href']:
                        print(f"     URL: {btn['href']}")
                    if btn['className']:
                        print(f"     Class: {btn['className'][:50]}")
                
                # Tentar clicar no primeiro candidato promissor
                print(f"\n🎯 Tentando clicar no primeiro candidato...")
                
                try:
                    best_candidate = chat_buttons[0]
                    
                    # Criar seletor para o elemento
                    if best_candidate['id']:
                        selector = f"#{best_candidate['id']}"
                    elif best_candidate['className']:
                        first_class = best_candidate['className'].split()[0]
                        selector = f".{first_class}"
                    else:
                        selector = f"{best_candidate['tag'].lower()}:has-text('{best_candidate['text'][:30]}')"
                    
                    print(f"🎯 Usando seletor: {selector}")
                    
                    # Aguardar e clicar
                    self.page.wait_for_selector(selector, timeout=5000)
                    self.page.click(selector)
                    time.sleep(5)
                    
                    # Verificar nova URL
                    new_url = self.page.url
                    print(f"🔗 Nova URL: {new_url}")
                    
                    # Screenshot após click
                    self.page.screenshot(path="/workspaces/replit/investigation_after_click.png", full_page=True)
                    print("📸 Screenshot: investigation_after_click.png")
                    
                    # Verificar se chegamos ao chat
                    has_input = self.page.evaluate("""
                        () => {
                            const inputs = document.querySelectorAll('textarea, input[type="text"], [contenteditable="true"]');
                            for (const input of inputs) {
                                if (input.offsetParent && input.getBoundingClientRect().width > 100) {
                                    return true;
                                }
                            }
                            return false;
                        }
                    """)
                    
                    if has_input:
                        print("✅ SUCESSO! Campo de input encontrado no chat!")
                        return new_url
                    else:
                        print("⚠️ Clique funcionou mas sem campo de input visível")
                        
                except Exception as e:
                    print(f"❌ Erro ao clicar: {e}")
            else:
                print("❌ Nenhum candidato para criar chat encontrado")
            
            return None
            
        except Exception as e:
            print(f"❌ Erro na investigação: {e}")
            return None
        finally:
            self.cleanup()

def main():
    investigation = AIStudioInvestigation()
    result = investigation.investigate_navigation()
    
    if result:
        print(f"\n🎉 URL DO CHAT ENCONTRADA: {result}")
    else:
        print(f"\n⚠️ Investigação não encontrou caminho direto para o chat")

if __name__ == "__main__":
    main()
