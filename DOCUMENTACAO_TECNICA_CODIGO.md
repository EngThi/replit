# 🔧 DOCUMENTAÇÃO TÉCNICA: CÓDIGO E IMPLEMENTAÇÃO

## 🧠 ANÁLISE TÉCNICA DETALHADA

### 📋 CLASSE AIStudioHumanBehavior

```python
class AIStudioHumanBehavior(AIStudioLogin2FA):
    """
    Sistema avançado de automação com comportamento humano
    Herda de AIStudioLogin2FA para funcionalidades base
    """
    
    def __init__(self, headless=False):
        super().__init__(headless)
        self.human_delays = {
            'quick': (0.5, 1.5),      # Ações rápidas
            'normal': (1.0, 3.0),     # Ações normais
            'thinking': (2.0, 5.0),   # "Pensando"
            'reading': (3.0, 8.0),    # Lendo página
            'typing': (0.1, 0.3)      # Entre caracteres
        }
```

#### 🎯 MÉTODO: human_delay()
```python
def human_delay(self, delay_type='normal'):
    """
    Gera delays humanizados com variação natural
    
    Args:
        delay_type: Tipo de delay ('quick', 'normal', 'thinking', 'reading', 'typing')
    
    Returns:
        float: Tempo real do delay aplicado
    """
    min_delay, max_delay = self.human_delays[delay_type]
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)
    return delay
```

**Uso Estratégico:**
- `quick`: Movimentos rápidos de mouse
- `normal`: Cliques e navegação
- `thinking`: Pausas de reflexão
- `reading`: Simulação de leitura
- `typing`: Entre caracteres na digitação

#### 🖱️ MÉTODO: human_mouse_movement()
```python
def human_mouse_movement(self):
    """
    Simula movimento natural e errático de mouse
    Posições aleatórias com variação para parecer humano
    """
    try:
        positions = [
            (200, 300), (400, 200), (600, 400), 
            (300, 500), (500, 250), (350, 350)
        ]
        
        for _ in range(random.randint(2, 4)):
            x, y = random.choice(positions)
            # Adicionar variação
            x += random.randint(-50, 50)
            y += random.randint(-50, 50)
            
            self.page.mouse.move(x, y)
            self.human_delay('quick')
    except Exception as e:
        print(f"⚠️ Mouse movement error: {e}")
```

**Características Humanas:**
- Movimentos não lineares
- Variação aleatória de posições
- Múltiplos pontos de movimento
- Tolerância a erros

#### ⌨️ MÉTODO: human_typing()
```python
def human_typing(self, text, field_locator):
    """
    Digitação humanizada caracter por caracter
    
    Args:
        text: Texto para digitar
        field_locator: Seletor do campo de entrada
    """
    try:
        # Limpar e focar no campo
        field_locator.clear()
        self.human_delay('quick')
        field_locator.focus()
        self.human_delay('quick')
        
        # Digitar caracter por caracter
        for char in text:
            field_locator.type(char)
            # Delay variável entre caracteres
            typing_delay = random.uniform(0.05, 0.25)
            time.sleep(typing_delay)
            
            # Ocasionalmente pausar como se estivesse pensando
            if random.random() < 0.1:  # 10% chance
                self.human_delay('thinking')
        
        print(f"✅ Texto digitado humanizadamente: {text[:20]}...")
    except Exception as e:
        print(f"❌ Erro na digitação humanizada: {e}")
        # Fallback para método normal
        field_locator.fill(text)
```

**Algoritmo de Humanização:**
1. **Preparação:** Limpar e focar campo
2. **Digitação:** Caracter por caracter
3. **Variação:** Delay aleatório entre 0.05-0.25s
4. **Pausas:** 10% chance de "pensar" entre caracteres
5. **Fallback:** Método normal em caso de erro

