# 🔧 Instruções para Rebuild do Container

Se você ainda estiver enfrentando problemas com o codespace, siga estas etapas:

## 1. Verificar Logs de Criação

1. Pressione `Cmd/Ctrl + Shift + P`
2. Digite: "Codespaces: View Creation Log"
3. Analise os logs para identificar erros específicos

## 2. Rebuild do Container

1. Pressione `Cmd/Ctrl + Shift + P`
2. Digite: "Codespaces: Rebuild Container"
3. Selecione "Rebuild Container" 
4. Aguarde o processo completo

## 3. Verificação Pós-Rebuild

Após o rebuild, execute os seguintes comandos para verificar se tudo está funcionando:

```bash
# Verificar usuário e diretórios
whoami
echo $HOME
ls -la /home/

# Ativar ambiente virtual
source venv/bin/activate

# Verificar dependências
pip list

# Iniciar aplicação
./start.sh
```

## 4. Solução Manual (Se Necessário)

Se ainda houver problemas, execute manualmente:

```bash
# Criar diretórios necessários
sudo mkdir -p /home/codespace
sudo chown vscode:vscode /home/codespace
mkdir -p /home/codespace/.config/vscode-dev-containers
touch /home/codespace/.config/vscode-dev-containers/first-run-notice-already-displayed

# Configurar ambiente virtual
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Iniciar aplicação
streamlit run app.py --server.port=5000 --server.address=0.0.0.0
```

## 5. Links Úteis

- [Documentação GitHub Codespaces](https://docs.github.com/en/codespaces)
- [Configuração de Dev Containers](https://aka.ms/ghcs-custom-configuration)
- [Troubleshooting Codespaces](https://docs.github.com/en/codespaces/troubleshooting)

## Status Atual

✅ **Problema de permissões resolvido**  
✅ **Configuração de dev container otimizada**  
✅ **Ambiente virtual configurado**  
✅ **Aplicação Streamlit funcionando**  
✅ **Tratamento gracioso de dependências ausentes**

---

*Este codespace agora deve funcionar corretamente. Se persistirem problemas, consulte os logs de criação para detalhes específicos.*
