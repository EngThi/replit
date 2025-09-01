"""
Teste das Funcionalidades de Interação com AI Studio
Testa navegação, criação de chats, envio de mensagens
"""

import sys
import os

# Adicionar caminho do projeto
sys.path.append('/workspaces/replit')

try:
    from ai_studio_interaction_complete import AIStudioInteraction
    print("✅ Módulo de interação importado com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar: {e}")
    sys.exit(1)

def test_navigation():
    """Testa navegação básica"""
    print("\n🧪 Teste 1: Navegação para AI Studio")
    try:
        interaction = AIStudioInteraction(headless=True)
        interaction.initialize_browser()
        
        # Verificar login
        if not interaction.check_if_logged_in():
            print("⚠️ Não está logado - executando login rápido...")
            if not interaction.quick_login():
                print("❌ Login falhou")
                return False
        
        # Navegar para home
        success = interaction.navigate_to_studio_home()
        
        if success:
            print("✅ Navegação bem-sucedida")
        else:
            print("❌ Falha na navegação")
        
        interaction.cleanup()
        return success
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def test_chat_creation():
    """Testa criação de novo chat"""
    print("\n🧪 Teste 2: Criação de Novo Chat")
    try:
        interaction = AIStudioInteraction(headless=True)
        interaction.initialize_browser()
        
        # Verificar login
        if not interaction.check_if_logged_in():
            print("⚠️ Fazendo login...")
            if not interaction.quick_login():
                print("❌ Login falhou")
                return False
        
        # Navegar e criar chat
        interaction.navigate_to_studio_home()
        success = interaction.create_new_chat()
        
        if success:
            print(f"✅ Chat criado: {interaction.current_chat_url}")
        else:
            print("❌ Falha ao criar chat")
        
        interaction.cleanup()
        return success
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def test_message_input_detection():
    """Testa detecção do campo de mensagem"""
    print("\n🧪 Teste 3: Detecção de Campo de Mensagem")
    try:
        interaction = AIStudioInteraction(headless=True)
        interaction.initialize_browser()
        
        # Login e navegar
        if not interaction.check_if_logged_in():
            if not interaction.quick_login():
                print("❌ Login falhou")
                return False
        
        interaction.navigate_to_studio_home()
        interaction.create_new_chat()
        
        # Tentar encontrar campo de mensagem
        input_field = interaction.find_message_input()
        
        if input_field:
            print(f"✅ Campo de mensagem encontrado: {input_field}")
            success = True
        else:
            print("❌ Campo de mensagem não encontrado")
            success = False
        
        interaction.cleanup()
        return success
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def test_complete_interaction():
    """Testa interação completa (envio + resposta)"""
    print("\n🧪 Teste 4: Interação Completa")
    try:
        interaction = AIStudioInteraction(headless=True)
        
        # Mensagem de teste simples
        test_message = "Olá! Responda apenas 'Funcionando!' para confirmar que você recebeu esta mensagem."
        
        print(f"💬 Testando com: '{test_message}'")
        
        # Executar interação completa
        result = interaction.complete_interaction(test_message)
        
        if result and result.get('response'):
            print(f"✅ Interação completa bem-sucedida!")
            print(f"📝 Resposta recebida: {len(result['response'])} caracteres")
            success = True
        else:
            print("❌ Interação não foi concluída")
            success = False
        
        interaction.cleanup()
        return success
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def test_conversation_saving():
    """Testa salvamento de conversas"""
    print("\n🧪 Teste 5: Salvamento de Conversas")
    try:
        interaction = AIStudioInteraction(headless=True)
        interaction.initialize_browser()
        
        # Simular histórico de conversa
        interaction.conversation_history = [
            {
                'type': 'user_message',
                'content': 'Teste de mensagem',
                'timestamp': '2025-08-14T12:00:00'
            },
            {
                'type': 'ai_response', 
                'content': 'Resposta de teste',
                'timestamp': '2025-08-14T12:00:05'
            }
        ]
        
        # Salvar conversa
        conversation_file = interaction.save_conversation("teste_conversa.json")
        
        if conversation_file and os.path.exists(conversation_file):
            print(f"✅ Conversa salva: {conversation_file}")
            success = True
        else:
            print("❌ Falha ao salvar conversa")
            success = False
        
        interaction.cleanup()
        return success
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def main():
    """Executa todos os testes de interação"""
    print("🚀 INICIANDO TESTES DE INTERAÇÃO")
    print("=" * 45)
    
    tests = [
        ("Navegação", test_navigation),
        ("Criação de Chat", test_chat_creation),
        ("Detecção de Campo", test_message_input_detection),
        ("Interação Completa", test_complete_interaction),
        ("Salvamento de Conversas", test_conversation_saving)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Executando: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            
            if result:
                print(f"✅ {test_name}: PASSOU")
            else:
                print(f"❌ {test_name}: FALHOU")
                
        except Exception as e:
            print(f"❌ {test_name}: ERRO - {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 45)
    print("📊 RESUMO DOS TESTES DE INTERAÇÃO:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Total: {passed}/{len(tests)} testes passaram")
    
    if passed >= len(tests) * 0.8:  # 80% de sucesso
        print("🎉 MAIORIA DOS TESTES PASSOU!")
        print("💡 Sistema de interação está funcional")
    else:
        print("⚠️ Muitos testes falharam")
        print("💡 Verifique os erros e logs")
    
    print(f"\n📁 Verifique arquivos salvos em: /workspaces/replit/interactions/")

if __name__ == "__main__":
    main()
