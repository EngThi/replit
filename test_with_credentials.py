#!/usr/bin/env python3
"""
Teste do Sistema Completo com Credenciais
"""

import sys
sys.path.append('/workspaces/replit')

from ai_studio_interaction_improved import AIStudioInteraction
from credentials_manager import CredentialsManager

def test_with_credentials():
    """Testa sistema com verificação de credenciais"""
    print("🔐 TESTE DO SISTEMA COM CREDENCIAIS")
    print("=" * 45)
    
    # Verificar credenciais primeiro
    creds = CredentialsManager()
    
    if creds.has_valid_credentials():
        print("✅ Credenciais encontradas - testando login automático")
        mode = "automático"
    else:
        print("⚠️ Credenciais não encontradas - testando login manual")
        mode = "manual"
    
    print(f"\n🎯 Modo: {mode}")
    print("-" * 30)
    
    # Teste de acesso
    interaction = AIStudioInteraction(headless=True)
    
    try:
        print("\n1️⃣ Testando acesso ao chat...")
        
        # Inicializar
        interaction.initialize_browser()
        
        # Tentar acessar chat
        if interaction.access_chat_directly():
            print("✅ Chat acessível!")
            
            # Verificar campo de input
            input_field = interaction.find_input_field()
            if input_field:
                print(f"✅ Campo de entrada encontrado: {input_field}")
                
                # Teste de digitação
                print("\n2️⃣ Testando envio de mensagem...")
                message = "Olá! Esta é uma mensagem de teste."
                
                if interaction.send_message_robust(message):
                    print("✅ Mensagem enviada com sucesso!")
                    
                    # Aguardar resposta
                    print("\n3️⃣ Aguardando resposta...")
                    response = interaction.wait_for_ai_response(timeout=30)
                    
                    if response:
                        print(f"✅ Resposta recebida: {response[:100]}...")
                        
                        # Salvar conversa
                        conversation_file = interaction.save_conversation()
                        print(f"✅ Conversa salva: {conversation_file}")
                        
                        print("\n🎉 TESTE COMPLETO: SUCESSO TOTAL!")
                        return True
                    else:
                        print("⚠️ Resposta não capturada")
                        return False
                else:
                    print("❌ Falha ao enviar mensagem")
                    return False
            else:
                print("❌ Campo de entrada não encontrado")
                return False
        else:
            print("❌ Não foi possível acessar chat")
            print(f"ℹ️ Isso é esperado em modo {mode} sem interação manual")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False
    finally:
        interaction.cleanup()

def show_setup_instructions():
    """Mostra instruções de configuração"""
    print("\n📋 CONFIGURAÇÃO RÁPIDA:")
    print("=" * 25)
    
    print("\n🔧 Para testar com credenciais:")
    print("1. Crie o arquivo: /workspaces/replit/config.json")
    print("2. Conteúdo:")
    print("""{
  "google": {
    "email": "seu_email@gmail.com",
    "password": "sua_senha"
  }
}""")
    
    print("\n⚠️ IMPORTANTE:")
    print("• Use senha de aplicativo se tiver 2FA")
    print("• Google > Conta > Segurança > Senhas de app")
    print("• Nunca commite este arquivo no git!")

def main():
    """Executa teste completo"""
    print("🚀 TESTE COMPLETO DO SISTEMA AI STUDIO")
    print("=" * 50)
    
    # Executar teste
    success = test_with_credentials()
    
    if success:
        print("\n🎉 SISTEMA FUNCIONANDO PERFEITAMENTE!")
        print("✅ Pronto para uso em produção")
    else:
        print("\n⚠️ Sistema parcialmente funcional")
        print("ℹ️ Configure credenciais para funcionamento completo")
        show_setup_instructions()

if __name__ == "__main__":
    main()
