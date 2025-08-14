import streamlit as st
import os
from automation import GoogleAIStudioAutomation
from utils import validate_email, sanitize_input

def main():
    """
    Aplicação Streamlit para automação de login no Google AI Studio
    """
    st.title("🤖 Automação Google AI Studio")
    st.markdown("### Login Automatizado com Playwright")
    
    # Sidebar com informações e configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        headless_mode = st.checkbox("Modo Headless", value=True, help="Execute o navegador em segundo plano")
        timeout_2fa = st.slider("Timeout 2FA (segundos)", min_value=30, max_value=120, value=40, step=10)
        
        st.markdown("---")
        st.markdown("### 🔒 Segurança")
        st.info("As credenciais podem ser fornecidas via variáveis de ambiente (SEU_EMAIL, SUA_SENHA) ou inseridas abaixo.")
    
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
            
            # Executar automação
            execute_automation(email, password, headless_mode, timeout_2fa)

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
            status_text.text(f"⏳ Aguardando autenticação de dois fatores ({timeout_2fa}s)...")
            progress_bar.progress(85)
            automation.wait_for_2fa()
            
            # Finalizar
            progress_bar.progress(100)
            status_text.text("✅ Login concluído com sucesso!")
            
            st.success("🎉 Automação finalizada com sucesso!")
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

if __name__ == "__main__":
    # Configurar página
    st.set_page_config(
        page_title="Automação Google AI Studio",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    main()
