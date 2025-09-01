#!/usr/bin/env python3
"""
Solução para loop infinito - Múltiplas estratégias de clique
"""

import sys
import time
sys.path.append('/workspaces/replit')

from ai_studio_fixed import AIStudioInteractionFixed

def test_click_strategies():
    """Testa diferentes estratégias para clicar na conta"""
    print("🎯 TESTANDO ESTRATÉGIAS DE CLIQUE")
    print("=" * 45)
    
    interaction = AIStudioInteractionFixed(headless=True)
    
    try:
        interaction.initialize_browser()
        
        target_url = "https://aistudio.google.com/u/3/prompts/new_chat"
        print(f"🔗 Acessando: {target_url}")
        
        interaction.page.goto(target_url, timeout=20000)
        time.sleep(3)
        
        current_url = interaction.page.url
        print(f"📍 URL atual: {current_url}")
        
        if "accountchooser" in current_url:
            print("✅ Na página de escolha de conta")
            
            # Capturar screenshot inicial
            interaction.take_screenshot("before_click_strategies")
            
            # ESTRATÉGIA 1: JavaScript Click
            print("\n🎯 ESTRATÉGIA 1: JavaScript Click")
            try:
                result = interaction.page.evaluate("""
                    () => {
                        const elements = Array.from(document.querySelectorAll('*'));
                        const accountElement = elements.find(el => 
                            el.textContent && el.textContent.includes('thiago.edu511@gmail.com')
                        );
                        
                        if (accountElement) {
                            accountElement.click();
                            return 'clicked';
                        }
                        return 'not_found';
                    }
                """)
                print(f"   Resultado: {result}")
                
                if result == 'clicked':
                    time.sleep(5)
                    new_url = interaction.page.url
                    print(f"   📍 Nova URL: {new_url}")
                    
                    if new_url != current_url:
                        print("   🎉 SUCESSO! URL mudou!")
                        interaction.take_screenshot("after_js_click_success")
                        return True
                    else:
                        print("   ⚠️ URL não mudou")
                        
            except Exception as e:
                print(f"   ❌ Erro: {e}")
            
            # ESTRATÉGIA 2: Force Click no elemento pai
            print("\n🎯 ESTRATÉGIA 2: Force Click")
            try:
                # Procurar elemento clicável pai
                account_element = interaction.page.locator('text=thiago.edu511@gmail.com').first
                if account_element.count() > 0:
                    # Forçar clique
                    account_element.click(force=True)
                    print("   ✅ Force click realizado")
                    
                    time.sleep(5)
                    new_url = interaction.page.url
                    print(f"   📍 Nova URL: {new_url}")
                    
                    if new_url != current_url:
                        print("   🎉 SUCESSO! URL mudou!")
                        interaction.take_screenshot("after_force_click_success")
                        return True
                    else:
                        print("   ⚠️ URL não mudou")
                        
            except Exception as e:
                print(f"   ❌ Erro: {e}")
            
            # ESTRATÉGIA 3: Procurar elemento clicável pai
            print("\n🎯 ESTRATÉGIA 3: Elemento Pai Clicável")
            try:
                clickable_parent = interaction.page.evaluate("""
                    () => {
                        const elements = Array.from(document.querySelectorAll('*'));
                        const textElement = elements.find(el => 
                            el.textContent && el.textContent.includes('thiago.edu511@gmail.com')
                        );
                        
                        if (textElement) {
                            // Procurar pai clicável
                            let parent = textElement.parentElement;
                            while (parent) {
                                const style = window.getComputedStyle(parent);
                                if (style.cursor === 'pointer' || 
                                    parent.tagName === 'BUTTON' || 
                                    parent.tagName === 'A' ||
                                    parent.onclick ||
                                    parent.getAttribute('role') === 'button') {
                                    
                                    parent.click();
                                    return 'clicked_parent';
                                }
                                parent = parent.parentElement;
                            }
                        }
                        return 'no_clickable_parent';
                    }
                """)
                print(f"   Resultado: {clickable_parent}")
                
                if clickable_parent == 'clicked_parent':
                    time.sleep(5)
                    new_url = interaction.page.url
                    print(f"   📍 Nova URL: {new_url}")
                    
                    if new_url != current_url:
                        print("   🎉 SUCESSO! URL mudou!")
                        interaction.take_screenshot("after_parent_click_success")
                        return True
                    else:
                        print("   ⚠️ URL não mudou")
                        
            except Exception as e:
                print(f"   ❌ Erro: {e}")
            
            # ESTRATÉGIA 4: Keyboard Enter
            print("\n🎯 ESTRATÉGIA 4: Keyboard Enter")
            try:
                account_element = interaction.page.locator('text=thiago.edu511@gmail.com').first
                if account_element.count() > 0:
                    account_element.focus()
                    interaction.page.keyboard.press('Enter')
                    print("   ✅ Enter pressionado")
                    
                    time.sleep(5)
                    new_url = interaction.page.url
                    print(f"   📍 Nova URL: {new_url}")
                    
                    if new_url != current_url:
                        print("   🎉 SUCESSO! URL mudou!")
                        interaction.take_screenshot("after_enter_success")
                        return True
                    else:
                        print("   ⚠️ URL não mudou")
                        
            except Exception as e:
                print(f"   ❌ Erro: {e}")
            
            print("\n❌ TODAS AS ESTRATÉGIAS FALHARAM")
            interaction.take_screenshot("all_strategies_failed")
            
            # Capturar informações da página para debug
            page_info = interaction.page.evaluate("""
                () => {
                    return {
                        url: window.location.href,
                        title: document.title,
                        bodyText: document.body.textContent.substring(0, 500),
                        hasJavaScriptErrors: window.errors || 'none'
                    };
                }
            """)
            
            print(f"\n📋 INFO DA PÁGINA:")
            print(f"   URL: {page_info['url']}")
            print(f"   Title: {page_info['title']}")
            print(f"   Texto: {page_info['bodyText'][:100]}...")
            
            return False
            
        else:
            print("⚠️ Não está na página de escolha de conta")
            interaction.take_screenshot("not_account_chooser")
            return False
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False
    finally:
        interaction.cleanup()

if __name__ == "__main__":
    success = test_click_strategies()
    if success:
        print("\n🎉 PROBLEMA RESOLVIDO!")
    else:
        print("\n😞 Problema persiste. Verificar screenshots para mais detalhes.")
