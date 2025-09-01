# 📱 GUIA: Como Lidar com 2FA na Automação

## 🚨 **Problema**: Código 2FA Invisível

Quando o 2FA é solicitado no modo headless, você não consegue ver o código na tela.

## ✅ **SOLUÇÕES DISPONÍVEIS**

### **🥇 SOLUÇÃO 1: Modo Interativo (RECOMENDADO)**

```bash
# Configure suas credenciais:
export SEU_EMAIL="seu.email@gmail.com"
export SUA_SENHA="sua_senha_ou_app_password"

# Execute o modo interativo:
python interactive_login.py
```

**O que acontece:**
1. ✅ Automação roda normalmente
2. 📸 Captura screenshot da tela de 2FA
3. ⌨️ Permite você digitar o código manualmente
4. ✅ Continua a automação

### **🥈 SOLUÇÃO 2: Interface Streamlit + Screenshots**

1. **Use a interface**: http://localhost:5000
2. **Quando aparecer 2FA**: A automação captura screenshot
3. **Veja o arquivo**: `2fa_page.png` 
4. **Use modo interativo**: Se necessário

### **🥉 SOLUÇÃO 3: App Password (EVITA 2FA)**

```bash
# 1. Gere App Password no Google:
# https://myaccount.google.com/security → App passwords

# 2. Use a senha de 16 dígitos:
export SUA_SENHA="abcd-efgh-ijkl-mnop"  # Senha de app
```

## 🎯 **TESTE RÁPIDO DO MODO INTERATIVO**

```bash
# Terminal 1 - Configure:
export SEU_EMAIL="seu.email@gmail.com"
export SUA_SENHA="sua_senha"

# Terminal 1 - Execute:
python interactive_login.py
```

**Fluxo do modo interativo:**
```
🚀 Automação Interativa do Google AI Studio
==================================================
📧 Email: seu.email@gmail.com
🔒 Senha: [configurada via variável de ambiente]

1. ✅ Inicializando navegador...
2. ✅ Navegando para Google AI Studio...
3. ✅ Clicando em Get started...
4. ✅ Inserindo email...
5. ✅ Inserindo senha...
6. 🔍 Verificando 2FA...
📸 Screenshot da página atual salvo em: current_page.png

📱 2FA DETECTADO!
==============================
🔍 Verifique seu celular para o código de verificação
📸 Ou olhe o arquivo 'current_page.png' para ver a tela atual

🔢 Digite o código 2FA (ou 'screenshot' para nova captura): 
```

## 📋 **Recursos do Modo Interativo**

### **✅ O que faz automaticamente:**
- Detecta campos de 2FA
- Captura screenshots da tela atual
- Aguarda sua entrada manual
- Submete o código automaticamente
- Verifica se foi aceito

### **⌨️ Comandos disponíveis:**
- **Código 2FA**: Digite os 6+ dígitos
- **`screenshot`**: Captura nova tela
- **Ctrl+C**: Cancela operação

### **📸 Screenshots gerados:**
- `current_page.png` - Tela atual
- `2fa_page.png` - Página de 2FA
- `login_success.png` - Login bem-sucedido
- `error_page.png` - Em caso de erro

## 🔄 **Workflow Completo**

```bash
# 1. Configurar
export SEU_EMAIL="seu.email@gmail.com"
export SUA_SENHA="sua_senha_ou_app_password"

# 2. Executar modo interativo
python interactive_login.py

# 3. Quando solicitar 2FA:
#    → Verificar celular
#    → Ver screenshot se necessário
#    → Digitar código
#    → Aguardar confirmação

# 4. Login concluído! 🎉
```

## 🆘 **Troubleshooting**

### **Se não detectar 2FA:**
- ✅ Screenshot é capturado mesmo assim
- ✅ Verifique `current_page.png`
- ✅ Login pode ter sido concluído

### **Se código for rejeitado:**
- ✅ Novo screenshot é capturado
- ✅ Tente novamente
- ✅ Verifique se código não expirou

### **Se der erro:**
- ✅ Screenshot de erro salvo
- ✅ Use `python interactive_login.py` novamente

---

**💡 Dica**: O modo interativo é a melhor forma de lidar com 2FA em automação headless!