#### 🖱️ MÉTODO: human_click()
```python
def human_click(self, locator, description="elemento"):
    """
    Clique humanizado com movimento de mouse
    
    Args:
        locator: Elemento para clicar
        description: Descrição do elemento para logs
    """
    try:
        # Mover mouse próximo ao elemento primeiro
        bbox = locator.bounding_box()
        if bbox:
            # Posição próxima mas não exata
            target_x = bbox['x'] + bbox['width'] / 2 + random.randint(-10, 10)
            target_y = bbox['y'] + bbox['height'] / 2 + random.randint(-5, 5)
            
            self.page.mouse.move(target_x, target_y)
            self.human_delay('quick')
        
        # Pequena pausa antes do clique
        self.human_delay('quick')
        
        # Realizar clique
        locator.click()
        print(f"✅ Clique humanizado em: {description}")
        
        # Pausa após clique
        self.human_delay('normal')
    except Exception as e:
        print(f"❌ Erro no clique humanizado: {e}")
        # Fallback para clique normal
        locator.click()
```

**Técnica de Humanização:**
1. **Posicionamento:** Mover mouse para próximo do elemento
2. **Imprecisão:** Adicionar variação aleatória (-10 a +10 pixels)
3. **Timing:** Pausas antes e depois do clique
4. **Feedback:** Log detalhado da ação

#### 👀 MÉTODO: simulate_page_reading()
```python
def simulate_page_reading(self):
    """
    Simula comportamento de leitura da página
    Scroll patterns que imitam usuário real
    """
    print("👀 Simulando leitura da página...")
    
    # Scroll para cima e para baixo como se estivesse lendo
    for _ in range(random.randint(2, 4)):
        scroll_amount = random.randint(100, 300)
        self.page.mouse.wheel(0, scroll_amount)
        self.human_delay('reading')
        
        # Scroll de volta
        self.page.mouse.wheel(0, -scroll_amount // 2)
        self.human_delay('thinking')
```

**Padrão de Leitura:**
- Scroll descendente (lendo)
- Pausa para "absorver" conteúdo
- Scroll ascendente parcial (revisando)
- Repetição aleatória (2-4 vezes)

---

## 🔑 SISTEMA DE CREDENCIAIS

### 📋 CLASSE CredentialsManager

```python
class CredentialsManager:
    def __init__(self):
        self.accounts = {
            'thiago.edu511@gmail.com': 'Thiagao15@',
            'steveplayer120@gmail.com': 'Thiagao15@'
        }
        self.current_account = None
        self.load_credentials()
```

#### 📧 MÉTODO: get_accounts()
```python
def get_accounts(self) -> dict:
    """
    Retorna todas as contas disponíveis
    
    Returns:
        dict: Dicionário {email: password}
    """
    return self.accounts
```

#### 🔐 MÉTODO: get_password_for_email()
```python
def get_password_for_email(self, email: str) -> Optional[str]:
    """
    Retorna senha para um email específico
    
    Args:
        email: Endereço de email
        
    Returns:
        str: Senha correspondente ou None
    """
    return self.accounts.get(email)
```

#### 🔄 MÉTODO: set_current_account()
```python
def set_current_account(self, email: str):
    """
    Define conta atual para uso
    
    Args:
        email: Email da conta a ser definida como atual
        
    Returns:
        bool: True se conta existe, False caso contrário
    """
    if email in self.accounts:
        self.current_account = email
        print(f"🔄 Conta atual: {email}")
        return True
    return False
```

---

## 🛡️ CONFIGURAÇÕES ANTI-DETECÇÃO

### 🌐 Browser Configuration

```python
# Configurações adicionais para parecer humano
system.page.add_init_script("""
    // Remover indicadores de automação
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined,
    });
    
    // Simular comportamento humano
    window.chrome = {
        runtime: {}
    };
    
    // Adicionar propriedades humanas
    Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5],
    });
""")

# Configurar viewport como desktop real
system.page.set_viewport_size({"width": 1366, "height": 768})
```

