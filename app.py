import streamlit as st
import os
from dotenv import load_dotenv
from automation import GoogleAIStudioAutomation
from utils import validate_email, sanitize_input, check_playwright_installation, get_browser_info

# Carregar variáveis de ambiente do arquivo .env se existir
load_dotenv()

def main():
    """
    Aplicação Streamlit para automação de login no Google AI Studio
    """
    st.title("🤖 Automação Google AI Studio")
    st.markdown("### Login Automatizado com Playwright")
    
    # Informações sobre o projeto
    with st.expander("ℹ️ Sobre este Projeto", expanded=False):
        st.markdown("""
        Esta aplicação demonstra como automatizar o login no Google AI Studio usando **Playwright** - 
        uma biblioteca poderosa para automação de navegadores web.
        
        **Funcionalidades:**
        - Interface web amigável construída com Streamlit
        - Automação completa do processo de login do Google
        - Suporte para autenticação de dois fatores (2FA)
        - Validação de credenciais e tratamento de erros
        - Modo simulação para demonstração
        
        **Tecnologias utilizadas:**
        - **Streamlit**: Interface web interativa
        - **Playwright**: Automação de navegador
        - **Python**: Lógica de backend e processamento
        
        **Nota importante:** No ambiente Replit, algumas dependências do sistema podem estar faltando,
        o que pode impedir a execução completa da automação. Use o modo "Simular Automação" para 
        ver como funcionaria.
        """)
    
    # Sidebar com informações e configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        headless_mode = st.checkbox("Modo Headless", value=True, help="Execute o navegador em segundo plano", disabled=True)
        st.caption("Modo headless obrigatório no Replit")
        timeout_2fa = st.slider("Timeout 2FA (segundos)", min_value=30, max_value=120, value=40, step=10)
        
        st.markdown("---")
        st.markdown("### 🔒 Segurança")
        st.info("As credenciais podem ser fornecidas via variáveis de ambiente (SEU_EMAIL, SUA_SENHA) ou inseridas abaixo.")
        
        st.markdown("---")
        st.markdown("### ⚠️ Limitações do Ambiente")
        st.warning("No ambiente Replit, algumas dependências do navegador podem estar faltando. Isso pode causar erros durante a automação.")
        st.info("💡 Use o botão 'Simular Automação' para ver uma demonstração completa do processo!")
        
        if st.button("🔧 Verificar Dependências"):
            check_browser_dependencies()
    
    # Formulário principal
    st.markdown("### 📧 Credenciais de Acesso")
    
    # Verificar se existem credenciais nas variáveis de ambiente
    env_email = os.getenv("SEU_EMAIL", "")
    env_password = os.getenv("SUA_SENHA", "")
    
    col1, col2 = st.columns(2)
    
    with col1:
        email = st.text_input(
            "Email",
            value=env_email,
            placeholder="seu.email@gmail.com",
            help="Seu email do Google"
        )
    
    with col2:
        password = st.text_input(
            "Senha",
            value=env_password,
            type="password",
            placeholder="Sua senha",
            help="Sua senha do Google"
        )
    
    # Validação dos campos
    email_valid = validate_email(email) if email else False
    password_valid = len(password.strip()) > 0 if password else False
    
    # Indicadores visuais de validação
    if email:
        if email_valid:
            st.success("✅ Email válido")
        else:
            st.error("❌ Formato de email inválido")
    
    if password:
        if password_valid:
            st.success("✅ Senha fornecida")
        else:
            st.error("❌ Senha não pode estar vazia")
    
    # Botão de execução
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Iniciar Automação", type="primary", use_container_width=True):
            if not email_valid:
                st.error("Por favor, forneça um email válido.")
                return
            
            if not password_valid:
                st.error("Por favor, forneça uma senha válida.")
                return
            
            # Verificar dependências antes de executar
            if not check_playwright_installation():
                st.error("❌ Playwright não está instalado corretamente.")
                
                # Expandir informações sobre a solução
                with st.expander("� Como resolver este problema", expanded=True):
                    st.markdown("""
                    **No ambiente Codespaces/Replit, o Playwright pode não funcionar devido a limitações do sistema.**
                    
                    **Soluções disponíveis:**
                    
                    1. **🎭 Use o Modo Demonstração** (recomendado aqui):
                       - Clique no botão "📋 Simular Automação" abaixo
                       - Veja como o código funcionaria
                    
                    2. **💻 Execute em ambiente local**:
                       ```bash
                       pip install playwright
                       playwright install chromium
                       ```
                    
                    3. **🐳 Use Docker localmente**:
                       ```bash
                       docker run -it mcr.microsoft.com/playwright/python:v1.40.0-jammy
                       ```
                    
                    **Por que isso acontece?**
                    - Ambiente Alpine Linux não tem todas as dependências do Chromium
                    - Limitações de segurança do ambiente containerizado
                    - Arquitetura específica pode não ser suportada
                    """)
                
                st.info("💡 **Dica**: Use o botão 'Simular Automação' para ver uma demonstração completa!")
                return
            
            # Executar automação
            execute_automation(email, password, headless_mode, timeout_2fa)
    
    # Botão alternativo para demonstração
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📋 Simular Automação (Demo)", use_container_width=True):
            if not email_valid:
                st.error("Por favor, forneça um email válido.")
                return
            
            if not password_valid:
                st.error("Por favor, forneça uma senha válida.")
                return
            
            # Executar simulação
            simulate_automation(email, password, timeout_2fa)

