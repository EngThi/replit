#!/bin/bash
# Script para iniciar o Streamlit
echo "🚀 Iniciando aplicação Streamlit..."
streamlit run app.py --server.port=5000 --server.address=0.0.0.0
