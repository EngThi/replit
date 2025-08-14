"""
Teste Rápido do Sistema 2FA
Script simples para testar a funcionalidade básica
"""

import sys
import os

# Adicionar caminho do projeto
sys.path.append('/workspaces/replit')

try:
    from ai_studio_login_2fa import AIStudioLogin2FA
    print("✅ Módulo AI Studio Login importado com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar: {e}")
    sys.exit(1)

def test_initialization():
    """Testa inicialização básica"""
    print("\n🧪 Teste 1: Inicialização")
    try:
        login_system = AIStudioLogin2FA(headless=True)
        print("✅ Sistema de login criado")
        
        login_system.initialize_browser()
        print("✅ Navegador inicializado")
        
        # Testar navegação básica
        login_system.page.goto("https://google.com", timeout=30000)
        title = login_system.page.title()
        print(f"✅ Navegação testada: {title}")
        
        login_system.cleanup()
        print("✅ Limpeza realizada")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def test_ai_studio_access():
    """Testa acesso ao AI Studio"""
    print("\n🧪 Teste 2: Acesso AI Studio")
    try:
        login_system = AIStudioLogin2FA(headless=True)
        login_system.initialize_browser()
        
        # Tentar acessar AI Studio
        login_system.page.goto("https://aistudio.google.com", timeout=30000)
        url = login_system.page.url
        title = login_system.page.title()
        
        print(f"🔗 URL: {url}")
        print(f"📄 Título: {title}")
        
        # Capturar screenshot
        login_system.page.screenshot(path="test_ai_studio_access.png")
        print("📸 Screenshot salvo: test_ai_studio_access.png")
        
        # Verificar se precisa de login
        if "accounts.google.com" in url:
            print("⚠️ Redirecionado para login - normal para primeira vez")
        elif "aistudio.google.com" in url:
            print("✅ Acessou AI Studio diretamente")
        
        login_system.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def test_session_check():
    """Testa verificação de sessão"""
    print("\n🧪 Teste 3: Verificação de Sessão")
    try:
        login_system = AIStudioLogin2FA(headless=True)
        login_system.initialize_browser()
        
        # Verificar se já está logado
        is_logged = login_system.check_if_logged_in()
        print(f"📊 Status de login: {is_logged}")
        
        login_system.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 INICIANDO TESTES DO SISTEMA 2FA")
    print("=" * 45)
    
    tests = [
        ("Inicialização", test_initialization),
        ("Acesso AI Studio", test_ai_studio_access), 
        ("Verificação de Sessão", test_session_check)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Executando: {test_name}")
        result = test_func()
        results.append((test_name, result))
        
        if result:
            print(f"✅ {test_name}: PASSOU")
        else:
            print(f"❌ {test_name}: FALHOU")
    
    print("\n" + "=" * 45)
    print("📊 RESUMO DOS TESTES:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Total: {passed}/{len(tests)} testes passaram")
    
    if passed == len(tests):
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("💡 Sistema está pronto para uso")
    else:
        print("⚠️ Alguns testes falharam")
        print("💡 Verifique os erros acima")

if __name__ == "__main__":
    main()
