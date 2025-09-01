#!/usr/bin/env python3
"""
Debug DETALHADO da página de escolha de conta
Para entender por que o Enter não está funcionando
"""

import sys
import time
sys.path.append('/workspaces/replit')

from playwright.sync_api import sync_playwright

def debug_detailed():
    print("🔍 DEBUG DETALHADO - PÁGINA DE ESCOLHA")
    print("=" * 45)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        
        context = browser.new_context()
        page = context.new_page()
        
        try:
            print("🔗 Acessando AI Studio...")
            page.goto("https://aistudio.google.com/u/3/prompts/new_chat", timeout=20000)
            time.sleep(3)
            
            url = page.url
            print(f"📍 URL: {url}")
            
            if "accountchooser" in url:
                print("✅ Na página de escolha de conta")
                
                # Capturar screenshot inicial
                page.screenshot(path="debug_detailed_initial.png")
                print("📸 Screenshot inicial salvo")
                
                # Analisar toda a estrutura da página
                page_analysis = page.evaluate("""
                    () => {
                        const analysis = {
                            title: document.title,
                            accounts: [],
                            allClickableElements: [],
                            formElements: [],
                            buttons: [],
                            links: []
                        };
                        
                        // Procurar por elementos que contenham o email
                        const allElements = Array.from(document.querySelectorAll('*'));
                        
                        allElements.forEach(el => {
                            const text = el.textContent || '';
                            
                            // Se contém o email
                            if (text.includes('thiago.edu511@gmail.com')) {
                                analysis.accounts.push({
                                    tagName: el.tagName,
                                    text: text.trim(),
                                    id: el.id,
                                    className: Array.from(el.classList).join(' '),
                                    role: el.getAttribute('role'),
                                    tabIndex: el.tabIndex,
                                    clickable: el.onclick !== null,
                                    isButton: el.tagName === 'BUTTON',
                                    isLink: el.tagName === 'A',
                                    isFormElement: ['INPUT', 'BUTTON', 'SELECT', 'TEXTAREA'].includes(el.tagName),
                                    style: {
                                        cursor: window.getComputedStyle(el).cursor,
                                        display: window.getComputedStyle(el).display,
                                        position: window.getComputedStyle(el).position
                                    },
                                    boundingBox: el.getBoundingClientRect()
                                });
                            }
                            
                            // Elementos clicáveis em geral
                            if (el.onclick || el.tagName === 'BUTTON' || el.tagName === 'A' || 
                                window.getComputedStyle(el).cursor === 'pointer') {
                                analysis.allClickableElements.push({
                                    tagName: el.tagName,
                                    text: text.substring(0, 50),
                                    className: Array.from(el.classList).join(' ')
                                });
                            }
                        });
                        
                        // Formulários
                        document.querySelectorAll('form').forEach(form => {
                            analysis.formElements.push({
                                action: form.action,
                                method: form.method,
                                elements: form.elements.length
                            });
                        });
                        
                        // Botões
                        document.querySelectorAll('button').forEach(btn => {
                            analysis.buttons.push({
                                text: btn.textContent.trim(),
                                type: btn.type,
                                disabled: btn.disabled,
                                className: Array.from(btn.classList).join(' ')
                            });
                        });
                        
                        // Links
                        document.querySelectorAll('a').forEach(link => {
                            analysis.links.push({
                                text: link.textContent.trim(),
                                href: link.href,
                                className: Array.from(link.classList).join(' ')
                            });
                        });
                        
                        return analysis;
                    }
                """)
                
                print(f"\n📋 ANÁLISE DA PÁGINA:")
                print(f"   Título: {page_analysis['title']}")
                print(f"   Contas encontradas: {len(page_analysis['accounts'])}")
                print(f"   Elementos clicáveis: {len(page_analysis['allClickableElements'])}")
                print(f"   Formulários: {len(page_analysis['formElements'])}")
                print(f"   Botões: {len(page_analysis['buttons'])}")
                print(f"   Links: {len(page_analysis['links'])}")
                
                # Detalhar contas encontradas
                if page_analysis['accounts']:
                    print(f"\n🎯 DETALHES DAS CONTAS:")
                    for i, acc in enumerate(page_analysis['accounts']):
                        print(f"   Conta {i+1}:")
                        print(f"     Tag: {acc['tagName']}")
                        print(f"     Texto: {acc['text'][:100]}...")
                        print(f"     Classes: {acc['className'][:50]}")
                        print(f"     Role: {acc['role']}")
                        print(f"     Cursor: {acc['style']['cursor']}")
                        print(f"     Clicável: {acc['clickable']}")
                        print(f"     Botão: {acc['isButton']}")
                        print(f"     Link: {acc['isLink']}")
                        print(f"     TabIndex: {acc['tabIndex']}")
                        print(f"     BoundingBox: w={acc['boundingBox']['width']:.0f} h={acc['boundingBox']['height']:.0f}")
                        print()
                
                # Testar se consegue focar no elemento
                print("🎯 TESTANDO FOCO NO ELEMENTO...")
                focus_result = page.evaluate("""
                    () => {
                        const elements = Array.from(document.querySelectorAll('*'));
                        const accountElement = elements.find(el => 
                            el.textContent && el.textContent.includes('thiago.edu511@gmail.com')
                        );
                        
                        if (accountElement) {
                            try {
                                accountElement.focus();
                                return {
                                    success: true,
                                    focused: document.activeElement === accountElement,
                                    activeElementTag: document.activeElement.tagName,
                                    activeElementText: document.activeElement.textContent?.substring(0, 50)
                                };
                            } catch(e) {
                                return {
                                    success: false,
                                    error: e.message
                                };
                            }
                        }
                        return {success: false, error: 'Element not found'};
                    }
                """)
                
                print(f"   Resultado do foco: {focus_result}")
                
                # Se conseguiu focar, testar Enter
                if focus_result.get('success'):
                    print("\n⌨️ TESTANDO KEYBOARD ENTER...")
                    page.keyboard.press('Enter')
                    time.sleep(3)
                    
                    new_url = page.url
                    print(f"   URL após Enter: {new_url}")
                    
                    if new_url != url:
                        print("   🎉 SUCESSO! URL mudou!")
                        page.screenshot(path="debug_detailed_success.png")
                    else:
                        print("   ❌ URL não mudou")
                        page.screenshot(path="debug_detailed_failed.png")
                
                # Testar estratégia alternativa: procurar por data-identifier
                print("\n🔍 PROCURANDO ELEMENTOS COM DATA-IDENTIFIER...")
                data_elements = page.evaluate("""
                    () => {
                        const elements = [];
                        document.querySelectorAll('[data-identifier]').forEach(el => {
                            elements.push({
                                identifier: el.getAttribute('data-identifier'),
                                text: el.textContent?.substring(0, 50),
                                tagName: el.tagName,
                                clickable: window.getComputedStyle(el).cursor === 'pointer' || el.onclick
                            });
                        });
                        return elements;
                    }
                """)
                
                print(f"   Elementos com data-identifier: {len(data_elements)}")
                for elem in data_elements[:5]:
                    print(f"     {elem['identifier']}: {elem['text']} ({elem['tagName']})")
                
            else:
                print("⚠️ Não é página de escolha de conta")
                page.screenshot(path="debug_detailed_not_chooser.png")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    debug_detailed()