def execute_automation(email: str, password: str, headless: bool, timeout_2fa: int):
    """
    Executa a automação de login
    """
    # Sanitizar inputs
    email = sanitize_input(email)
    password = sanitize_input(password)
    
    # Inicializar variável de automação
    automation = None
    
    # Criar container para status
    status_container = st.container()
    
    with status_container:
        # Barra de progresso
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Inicializar automação
            automation = GoogleAIStudioAutomation(headless=headless, timeout_2fa=timeout_2fa)
            
            # Etapa 1: Inicializar navegador
            status_text.text("🔄 Inicializando navegador...")
            progress_bar.progress(10)
            automation.initialize_browser()
            
            # Etapa 2: Navegar para o site
            status_text.text("🌐 Navegando para Google AI Studio...")
            progress_bar.progress(25)
            automation.navigate_to_ai_studio()
            
            # Etapa 3: Iniciar login
            status_text.text("🔑 Iniciando processo de login...")
            progress_bar.progress(40)
            automation.start_login()
            
            # Etapa 4: Inserir email
            status_text.text("📧 Inserindo email...")
            progress_bar.progress(55)
            automation.enter_email(email)
            
            # Etapa 5: Inserir senha
            status_text.text("🔒 Inserindo senha...")
            progress_bar.progress(70)
            automation.enter_password(password)
            
            # Etapa 6: Aguardar 2FA
            status_text.text(f"📱 Verificando autenticação de dois fatores...")
            progress_bar.progress(85)
            automation.wait_for_2fa()
            
            # Verificar se há screenshot de 2FA
            import os
            if os.path.exists("2fa_page.png"):
                st.info("📱 **2FA Detectado!** Screenshot da página salvo em: `2fa_page.png`")
                st.info("🔍 **Verificação necessária**: Confirme no seu celular ou use o modo interativo")
                
                # Mostrar opção para modo interativo
                if st.button("🔧 Usar Modo Interativo", key="interactive_mode"):
                    st.info("💻 **Execute no terminal**: `python interactive_login.py`")
            
            # Finalizar
            progress_bar.progress(100)
            status_text.text("✅ Login concluído com sucesso!")
            
            st.success("🎉 Automação finalizada com sucesso!")
            
            # Mostrar screenshots se existirem
            screenshot_files = ["login_success.png", "current_page.png", "2fa_page.png"]
            for screenshot in screenshot_files:
                if os.path.exists(screenshot):
                    st.success(f"📸 Screenshot salvo: `{screenshot}`")
            
            st.balloons()
            
            automation.close_browser()
            
        except Exception as e:
            progress_bar.progress(100)
            status_text.text("❌ Erro durante a automação")
            
            # Capturar screenshot se possível
            error_details = str(e)
            
            if automation and hasattr(automation, 'page') and automation.page:
                try:
                    screenshot_path = "erro_automacao.png"
                    automation.page.screenshot(path=screenshot_path)
                    st.error(f"❌ Erro: {error_details}")
                    st.info("📸 Screenshot do erro foi capturada: erro_automacao.png")
                except:
                    st.error(f"❌ Erro: {error_details}")
            else:
                st.error(f"❌ Erro: {error_details}")
            
            # Tentar fechar o navegador mesmo em caso de erro
            try:
                if automation and hasattr(automation, 'browser') and automation.browser:
                    automation.close_browser()
            except:
                pass

