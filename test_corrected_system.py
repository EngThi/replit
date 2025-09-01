#!/usr/bin/env python3
"""
Teste do Sistema Corrigido com Login Automático
"""

import os
import sys
sys.path.append('/workspaces/replit')

from ai_studio_interaction_improved import AIStudioInteraction

def test_complete_system():
    """Teste completo do sistema corrigido"""
    print("🧪 TESTE DO SISTEMA CORRIGIDO")
    print("=" * 35)
    
    interaction = AIStudioInteraction(headless=True)
    
    try:
        # Teste com uma pergunta simples
        message = "Olá! Em uma palavra, qual é sua função?"
        print(f"💬 Pergunta de teste: '{message}'")
        
        # Executar interação completa
        result = interaction.complete_interaction(message)
        
        if result and result['success']:
            print("\n🎉 TESTE COMPLETO: SUCESSO!")
            print(f"🤖 Resposta obtida: {result['response'][:100]}...")
            print(f"📁 Arquivo salvo: {result['file']}")
            return True
        else:
            print("\n❌ TESTE COMPLETO: FALHOU")
            if result:
                print(f"ℹ️ Pergunta enviada: {result['question']}")
                print(f"ℹ️ Arquivo: {result['file']}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def test_access_only():
    """Teste apenas do acesso ao chat"""
    print("\n🔍 TESTE DE ACESSO AO CHAT")
    print("=" * 30)
    
    interaction = AIStudioInteraction(headless=True)
    
    try:
        # Inicializar
        interaction.initialize_browser()
        
        # Tentar acessar chat
        if interaction.access_chat_directly():
            print("✅ ACESSO AO CHAT: SUCESSO!")
            
            # Verificar se encontra campo de input
            input_field = interaction.find_input_field()
            if input_field:
                print(f"✅ Campo de input encontrado: {input_field}")
                return True
            else:
                print("⚠️ Chat acessível mas campo não encontrado")
                return False
        else:
            print("❌ ACESSO AO CHAT: FALHOU")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste de acesso: {e}")
        return False
    finally:
        interaction.cleanup()

def main():
    """Executa todos os testes"""
    print("🚀 BATERIA DE TESTES - SISTEMA CORRIGIDO")
    print("=" * 50)
    
    results = []
    
    # Teste 1: Acesso apenas
    result1 = test_access_only()
    results.append(("Acesso ao Chat", result1))
    
    # Teste 2: Sistema completo (apenas se o acesso funcionou)
    if result1:
        result2 = test_complete_system()
        results.append(("Sistema Completo", result2))
    else:
        print("\n⚠️ Pulando teste completo pois acesso falhou")
        results.append(("Sistema Completo", False))
    
    # Resumo
    print("\n📊 RESUMO DOS TESTES")
    print("=" * 25)
    
    for test_name, success in results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"{test_name}: {status}")
    
    total_passed = sum(1 for _, success in results if success)
    print(f"\n🎯 RESULTADO: {total_passed}/{len(results)} testes passaram")
    
    if total_passed == len(results):
        print("🎉 SISTEMA FUNCIONANDO! Pronto para uso com credenciais.")
    else:
        print("⚠️ Sistema precisa de ajustes.")

if __name__ == "__main__":
    main()
