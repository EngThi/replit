#!/bin/bash

# Script para testar sistema de interação do AI Studio
echo "🤖 TESTE DE INTERAÇÃO COM AI STUDIO"
echo "===================================="

# Configurar ambiente Python
PYTHON_CMD="python"

# Verificar se ambiente está configurado
if ! command -v $PYTHON_CMD &> /dev/null
then
    echo "❌ Comando Python não encontrado"
    exit 1
fi

# Criar diretório de interações se não existir
mkdir -p interactions/screenshots
mkdir -p interactions/conversations

echo ""
echo "🎯 OPÇÕES DE TESTE:"
echo "1. Teste completo do sistema de interação"
echo "2. Interação rápida (pergunta + resposta)"
echo "3. Teste apenas navegação e chat"
echo "4. Demo interativo completo"

read -p "Escolha uma opção (1-4): " choice

case $choice in
    1)
        echo "🧪 Executando testes completos..."
        $PYTHON_CMD test_interaction_system.py
        ;;
    2)
        echo "⚡ Interação rápida..."
        echo "Digite sua pergunta para o AI:"
        read -p "💬 Pergunta: " question
        
        if [ -z "$question" ]; then
            question="Olá! Como você pode me ajudar hoje?"
        fi
        
        $PYTHON_CMD -c "
import sys
sys.path.append('.')
from ai_studio_interaction_complete import AIStudioInteraction

interaction = AIStudioInteraction(headless=True)
try:
    result = interaction.complete_interaction('$question')
    if result and result.get('response'):
        print('\n✅ SUCESSO!')
        print(f'❓ Pergunta: $question')
        print(f'🤖 Resposta: {result[\"response\"][:300]}...')
    else:
        print('\n❌ Interação falhou')
finally:
    interaction.cleanup()
"
        ;;
    3)
        echo "🏠 Testando navegação e criação de chat..."
        $PYTHON_CMD -c "
import sys
sys.path.append('.')
from ai_studio_interaction_complete import AIStudioInteraction

interaction = AIStudioInteraction(headless=True)
try:
    interaction.initialize_browser()
    
    # Verificar login
    if not interaction.check_if_logged_in():
        print('🔑 Fazendo login...')
        if not interaction.quick_login():
            print('❌ Login falhou')
            exit(1)
    
    print('✅ Login OK')
    
    # Navegar
    if interaction.navigate_to_studio_home():
        print('✅ Navegação OK')
    else:
        print('❌ Navegação falhou')
        
    # Criar chat
    if interaction.create_new_chat():
        print('✅ Chat criado OK')
        print(f'🔗 URL: {interaction.current_chat_url}')
    else:
        print('❌ Criação de chat falhou')
        
    # Encontrar campo de input
    input_field = interaction.find_message_input()
    if input_field:
        print(f'✅ Campo de mensagem encontrado: {input_field}')
    else:
        print('❌ Campo de mensagem não encontrado')
        
finally:
    interaction.cleanup()
"
        ;;
    4)
        echo "🎯 Demo interativo completo..."
        $PYTHON_CMD ai_studio_interaction_complete.py
        ;;
    *)
        echo "❌ Opção inválida"
        exit 1
        ;;
esac

echo ""
echo "✅ Teste concluído!"
echo "📁 Verifique arquivos em:"
echo "   📸 Screenshots: interactions/screenshots/"
echo "   💬 Conversas: interactions/conversations/"
echo "   📊 Logs: interactions/interaction_log.json"
