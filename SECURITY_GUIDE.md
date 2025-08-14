# 🔐 Guia de Segurança: Como Testar a Automação com Suas Credenciais

## 🎯 **OPÇÕES DISPONÍVEIS**

### **✅ OPÇÃO 1: Variáveis de Ambiente (MAIS SEGURA)**

**Vantagens:**
- ✅ Credenciais não ficam em arquivos
- ✅ Não vão para o Git
- ✅ Seguras no ambiente

**Como usar:**
```bash
# 1. Configure as variáveis (substitua pelos seus dados):
export SEU_EMAIL="seu.email@gmail.com"
export SUA_SENHA="sua_senha_real"

# 2. Inicie a aplicação:
source venv/bin/activate
streamlit run app.py --server.port=5000 --server.address=0.0.0.0

# 3. Acesse http://localhost:5000
# Os campos já estarão preenchidos automaticamente!
```

### **✅ OPÇÃO 2: Arquivo .env (SEGURA)**

**Vantagens:**
- ✅ Reutilizável
- ✅ Não vai para Git (configurado no .gitignore)
- ✅ Fácil de gerenciar

**Como usar:**
```bash
# 1. Crie o arquivo .env:
cp .env.example .env

# 2. Edite o arquivo .env com suas credenciais:
nano .env
# ou
code .env

# 3. Instale python-dotenv:
pip install python-dotenv

# 4. A aplicação carregará automaticamente
```

### **✅ OPÇÃO 3: Interface Web (TEMPORÁRIA)**

**Vantagens:**
- ✅ Rápida para testes
- ✅ Não salva as credenciais
- ✅ Interface amigável

**Como usar:**
1. Acesse: http://localhost:5000
2. Digite email e senha nos campos
3. Clique em "🚀 Iniciar Automação"

## 🚨 **DICAS DE SEGURANÇA**

### **❌ NÃO FAÇA:**
- ❌ Não coloque credenciais diretamente no código
- ❌ Não commite arquivos com senhas
- ❌ Não compartilhe screenshots com credenciais

### **✅ FAÇA:**
- ✅ Use variáveis de ambiente
- ✅ Use arquivos .env com .gitignore
- ✅ Configure 2FA no Google (recomendado)
- ✅ Use senhas de aplicativo se tiver 2FA

## 🔐 **Para Contas com 2FA (Recomendado)**

Se sua conta Google tem 2FA ativado:

1. **Gere uma senha de aplicativo:**
   - Vá em: Google Account → Security → 2-Step Verification
   - Clique em "App passwords"
   - Gere uma senha para "Custom app"
   - Use ESSA senha na automação

2. **Configure timeout adequado:**
   - Use timeout de 60-120 segundos para 2FA
   - A automação aguardará você confirmar no celular

## 🧪 **TESTE RECOMENDADO**

**Para primeiro teste, use OPÇÃO 1:**

```bash
# Terminal 1 - Configure credenciais:
export SEU_EMAIL="seu.email@gmail.com"
export SUA_SENHA="sua_senha_ou_senha_de_app"

# Terminal 1 - Inicie aplicação:
source venv/bin/activate
streamlit run app.py --server.port=5000 --server.address=0.0.0.0
```

Depois acesse http://localhost:5000 e clique em "🚀 Iniciar Automação"

## 📱 **Fluxo Esperado**

1. **Navegação** → Google AI Studio ✅
2. **Click** → Botão "Get started" ✅  
3. **Redirecionamento** → Login Google ✅
4. **Email** → Inserção automática ✅
5. **Senha** → Inserção automática ✅
6. **2FA** → Aguardar confirmação no celular ⏳
7. **Login** → Concluído ✅

## 🆘 **Em Caso de Erro**

- Screenshot automático será salvo
- Logs detalhados na interface
- Arquivo de debug será criado

---

**🎯 Recomendação: Comece com OPÇÃO 1 (variáveis de ambiente) para teste inicial!**
