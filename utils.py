import re
import html
import os

def validate_email(email: str) -> bool:
    """
    Valida se o email tem um formato válido
    
    Args:
        email (str): Email para validar
        
    Returns:
        bool: True se o email for válido, False caso contrário
    """
    if not email or not isinstance(email, str):
        return False
    
    email = email.strip()
    
    # Padrão básico de validação de email
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return bool(re.match(email_pattern, email))

def sanitize_input(input_string: str) -> str:
    """
    Sanitiza input do usuário para prevenir ataques
    
    Args:
        input_string (str): String para sanitizar
        
    Returns:
        str: String sanitizada
    """
    if not input_string or not isinstance(input_string, str):
        return ""
    
    # Remove caracteres HTML
    sanitized = html.escape(input_string)
    
    # Remove quebras de linha e espaços extras
    sanitized = sanitized.strip()
    
    # Remove caracteres de controle perigosos
    sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', sanitized)
    
    return sanitized

def format_timeout(seconds: int) -> str:
    """
    Formata tempo em segundos para exibição amigável
    
    Args:
        seconds (int): Tempo em segundos
        
    Returns:
        str: Tempo formatado
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        if remaining_seconds == 0:
            return f"{minutes}min"
        else:
            return f"{minutes}min {remaining_seconds}s"
    else:
        hours = seconds // 3600
        remaining_minutes = (seconds % 3600) // 60
        return f"{hours}h {remaining_minutes}min"

def get_env_with_fallback(key: str, fallback: str = "") -> str:
    """
    Obtém variável de ambiente com fallback
    
    Args:
        key (str): Nome da variável de ambiente
        fallback (str): Valor padrão se a variável não existir
        
    Returns:
        str: Valor da variável ou fallback
    """
    return os.getenv(key, fallback).strip()

def mask_sensitive_data(data: str, mask_char: str = "*", visible_chars: int = 3) -> str:
    """
    Mascara dados sensíveis para logs/exibição
    
    Args:
        data (str): Dados para mascarar
        mask_char (str): Caractere usado para mascarar
        visible_chars (int): Número de caracteres visíveis no início
        
    Returns:
        str: Dados mascarados
    """
    if not data or len(data) <= visible_chars:
        return mask_char * len(data) if data else ""
    
    visible_part = data[:visible_chars]
    masked_part = mask_char * (len(data) - visible_chars)
    
    return visible_part + masked_part

def check_playwright_installation() -> bool:
    """
    Verifica se o Playwright está instalado e configurado
    
    Returns:
        bool: True se estiver instalado, False caso contrário
    """
    try:
        from playwright.sync_api import sync_playwright
        
        # Tentar inicializar playwright
        with sync_playwright() as p:
            # Verificar se o Chromium está disponível
            browser_type = p.chromium
            if not browser_type.executable_path:
                return False
        
        return True
        
    except ImportError:
        return False
    except Exception:
        return False

def get_browser_info() -> dict:
    """
    Obtém informações sobre os navegadores disponíveis
    
    Returns:
        dict: Informações dos navegadores
    """
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browsers = {}
            
            for browser_name in ['chromium', 'firefox', 'webkit']:
                try:
                    browser_type = getattr(p, browser_name)
                    executable = browser_type.executable_path
                    browsers[browser_name] = {
                        'available': bool(executable),
                        'path': executable if executable else None
                    }
                except:
                    browsers[browser_name] = {
                        'available': False,
                        'path': None
                    }
            
            return browsers
            
    except ImportError:
        return {
            'chromium': {'available': False, 'path': None},
            'firefox': {'available': False, 'path': None},
            'webkit': {'available': False, 'path': None}
        }
    except Exception:
        return {}

def log_automation_step(step: str, success: bool = True, details: str = ""):
    """
    Registra passos da automação para debug
    
    Args:
        step (str): Nome do passo
        success (bool): Se o passo foi bem-sucedido
        details (str): Detalhes adicionais
    """
    status = "✅ SUCESSO" if success else "❌ ERRO"
    timestamp = __import__('datetime').datetime.now().strftime("%H:%M:%S")
    
    log_message = f"[{timestamp}] {status} - {step}"
    if details:
        log_message += f" | {details}"
    
    print(log_message)