def simulate_automation(email: str, password: str, timeout_2fa: int):
    """
    Simula o processo de automação sem executar o navegador real
    """
    import time
    
    # Sanitizar inputs
    email = sanitize_input(email)
    password = sanitize_input(password)
    
    # Criar container para status
    status_container = st.container()
    
    with status_container:
        st.info("🎭 **Modo Demonstração** - Simulando processo de automação")
        
        # Barra de progresso
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        steps = [
            ("🔄 Inicializando navegador Playwright...", 10),
            ("🌐 Navegando para https://aistudio.google.com/...", 25),
            ("🔍 Procurando botão 'Sign in'...", 40),
            (f"📧 Inserindo email: {email[:3]}***@{email.split('@')[1] if '@' in email else 'gmail.com'}", 55),
            ("🔒 Inserindo senha...", 70),
            (f"⏳ Aguardando autenticação de dois fatores ({timeout_2fa}s)...", 85),
            ("✅ Login simulado concluído!", 100)
        ]
        
        for step_text, progress in steps:
            status_text.text(step_text)
            progress_bar.progress(progress)
            time.sleep(1.5)  # Simular tempo de processamento
            
        st.success("🎉 Simulação da automação finalizada!")
        st.info("📝 **Código que seria executado:**")
        
        # Exibir o código que seria executado
        code_example = f"""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # 1. Navegar para Google AI Studio
    page.goto("https://aistudio.google.com/")
    page.wait_for_load_state('networkidle')
    
    # 2. Procurar e clicar no botão "Get started" ou "Sign in"
    login_selectors = [
        "text=Get started",      # Botão principal na página inicial
        "text=Sign in",         # Botão alternativo
        "button:has-text('Get started')",
        "a:has-text('Get started')"
    ]
    
    clicked = False
    for selector in login_selectors:
        try:
            page.wait_for_selector(selector, timeout=5000)
            if page.is_visible(selector):
                page.click(selector)
                print(f"✅ Clicou em: {{selector}}")
                clicked = True
                break
        except:
            continue
    
    if not clicked:
        # Busca mais avançada usando JavaScript
        page.evaluate('''
            () => {{
                const buttons = document.querySelectorAll('button, a, [role="button"]');
                for (const btn of buttons) {{
                    if (btn.textContent.toLowerCase().includes('get started')) {{
                        btn.click();
                        return;
                    }}
                }}
            }}
        ''')
    
    # 3. Aguardar redirecionamento para login do Google
    page.wait_for_function(
        "() => window.location.href.includes('accounts.google.com')",
        timeout=15000
    )
    
    # 4. Inserir email
    page.fill("input[type='email']", "{email}")
    page.click("text=Next")
    
    # 5. Inserir senha
    page.wait_for_timeout(3000)
    page.fill("input[type='password']", "***")
    page.click("text=Next")
    
    # 6. Aguardar 2FA
    page.wait_for_timeout({timeout_2fa * 1000})
    
    print("✅ Login automatizado realizado!")
    browser.close()
        """
        
        st.code(code_example, language="python")
        
        st.markdown("---")
        st.markdown("**💡 Para executar realmente:**")
        st.markdown("""
        1. Execute este código em um ambiente local
        2. Instale as dependências: `pip install playwright` e `playwright install`
        3. Configure suas credenciais como variáveis de ambiente
        4. Use com responsabilidade e respeite os termos de uso do Google
        """)

def check_browser_dependencies():
    """
    Verifica e exibe o status das dependências do navegador
    """
    st.markdown("#### 🔍 Status das Dependências")
    
    # Verificar instalação do Playwright
    playwright_ok = check_playwright_installation()
    
    if playwright_ok:
        st.success("✅ Playwright está instalado")
        
        # Obter informações dos navegadores
        browser_info = get_browser_info()
        
        if browser_info:
            st.markdown("**Navegadores disponíveis:**")
            for browser, info in browser_info.items():
                if info['available']:
                    st.success(f"✅ {browser.title()}: Disponível")
                else:
                    st.error(f"❌ {browser.title()}: Não disponível")
        else:
            st.warning("⚠️ Não foi possível obter informações dos navegadores")
            
    else:
        st.error("❌ Playwright não está instalado corretamente")
    
    st.markdown("---")
    st.markdown("**💡 Soluções para erros de dependências:**")
    st.markdown("""
    1. **Ambiente Replit**: Algumas dependências do sistema podem estar faltando
    2. **Modo Headless**: Sempre use modo headless no Replit
    3. **Limitações**: A automação pode não funcionar completamente devido às restrições do ambiente
    4. **Alternativa**: Execute o código em um ambiente local com todas as dependências instaladas
    """)

if __name__ == "__main__":
    # Configurar página
    st.set_page_config(
        page_title="Automação Google AI Studio",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    main()
