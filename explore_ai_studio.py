"""
Exploração Avançada do AI Studio para Encontrar Chat
"""

import time
import sys
sys.path.append('/workspaces/replit')

from ai_studio_login_2fa import AIStudioLogin2FA

class AIStudioExplorer(AIStudioLogin2FA):
    def __init__(self):
        super().__init__(headless=True)
    
    def explore_ai_studio_thoroughly(self):
        """Explora o AI Studio de forma detalhada"""
        try:
            print("🕵️ EXPLORAÇÃO DETALHADA DO AI STUDIO")
            print("=" * 45)
            
            # Inicializar
            self.initialize_browser()
            
            # Verificar login
            if not self.check_if_logged_in():
                print("🔑 Fazendo login...")
                self.quick_login()
            
            print("✅ Login confirmado")
            
            # Lista de URLs para tentar
            urls_to_explore = [
                "https://aistudio.google.com/",
                "https://aistudio.google.com/app",
                "https://makersuite.google.com/",
                "https://makersuite.google.com/app",
                "https://aistudio.google.com/workspace",
                "https://aistudio.google.com/studio"
            ]
            
            for url in urls_to_explore:
                print(f"\n🔍 EXPLORANDO: {url}")
                print("-" * 40)
                
                try:
                    self.page.goto(url, timeout=15000)
                    time.sleep(4)
                    
                    current_url = self.page.url
                    print(f"🔗 URL final: {current_url}")
                    
                    # Verificar se há redirecionamento para login
                    if "accounts.google.com" in current_url:
                        print("⚠️ Redirecionado para login - pular")
                        continue
                    
                    # Verificar se há elementos de chat
                    chat_elements = self.page.evaluate("""
                        () => {
                            const elements = [];
                            
                            // Procurar por campos de input que possam ser chat
                            document.querySelectorAll('textarea, input, [contenteditable="true"]').forEach(el => {
                                if (el.offsetParent && el.getBoundingClientRect().width > 200) {
                                    elements.push({
                                        type: 'input',
                                        tag: el.tagName,
                                        placeholder: el.placeholder || '',
                                        text: el.textContent.slice(0, 50),
                                        className: Array.from(el.classList).join(' ').slice(0, 50)
                                    });
                                }
                            });
                            
                            // Procurar por botões relacionados a chat/novo projeto
                            const chatKeywords = ['chat', 'new', 'create', 'start', 'prompt', 'text', 'conversation'];
                            document.querySelectorAll('button, a, [role="button"]').forEach(el => {
                                const text = el.textContent.trim().toLowerCase();
                                const hasKeyword = chatKeywords.some(keyword => text.includes(keyword));
                                
                                if (hasKeyword && el.offsetParent && text.length < 100) {
                                    elements.push({
                                        type: 'button',
                                        tag: el.tagName,
                                        text: el.textContent.trim(),
                                        href: el.href || '',
                                        className: Array.from(el.classList).join(' ').slice(0, 50),
                                        id: el.id
                                    });
                                }
                            });
                            
                            return elements;
                        }
                    """)
                    
                    if chat_elements:
                        print(f"✅ Encontrados {len(chat_elements)} elementos de interesse:")
                        
                        # Separar por tipo
                        inputs = [el for el in chat_elements if el['type'] == 'input']
                        buttons = [el for el in chat_elements if el['type'] == 'button']
                        
                        if inputs:
                            print(f"\n📝 CAMPOS DE INPUT ({len(inputs)}):")
                            for inp in inputs[:3]:
                                print(f"  {inp['tag']}: placeholder='{inp['placeholder']}'")
                                if inp['className']:
                                    print(f"    class='{inp['className']}'")
                        
                        if buttons:
                            print(f"\n🔘 BOTÕES RELEVANTES ({len(buttons)}):")
                            for btn in buttons[:5]:
                                print(f"  {btn['tag']}: '{btn['text']}'")
                                if btn['href']:
                                    print(f"    -> {btn['href']}")
                                if btn['className']:
                                    print(f"    class='{btn['className']}'")
                        
                        # Se encontrou campo de input, esta pode ser a página certa
                        if inputs:
                            print(f"\n🎯 PÁGINA PROMISSORA! Testando interação...")
                            
                            # Tentar usar o primeiro campo de input
                            try:
                                first_input = inputs[0]
                                
                                # Criar seletor
                                if first_input['className']:
                                    first_class = first_input['className'].split()[0]
                                    selector = f".{first_class}"
                                else:
                                    selector = first_input['tag'].lower()
                                
                                print(f"🎯 Testando seletor: {selector}")
                                
                                # Tentar clicar e digitar
                                self.page.click(selector)
                                time.sleep(1)
                                self.page.type(selector, "Teste de digitação", delay=30)
                                time.sleep(1)
                                
                                # Verificar se texto foi digitado
                                typed_text = self.page.evaluate(f"""
                                    () => {{
                                        const el = document.querySelector('{selector}');
                                        return el ? (el.value || el.textContent || '') : '';
                                    }}
                                """)
                                
                                if "Teste" in typed_text:
                                    print("✅ SUCESSO! Campo de input funcional encontrado!")
                                    print(f"🎉 URL DO CHAT: {current_url}")
                                    
                                    # Limpar campo
                                    self.page.evaluate(f"""
                                        () => {{
                                            const el = document.querySelector('{selector}');
                                            if (el) {{
                                                el.value = '';
                                                if (el.textContent !== undefined) el.textContent = '';
                                            }}
                                        }}
                                    """)
                                    
                                    # Screenshot de sucesso
                                    self.page.screenshot(path="/workspaces/replit/chat_success.png", full_page=True)
                                    print("📸 Screenshot de sucesso: chat_success.png")
                                    
                                    return current_url
                                else:
                                    print("⚠️ Campo não respondeu à digitação")
                                    
                            except Exception as e:
                                print(f"❌ Erro testando campo: {e}")
                    else:
                        print("❌ Nenhum elemento de chat encontrado")
                        
                except Exception as e:
                    print(f"❌ Erro explorando {url}: {e}")
                    
            print("\n❌ Nenhuma página de chat funcional encontrada")
            return None
            
        except Exception as e:
            print(f"❌ Erro na exploração: {e}")
            return None
        finally:
            self.cleanup()

def main():
    explorer = AIStudioExplorer()
    result = explorer.explore_ai_studio_thoroughly()
    
    if result:
        print(f"\n🎉 CHAT ENCONTRADO EM: {result}")
        print("✅ Sistema pode prosseguir com interações!")
    else:
        print(f"\n❌ Chat não encontrado nas URLs testadas")
        print("ℹ️ Pode ser necessário atualizar URLs ou estratégia de acesso")

if __name__ == "__main__":
    main()
