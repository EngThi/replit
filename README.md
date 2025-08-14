# 🤖 Automação Google AI Studio

Uma aplicação web interativa construída com **Streamlit** que demonstra como automatizar o processo de login no Google AI Studio usando **Playwright**.

## 🎯 Funcionalidades

- **Interface Web Amigável**: Interface construída com Streamlit
- **Automação de Login**: Automação completa do processo de login do Google
- **Suporte a 2FA**: Aguarda autenticação de dois fatores
- **Modo Demonstração**: Simula o processo quando Playwright não está disponível
- **Validação de Credenciais**: Validação de email e tratamento de erros
- **Configurações Flexíveis**: Timeout configurável para 2FA

## 🛠️ Tecnologias Utilizadas

- **Python 3.12**
- **Streamlit** - Interface web interativa
- **Playwright** - Automação de navegador (opcional)
- **Alpine Linux** - Sistema operacional do container

## 🚀 Instalação e Execução

### Método 1: Script Automático

```bash
chmod +x start.sh
./start.sh
```

### Método 2: Manual

1. **Ativar ambiente virtual:**
```bash
source venv/bin/activate
```

2. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

3. **Executar aplicação:**
```bash
streamlit run app.py --server.port=5000 --server.address=0.0.0.0
```

4. **Acessar aplicação:**
   - URL: http://localhost:5000

## 🔧 Solução para Problemas do Codespace

Este projeto foi configurado para funcionar no **GitHub Codespaces** mesmo com limitações do ambiente. Aqui estão as soluções implementadas:

### ✅ Problema de Permissões Resolvido

**Erro Original:**
```
mkdir: cannot create directory '/home/codespace': Permission denied
touch: cannot touch '/home/codespace/.config/vscode-dev-containers/first-run-notice-already-displayed': No such file or directory
```

**Soluções Aplicadas:**

1. **Criação do diretório home correto:**
```bash
sudo mkdir -p /home/codespace
sudo chown vscode:vscode /home/codespace
```

2. **Configuração do devcontainer atualizada:**
```json
{
  "remoteUser": "vscode",
  "containerEnv": {
    "HOME": "/home/vscode"
  }
}
```

3. **Instalação de dependências do sistema:**
```bash
sudo apk add --no-cache py3-pip py3-virtualenv
```

### 🎭 Tratamento Gracioso do Playwright

Como o Playwright pode não funcionar completamente no ambiente Codespaces, implementamos:

- **Detecção automática** da disponibilidade do Playwright
- **Modo demonstração** quando Playwright não está disponível
- **Mensagens de erro informativas** com instruções claras
- **Interface funcional** mesmo sem automação completa

## 📁 Estrutura do Projeto

```
replit/
├── app.py                 # Aplicação principal Streamlit
├── automation.py          # Classe de automação Playwright
├── utils.py              # Funções utilitárias
├── requirements.txt      # Dependências Python
├── start.sh             # Script de inicialização
├── pyproject.toml       # Configuração do projeto
├── .devcontainer/       # Configuração do container
│   ├── devcontainer.json
│   └── Dockerfile
└── README.md           # Esta documentação
```

## 🔐 Configuração de Credenciais

### Variáveis de Ambiente (Recomendado)

```bash
export SEU_EMAIL="seu.email@gmail.com"
export SUA_SENHA="sua_senha_segura"
```

### Interface Web

As credenciais também podem ser inseridas diretamente na interface web.

## ⚠️ Limitações Conhecidas

1. **Playwright no Codespaces**: Algumas dependências do sistema podem estar faltando
2. **Modo Headless Obrigatório**: No ambiente Replit/Codespaces
3. **2FA Manual**: Requer intervenção manual para autenticação de dois fatores

## 🎯 Funcionalidades da Interface

### Página Principal
- Formulário de credenciais
- Validação em tempo real
- Barra de progresso durante automação
- Tratamento de erros com screenshots

### Barra Lateral
- Configurações de timeout
- Informações de segurança
- Verificação de dependências
- Status do sistema

### Modo Demonstração
- Simula todo o processo de automação
- Exibe código que seria executado
- Não requer Playwright instalado

## 🔍 Resolução de Problemas

### Erro: "Playwright não está instalado"
```bash
pip install playwright
playwright install chromium
```

### Erro: "Dependências do sistema faltando"
- Use o **Modo Demonstração** na interface
- Execute em ambiente local com todas as dependências

### Erro: "Permission denied"
- Já resolvido na configuração atual
- Verifique se o usuário tem permissões adequadas

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto é para fins educacionais e demonstrativos. Use com responsabilidade e respeite os termos de uso do Google.

## 🎉 Status do Projeto

✅ **Funcionando no GitHub Codespaces**  
✅ **Interface Streamlit operacional**  
✅ **Modo demonstração implementado**  
⚠️ **Playwright opcional (dependente do ambiente)**

---

*Desenvolvido para demonstrar automação web com Python e resolver problemas comuns em ambientes containerizados.*
