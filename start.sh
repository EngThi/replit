#!/bin/bash
# Script para iniciar o Streamlit
echo "🚀 Iniciando aplicação Streamlit..."

# Ativar ambiente virtual
source venv/bin/activate

# Verificar se as dependências estão instaladas
echo "📋 Verificando dependências..."
pip install -r requirements.txt

# Iniciar aplicação
echo "🌐 Iniciando servidor Streamlit..."
streamlit run app.py --server.port=5000 --server.address=0.0.0.0
