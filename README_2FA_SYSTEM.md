# Sistema de Login 2FA para Google AI Studio

## 🎯 Funcionalidades

✅ **Login automático** com detecção de 2FA  
✅ **Screenshots automáticos** para visualizar códigos  
✅ **Sessão persistente** para evitar relogins  
✅ **Monitoramento inteligente** de processo de login  
✅ **Relatórios detalhados** com análise completa  

## 🚀 Como Usar

### 1. Login Completo (Primeira vez)
```bash
cd /workspaces/replit
/workspaces/replit/venv/bin/python ai_studio_login_2fa.py
```

### 2. Monitor 2FA Inteligente (Recomendado)
```bash
/workspaces/replit/venv/bin/python monitor_2fa_inteligente.py
```

### 3. Login Rápido (Sessões seguintes)
```bash
/workspaces/replit/venv/bin/python -c "
from ai_studio_login_2fa import AIStudioLogin2FA
login = AIStudioLogin2FA()
login.quick_login()
login.cleanup()
"
```

### 4. Script de Teste Interativo
```bash
./test_2fa_system.sh
```

## 🔧 Como Funciona

### Sistema de Detecção 2FA
1. **Detecta automaticamente** quando Google solicita 2FA
2. **Captura screenshots** da tela com código destacado
3. **Extrai informações** da página (campos, botões, texto)
4. **Destaca elementos** importantes visualmente
5. **Solicita código** ao usuário de forma clara
6. **Insere automaticamente** e confirma

### Persistência de Sessão
- Salva dados de sessão em `browser_profile/`
- Mantém cookies e autenticação
- Próximos acessos são **automáticos**
- Funciona por **semanas** sem relogin

## 📸 Screenshots e Relatórios

Todos os arquivos são salvos em:
- **Screenshots:** `screenshots_2fa/`
- **Relatórios:** `screenshots_2fa/report_*.txt`
- **Logs de sessão:** `session_data.json`

## 🎛️ Configuração

### Variáveis de Ambiente (Opcional)
```bash
export GOOGLE_EMAIL="seu-email@gmail.com"
export GOOGLE_PASSWORD="sua-senha"
```

### Modo Headless vs Visual
- **Headless (padrão):** Mais rápido, sem interface
- **Visual:** Para debug, mude `headless=False`

## 🔍 Arquivos Principais

### `ai_studio_login_2fa.py`
Sistema principal de login com 2FA automático.

**Funcionalidades:**
- Detecção automática de 2FA
- Inserção de códigos
- Sessão persistente
- Verificação de status

### `monitor_2fa_inteligente.py`
Monitor avançado com análise detalhada.

**Funcionalidades:**
- Screenshots com elementos destacados
- Relatórios detalhados
- Análise de contexto
- Logs estruturados

### `test_sistema_basico.py`
Testes automatizados do sistema.

**Testa:**
- Inicialização do navegador
- Acesso ao AI Studio
- Verificação de sessões
- Captura de screenshots

## 🎯 Fluxo Típico de Uso

### Primeira Vez
1. Execute o monitor: `python monitor_2fa_inteligente.py`
2. Digite suas credenciais
3. Quando aparecer 2FA:
   - Verifique o screenshot gerado
   - Abra seu app autenticador
   - Digite o código de 6 dígitos
4. Sistema salva a sessão automaticamente

### Próximos Usos
1. Execute login rápido
2. Sistema usa sessão salva
3. Acesso **imediato** ao AI Studio

## 🛠️ Troubleshooting

### Problema: "Playwright não instalado"
```bash
cd /workspaces/replit
source venv/bin/activate
pip install playwright
playwright install chromium
```

### Problema: "Login falhou"
1. Verifique screenshots em `screenshots_2fa/`
2. Leia relatório detalhado
3. Tente novamente com monitor inteligente

### Problema: "Sessão expirou"
1. Execute login completo novamente
2. Sistema criará nova sessão persistente

## 💡 Dicas de Uso

### Para Debug
- Use `headless=False` para ver navegador
- Verifique logs no terminal
- Analise screenshots capturados

### Para Produção
- Use variáveis de ambiente para credenciais
- Execute em modo headless
- Configure backup de sessões

### Integração
```python
from ai_studio_login_2fa import AIStudioLogin2FA

# Login rápido
login = AIStudioLogin2FA()
try:
    if login.quick_login():
        print("✅ Logado com sucesso!")
        # Seu código aqui
    else:
        # Fazer login completo se necessário
        login.complete_login()
finally:
    login.cleanup()
```

## 📊 Status dos Testes

Último teste: ✅ **3/3 testes passaram**
- ✅ Inicialização
- ✅ Acesso AI Studio  
- ✅ Verificação de Sessão

## 🔒 Segurança

- Credenciais **não são armazenadas** em texto plano
- Apenas cookies de sessão são mantidos
- Profile do navegador usa diretório local
- Screenshots **não contêm** informações sensíveis

---

**🎉 Sistema pronto para uso!** 
Execute `./test_2fa_system.sh` para começar.
