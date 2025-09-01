#!/usr/bin/env python3
"""
Debug - Capturar screenshot da página de escolha
Para entender o que está acontecendo
"""

import sys
sys.path.append('/workspaces/replit')

from ai_studio_fixed import AIStudioInteractionFixed

def debug_account_chooser():
    """Debug da página de escolha de conta"""
    print("🔍 DEBUG - PÁGINA DE ESCOLHA DE CONTA")
    print("=" * 45)
    
    interaction = AIStudioInteractionFixed(headless=True)
    
    try:
        interaction.initialize_browser()
        
        # Ir para URL que leva à página de escolha
        target_url = "https://aistudio.google.com/u/3/prompts/new_chat"
        print(f"🔗 Acessando: {target_url}")
        
        interaction.page.goto(target_url, timeout=20000)
        time.sleep(3)
        
        current_url = interaction.page.url
        print(f"🔗 URL atual: {current_url}")
        
        if "accountchooser" in current_url:
            print("✅ Na página de escolha de conta")
            
            # Capturar screenshot
            screenshot_path = interaction.take_screenshot("account_chooser_debug")
            print(f"📸 Screenshot capturado: {screenshot_path}")
            
            # Analisar elementos na página
            account_info = interaction.page.evaluate("""
                () => {
                    const info = {
                        accounts: [],
                        buttons: [],
                        links: [],
                        allText: document.body.textContent
                    };
                    
                    // Procurar por elementos de conta
                    document.querySelectorAll('*').forEach(el => {
                        const text = el.textContent;
                        if (text && text.includes('thiago')) {
                            info.accounts.push({
                                tag: el.tagName,
                                text: text.trim(),
                                className: Array.from(el.classList).join(' '),
                                id: el.id,
                                clickable: el.onclick || el.href || el.tagName === 'BUTTON'
                            });
                        }
                    });
                    
                    // Procurar botões
                    document.querySelectorAll('button, [role="button"], .button').forEach(btn => {
                        if (btn.offsetParent) {
                            info.buttons.push({
                                text: btn.textContent.trim(),
                                className: Array.from(btn.classList).join(' ')
                            });
                        }
                    });
                    
                    // Procurar links
                    document.querySelectorAll('a').forEach(link => {
                        if (link.offsetParent) {
                            info.links.push({
                                text: link.textContent.trim(),
                                href: link.href
                            });
                        }
                    });
                    
                    return info;
                }
            """)
            
            print(f"\n📋 CONTAS ENCONTRADAS ({len(account_info['accounts'])}):")
            for i, acc in enumerate(account_info['accounts'][:5]):
                print(f"  {i+1}. {acc['tag']}: '{acc['text'][:50]}...'")
                print(f"     Clicável: {acc['clickable']}")
                print(f"     Classes: {acc['className'][:50]}")
            
            print(f"\n🔘 BOTÕES ({len(account_info['buttons'])}):")
            for btn in account_info['buttons'][:5]:
                print(f"  • '{btn['text'][:30]}' (classes: {btn['className'][:30]})")
            
            print(f"\n🔗 LINKS ({len(account_info['links'])}):")
            for link in account_info['links'][:3]:
                print(f"  • '{link['text'][:30]}' -> {link['href'][:50]}")
            
            # Tentar clicar e capturar o que acontece
            print(f"\n🎯 Tentando clicar na conta...")
            
            try:
                # Tentar clicar de diferentes formas
                clicked = False
                
                # Método 1: Texto direto
                try:
                    interaction.page.click('text=thiago.edu511@gmail.com')
                    print("✅ Clique método 1: texto direto")
                    clicked = True
                except:
                    print("❌ Método 1 falhou")
                
                if not clicked:
                    # Método 2: Elemento visível com Thiago
                    try:
                        elements = interaction.page.query_selector_all('*:has-text("Thiago")')
                        for el in elements:
                            if el.is_visible():
                                el.click()
                                print("✅ Clique método 2: elemento com Thiago")
                                clicked = True
                                break
                    except:
                        print("❌ Método 2 falhou")
                
                if clicked:
                    print("⏳ Aguardando resultado do clique...")
                    time.sleep(5)
                    
                    new_url = interaction.page.url
                    print(f"🔗 URL após clique: {new_url}")
                    
                    if new_url != current_url:
                        print("✅ URL mudou!")
                        interaction.take_screenshot("after_account_click")
                    else:
                        print("⚠️ URL não mudou - problema identificado!")
                        interaction.take_screenshot("click_failed")
                        
                        # Verificar se há alguma mensagem de erro
                        error_info = interaction.page.evaluate("""
                            () => {
                                const errorTexts = [];
                                document.querySelectorAll('*').forEach(el => {
                                    const text = el.textContent.toLowerCase();
                                    if (text.includes('error') || text.includes('erro') || 
                                        text.includes('invalid') || text.includes('inválido') ||
                                        text.includes('incorrect') || text.includes('incorreto')) {
                                        errorTexts.push(el.textContent.trim());
                                    }
                                });
                                return errorTexts;
                            }
                        """)
                        
                        if error_info:
                            print("⚠️ POSSÍVEIS ERROS ENCONTRADOS:")
                            for error in error_info[:3]:
                                print(f"  • {error}")
                else:
                    print("❌ Não foi possível clicar na conta")
                    
            except Exception as e:
                print(f"❌ Erro ao tentar clicar: {e}")
        else:
            print("⚠️ Não está na página de escolha de conta")
            interaction.take_screenshot("unexpected_page")
            
    except Exception as e:
        print(f"❌ Erro no debug: {e}")
    finally:
        interaction.cleanup()

if __name__ == "__main__":
    import time
    debug_account_chooser()