**Estratégias Implementadas:**

1. **Remoção de Webdriver Flag**
   - `navigator.webdriver = undefined`
   - Evita detecção primária de automação

2. **Simulação de Chrome Extension**
   - `window.chrome.runtime = {}`
   - Imita presença de extensões

3. **Plugins Simulados**
   - Lista falsa de plugins
   - Comportamento mais natural

4. **Viewport Realista**
   - Resolução comum de desktop
   - Não usa tamanhos suspeitos

---

## 📸 SISTEMA DE DEBUGGING

### 🖼️ MÉTODO: take_screenshot()

```python
def take_screenshot(self, name):
    """
    Captura screenshot com organização temporal
    
    Args:
        name: Nome descritivo do screenshot
        
    Returns:
        str: Caminho completo do arquivo gerado
    """
    try:
        screenshot_dir = "/workspaces/replit/interactions/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(screenshot_dir, filename)
        
        self.page.screenshot(path=filepath)
        print(f"📸 Screenshot: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"❌ Erro ao capturar screenshot: {e}")
        return None
```

**Organização de Screenshots:**
- Prefixo numérico para ordem (01_, 02_, 03_...)
- Nome descritivo da etapa
- Timestamp único (YYYYMMDD_HHMMSS)
- Diretório organizado

---

## 🔄 FLUXO DE LOGIN DETALHADO

### 📋 MÉTODO: login_with_human_behavior()

```python
def login_with_human_behavior(self):
    """
    Processo completo de login com comportamento humano
    
    Returns:
        bool: True se sucesso, False se falha
    """
```

#### Etapa 1: Navegação Natural
```python
# ETAPA 1: Chegada à página (simular usuário chegando)
target_url = "https://aistudio.google.com/"
print(f"🏠 Acessando página inicial primeiro...")

self.page.goto(target_url, timeout=30000)
self.human_delay('reading')

# Simular leitura da página inicial
self.simulate_page_reading()
self.take_screenshot("01_homepage")

# Agora ir para o chat (como usuário real faria)
print("🔗 Navegando para o chat...")
chat_url = "https://aistudio.google.com/u/3/prompts/new_chat"
self.page.goto(chat_url, timeout=30000)
self.human_delay('reading')
```

#### Etapa 2: Detecção de Contas
```python
if "accountchooser" in current_url:
    print("👥 Escolhendo conta...")
    
    # Simular olhando as opções
    self.simulate_page_reading()
    
    # Lista de contas para tentar
    accounts = [
        "thiago.edu511@gmail.com",
        "steveplayer120@gmail.com"
    ]
    
    account_found = False
    for email in accounts:
        print(f"👀 Procurando conta: {email}")
        account_locator = self.page.locator(f'text={email}').first
        
        if account_locator.count() > 0 and account_locator.is_visible():
            print(f"✅ Conta encontrada: {email}")
            self.take_screenshot(f"03_before_account_click_{email.split('@')[0]}")
            
            # Clique humanizado
            self.human_click(account_locator, f"conta {email}")
            account_found = True
            
            # Aguardar carregamento
            self.human_delay('reading')
            current_url = self.page.url
            print(f"📍 Após clique na conta: {current_url}")
            break
```

#### Etapa 3: Detecção de Senha Inteligente
```python
# Verificar se há campo de senha visível (independente da URL)
password_field = self.page.locator('input[type="password"]').first

if password_field.count() > 0 and password_field.is_visible():
    print("🔐 Página de senha detectada! Inserindo senha humanamente...")
    
    credentials_manager = CredentialsManager()
    
    # Determinar qual conta estamos usando baseado na URL ou contexto
    current_url = self.page.url
    current_account = None
    
    # Verificar se conseguimos identificar a conta na página
    for email in credentials_manager.get_accounts().keys():
        if email.split('@')[0] in current_url or email in self.page.content():
            current_account = email
            break
    
    # Se não identificou, usar primeira disponível
    if not current_account:
        current_account = credentials_manager.get_email()
    
    password = credentials_manager.get_password_for_email(current_account)
    
    if password:
        print(f"🔑 Usando conta: {current_account}")
        credentials_manager.set_current_account(current_account)
```

