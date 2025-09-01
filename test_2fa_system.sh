#!/bin/bash

# Script de teste do sistema 2FA
echo "🧪 TESTE DO SISTEMA 2FA AI STUDIO"
echo "================================="

# Verificar dependências
echo "📦 Verificando dependências..."

PYTHON_CMD="/workspaces/replit/venv/bin/python"

if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "❌ Python virtual environment não encontrado"
    exit 1
fi

if ! $PYTHON_CMD -c "import playwright" 2>/dev/null; then
    echo "❌ Playwright não instalado"
    echo "💡 Instale com: pip install playwright && playwright install"
    exit 1
fi

echo "✅ Dependências OK"

# Criar diretório de screenshots se não existir
mkdir -p /workspaces/replit/screenshots_2fa

echo ""
echo "🎯 OPÇÕES DE TESTE:"
echo "1. Login completo com 2FA automático"
echo "2. Monitor 2FA inteligente"  
echo "3. Login rápido (sessão salva)"
echo "4. Teste de detecção 2FA"

read -p "Escolha uma opção (1-4): " choice

case $choice in
    1)
        echo "🚀 Executando login completo..."
        $PYTHON_CMD /workspaces/replit/ai_studio_login_2fa.py
        ;;
    2)
        echo "🕵️ Executando monitor inteligente..."
        $PYTHON_CMD /workspaces/replit/monitor_2fa_inteligente.py
        ;;
    3)
        echo "⚡ Testando login rápido..."
        $PYTHON_CMD -c "
from ai_studio_login_2fa import AIStudioLogin2FA
login = AIStudioLogin2FA()
try:
    if login.quick_login():
        print('✅ Login rápido funcionou!')
    else:
        print('⚠️ Login rápido falhou, tente opção 1')
finally:
    login.cleanup()
"
        ;;
    4)
        echo "🔍 Teste de detecção..."
        $PYTHON_CMD -c "
from monitor_2fa_inteligente import Monitor2FA
import os
monitor = Monitor2FA()
try:
    monitor.login_system.initialize_browser()
    monitor.login_system.page.goto('https://accounts.google.com')
    context = monitor.detect_2fa_context()
    page_info = monitor.extract_page_info()
    print(f'URL: {page_info[\"url\"]}')
    print(f'Provável 2FA: {context[\"likely_2fa\"]}')
    print(f'Palavras-chave: {context[\"detected_keywords\"]}')
    monitor.capture_enhanced_screenshot('test_detection')
    print('📸 Screenshots salvos em screenshots_2fa/')
finally:
    monitor.cleanup()
"
        ;;
    *)
        echo "❌ Opção inválida"
        exit 1
        ;;
esac

echo ""
echo "✅ Teste concluído!"
echo "📁 Verifique screenshots em: /workspaces/replit/screenshots_2fa/"
echo "📊 Logs e relatórios também estão disponíveis"
