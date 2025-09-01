#!/usr/bin/env python3
"""
Teste da URL Específica do Chat
Testando a URL direta: https://aistudio.google.com/u/3/prompts/new_chat
"""

import sys
sys.path.append('/workspaces/replit')

from ai_studio_interaction_improved import AIStudioInteraction

def test_specific_chat_url():
    """Teste da URL específica do chat"""
    print("🎯 TESTE DA URL ESPECÍFICA DO CHAT")
    print("=" * 40)
    
    interaction = AIStudioInteraction(headless=True)
    
    try:
        # Inicializar
        print("🔧 Inicializando browser...")
        interaction.initialize_browser()
        
        # Verificar login
        print("🔑 Verificando login...")
        if not interaction.check_if_logged_in():
            print("🔑 Fazendo login...")
            if not interaction.quick_login():
                print("❌ Login falhou")
                return False
        
        print("✅ Login OK")
        
        # Testar URL específica
        specific_url = "https://aistudio.google.com/u/3/prompts/new_chat"
        print(f"🎯 Testando URL específica: {specific_url}")
        
        interaction.page.goto(specific_url, timeout=20000)
        import time
        time.sleep(5)
        
        final_url = interaction.page.url
        print(f"🔗 URL final: {final_url}")
        
        # Verificar se não foi redirecionado para login
        if "accounts.google.com" not in final_url:
            print("✅ Não redirecionado para login!")
            
            # Procurar por campo de input
            input_field = interaction.find_input_field()
            
            if input_field:
                print(f"✅ Campo de input encontrado: {input_field}")
                
                # Testar digitação
                print("⌨️ Testando digitação...")
                interaction.page.click(input_field)
                interaction.page.type(input_field, "Teste da URL específica", delay=30)
                
                # Verificar se texto foi digitado
                typed_text = interaction.page.evaluate(f"""
                    () => {{
                        const el = document.querySelector('{input_field}');
                        return el ? (el.value || el.textContent || '') : '';
                    }}
                """)
                
                if "Teste" in typed_text:
                    print("🎉 SUCESSO TOTAL! URL específica funciona perfeitamente!")
                    
                    # Screenshot de sucesso
                    interaction.take_screenshot("specific_url_success")
                    
                    # Limpar campo
                    interaction.page.evaluate(f"""
                        () => {{
                            const el = document.querySelector('{input_field}');
                            if (el) {{
                                el.value = '';
                                if (el.textContent !== undefined) el.textContent = '';
                            }}
                        }}
                    """)
                    
                    return True
                else:
                    print("⚠️ Campo encontrado mas não respondeu à digitação")
                    return False
            else:
                print("❌ Campo de input não encontrado")
                interaction.take_screenshot("no_input_field")
                return False
        else:
            print("❌ Redirecionado para login")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False
    finally:
        interaction.cleanup()

def test_complete_interaction_with_url():
    """Teste de interação completa usando a URL específica"""
    print("\n🚀 TESTE DE INTERAÇÃO COMPLETA")
    print("=" * 35)
    
    interaction = AIStudioInteraction(headless=True)
    
    try:
        message = "Olá! Me responda apenas com 'Funcionou!' se você puder me ouvir."
        print(f"💬 Pergunta: '{message}'")
        
        result = interaction.complete_interaction(message)
        
        if result and result['success']:
            print("\n🎉 INTERAÇÃO COMPLETA FUNCIONOU!")
            print(f"🤖 Resposta: {result['response'][:100]}...")
            return True
        else:
            print("\n❌ Interação completa falhou")
            return False
            
    except Exception as e:
        print(f"❌ Erro na interação completa: {e}")
        return False

def main():
    """Executa os testes com a URL específica"""
    print("🧪 TESTES COM URL ESPECÍFICA")
    print("=" * 30)
    
    # Teste 1: Acesso direto
    print("\n📋 TESTE 1: Acesso Direto à URL")
    result1 = test_specific_chat_url()
    
    # Teste 2: Interação completa
    if result1:
        print("\n📋 TESTE 2: Interação Completa")
        result2 = test_complete_interaction_with_url()
    else:
        result2 = False
    
    # Resumo
    print("\n📊 RESUMO DOS TESTES")
    print("=" * 25)
    print(f"Acesso Direto: {'✅ PASSOU' if result1 else '❌ FALHOU'}")
    print(f"Interação Completa: {'✅ PASSOU' if result2 else '❌ FALHOU'}")
    
    if result1 and result2:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema pronto para uso com URL específica!")
    elif result1:
        print("\n⚠️ Acesso funciona, mas interação completa precisa ajustes")
    else:
        print("\n❌ URL específica ainda tem problemas")

if __name__ == "__main__":
    main()