#### Etapa 4: Digitação Humanizada
```python
# Digitação humanizada
print("⌨️ Digitando senha humanamente...")
self.human_typing(password, password_field)

self.take_screenshot("05_password_entered")

# Pausa antes de enviar (como usuário pensando)
print("💭 Pausa antes de enviar...")
self.human_delay('thinking')

# Enter humanizado
print("⏎ Enviando senha...")
self.page.keyboard.press('Enter')
print("✅ Senha enviada")
```

#### Etapa 5: Verificação Final
```python
# Aguardar até 30 segundos para carregar
for i in range(6):
    self.human_delay('normal')
    current_url = self.page.url
    
    if "aistudio.google.com" in current_url and "accounts.google.com" not in current_url:
        print(f"✅ Carregou AI Studio: {current_url}")
        break
    
    print(f"⏳ Aguardando... ({i+1}/6)")
```

---

## 🎯 ALGORITMOS ESPECÍFICOS

### 🧮 ALGORITMO DE DELAY HUMANIZADO

```python
def calculate_human_delay(action_type, base_delay):
    """
    Calcula delay baseado em distribuição normal
    Simula variabilidade humana real
    """
    if action_type == 'typing':
        # Distribuição normal para digitação
        mean = 0.15  # 150ms médio entre caracteres
        std_dev = 0.05  # Desvio padrão pequeno
        delay = max(0.05, random.normalvariate(mean, std_dev))
    
    elif action_type == 'mouse':
        # Delay de movimento de mouse
        mean = 0.8
        std_dev = 0.3
        delay = max(0.3, random.normalvariate(mean, std_dev))
    
    elif action_type == 'thinking':
        # Pausas de reflexão mais longas
        mean = 3.0
        std_dev = 1.0
        delay = max(1.0, random.normalvariate(mean, std_dev))
    
    return delay
```

### 🎯 ALGORITMO DE DETECÇÃO CONTEXTUAL

```python
def detect_page_context(page_content, url):
    """
    Detecta contexto da página para ação apropriada
    
    Args:
        page_content: Conteúdo HTML da página
        url: URL atual
        
    Returns:
        str: Contexto detectado ('login', 'password', 'chat', '2fa', etc.)
    """
    contexts = {
        'accountchooser': ['accountchooser', 'choose account'],
        'password': ['password', 'senha', 'enter your password'],
        '2fa': ['verification', 'verify', '2-step'],
        'chat': ['aistudio.google.com', 'gemini', 'chat'],
        'error': ['error', 'failed', 'blocked']
    }
    
    url_lower = url.lower()
    content_lower = page_content.lower()
    
    for context, keywords in contexts.items():
        for keyword in keywords:
            if keyword in url_lower or keyword in content_lower:
                return context
    
    return 'unknown'
```

---

## 📊 MÉTRICAS E MONITORAMENTO

### 📈 Sistema de Logs Estruturados

```python
class HumanBehaviorLogger:
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.actions = []
        self.timings = {}
    
    def log_action(self, action_type, description, duration=None):
        """
        Registra ação com timestamp e duração
        """
        action = {
            'timestamp': datetime.now().isoformat(),
            'type': action_type,
            'description': description,
            'duration': duration,
            'session_id': self.session_id
        }
        self.actions.append(action)
        
    def get_session_stats(self):
        """
        Retorna estatísticas da sessão atual
        """
        total_actions = len(self.actions)
        total_time = sum(a.get('duration', 0) for a in self.actions if a.get('duration'))
        
        return {
            'session_id': self.session_id,
            'total_actions': total_actions,
            'total_time': total_time,
            'actions_per_minute': total_actions / (total_time / 60) if total_time > 0 else 0
        }
```

