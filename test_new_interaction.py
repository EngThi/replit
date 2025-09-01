#!/usr/bin/env python3
"""
Teste da Nova Versão do Sistema de Interação
"""

import os
import sys
sys.path.append('/workspaces/replit')

from ai_studio_interaction_improved import AIStudioInteraction

def test_quick_interaction():
    """Teste rápido de interação"""
    print("🎯 TESTE RÁPIDO DE INTERAÇÃO")
    print("=" * 35)
    
    interaction = AIStudioInteraction(headless=True)
    
    try:
        # Inicializar browser
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
        
        # Tentar acessar chat
        print("🎯 Acessando chat...")
        if interaction.access_chat_directly():
            print("✅ Chat acessível!")
            
            # Procurar campo de input
            print("🔍 Procurando campo de entrada...")
            input_field = interaction.find_input_field()
            
            if input_field:
                print(f"✅ Campo encontrado: {input_field}")
                
                # Teste simples de digitação (sem enviar)
                print("⌨️ Testando digitação...")
                try:
                    interaction.page.click(input_field)
                    interaction.page.type(input_field, "Teste de digitação", delay=30)
                    print("✅ Digitação funcionou!")
                    
                    # Limpar campo
                    interaction.page.evaluate(f"""
                        () => {{
                            const field = document.querySelector('{input_field}');
                            if (field) {{
                                field.value = '';
                                if (field.textContent !== undefined) field.textContent = '';
                            }}
                        }}
                    """)
                    
                    return True
                    
                except Exception as e:
                    print(f"❌ Erro na digitação: {e}")
                    return False
            else:
                print("❌ Campo de entrada não encontrado")
                return False
        else:
            print("❌ Não foi possível acessar chat")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False
    finally:
        interaction.cleanup()

def test_full_interaction():
    """Teste completo com uma pergunta simples"""
    print("\n🚀 TESTE COMPLETO DE INTERAÇÃO")
    print("=" * 40)
    
    interaction = AIStudioInteraction(headless=True)
    
    try:
        message = "Olá! Em uma palavra, qual é sua função principal?"
        print(f"💬 Pergunta: '{message}'")
        
        result = interaction.complete_interaction(message)
        
        if result and result['success']:
            print("\n🎉 TESTE COMPLETO: SUCESSO!")
            print(f"🤖 Resposta: {result['response'][:100]}...")
            return True
        else:
            print("\n⚠️ TESTE COMPLETO: FALHOU")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste completo: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🔬 BATERIA DE TESTES - SISTEMA MELHORADO")
    print("=" * 50)
    
    results = []
    
    # Teste 1: Acesso básico
    print("\n📋 TESTE 1: Acesso e Campo de Entrada")
    result1 = test_quick_interaction()
    results.append(("Acesso Básico", result1))
    
    # Teste 2: Interação completa
    print("\n📋 TESTE 2: Interação Completa")
    result2 = test_full_interaction()
    results.append(("Interação Completa", result2))
    
    # Resumo
    print("\n📊 RESUMO DOS TESTES")
    print("=" * 25)
    
    for test_name, success in results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"{test_name}: {status}")
    
    total_passed = sum(1 for _, success in results if success)
    print(f"\n🎯 RESULTADO: {total_passed}/{len(results)} testes passaram")
    
    if total_passed == len(results):
        print("🎉 TODOS OS TESTES PASSARAM! Sistema pronto para uso.")
    else:
        print("⚠️ Alguns testes falharam. Verificar logs acima.")

if __name__ == "__main__":
    main()