### 🎯 Métricas de Humanização

```python
def calculate_humanization_score(session_data):
    """
    Calcula score de quão "humano" foi o comportamento
    
    Args:
        session_data: Dados da sessão de automação
        
    Returns:
        float: Score de 0-100 (100 = mais humano)
    """
    score = 100
    
    # Penalizar se ações muito rápidas
    avg_delay = session_data['total_time'] / session_data['total_actions']
    if avg_delay < 0.5:
        score -= 20
    
    # Bonificar variabilidade nos delays
    delay_variance = calculate_variance(session_data['delays'])
    if delay_variance > 0.5:
        score += 10
    
    # Verificar padrões não-humanos
    if has_robotic_patterns(session_data['actions']):
        score -= 30
    
    return max(0, min(100, score))
```

---

## 🚀 OTIMIZAÇÕES AVANÇADAS

### ⚡ Cache de Elementos

```python
class ElementCache:
    def __init__(self):
        self.cache = {}
        self.cache_timeout = 30  # segundos
    
    def get_element(self, selector):
        """
        Cache inteligente de elementos para reduzir buscas DOM
        """
        cache_key = f"{selector}_{int(time.time() // self.cache_timeout)}"
        
        if cache_key not in self.cache:
            self.cache[cache_key] = self.page.locator(selector)
        
        return self.cache[cache_key]
```

### 🧠 Previsão de Ações

```python
def predict_next_action(current_url, page_content):
    """
    Prediz próxima ação baseada em padrões aprendidos
    
    Args:
        current_url: URL atual
        page_content: Conteúdo da página
        
    Returns:
        str: Próxima ação provável
    """
    patterns = {
        'accounts.google.com/accountchooser': 'select_account',
        'accounts.google.com/signin/v2/challenge/pwd': 'enter_password',
        'aistudio.google.com': 'interact_chat'
    }
    
    for pattern, action in patterns.items():
        if pattern in current_url:
            return action
    
    # Análise de conteúdo se URL não é conclusiva
    if 'password' in page_content.lower():
        return 'enter_password'
    elif 'verify' in page_content.lower():
        return 'handle_2fa'
    
    return 'wait_and_observe'
```

---

## 🔒 SEGURANÇA E COMPLIANCE

### 🛡️ Sanitização de Logs

```python
def sanitize_log_data(log_entry):
    """
    Remove informações sensíveis dos logs
    
    Args:
        log_entry: Entrada de log original
        
    Returns:
        dict: Log sanitizado
    """
    sensitive_keywords = ['password', 'senha', 'pass', 'secret']
    
    sanitized = log_entry.copy()
    
    for key, value in sanitized.items():
        if isinstance(value, str):
            for keyword in sensitive_keywords:
                if keyword in key.lower():
                    sanitized[key] = '*' * len(value)
                elif keyword in value.lower():
                    sanitized[key] = re.sub(
                        rf'{keyword}[:\s]*[^\s]+', 
                        f'{keyword}: ****', 
                        value, 
                        flags=re.IGNORECASE
                    )
    
    return sanitized
```

### 🔐 Validação de Integridade

```python
def validate_session_integrity(session_data):
    """
    Valida se a sessão não foi comprometida
    
    Args:
        session_data: Dados da sessão
        
    Returns:
        bool: True se íntegra, False se suspeita
    """
    checks = {
        'timing_realistic': check_timing_patterns(session_data),
        'actions_logical': check_action_sequence(session_data),
        'no_anomalies': check_for_anomalies(session_data)
    }
    
    return all(checks.values())
```

---

Este documento técnico complementa a documentação principal e fornece todos os detalhes de implementação necessários para entender, manter e expandir o sistema de automação AI Studio com comportamento humano.
