import pytest
import sys
import os

# Adicionar o diretório raiz ao path para encontrar os módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_studio_automator import AIStudioAutomator

@pytest.fixture(scope="session")
def automator():
    """
    Fixture do Pytest para inicializar e finalizar o AIStudioAutomator.
    É executado uma vez por sessão de teste.
    """
    print("🚀 [Fixture] Inicializando automator para a sessão de teste...")
    instance = AIStudioAutomator(headless=True)

    # Realizar login uma vez para toda a sessão de teste
    try:
        instance.initialize_browser()
        if not instance.check_if_logged_in():
            print("🔑 [Fixture] Sessão não encontrada, executando login rápido...")
            if not instance.quick_login():
                pytest.fail("Falha no login rápido durante a configuração do teste.", pytrace=False)
        print("✅ [Fixture] Login verificado com sucesso.")
    except Exception as e:
        pytest.fail(f"Erro durante a inicialização do automator no fixture: {e}", pytrace=False)

    yield instance

    # Limpeza após todos os testes da sessão serem concluídos
    print("\n🔄 [Fixture] Finalizando automator e limpando recursos...")
    instance.cleanup()
    print("✅ [Fixture] Recursos limpos.")

class TestAIStudioAutomator:
    """
    Agrupa os testes para o AIStudioAutomator.
    Usa a fixture 'automator' para ter uma instância pré-configurada.
    """

    def test_navigation(self, automator):
        """Testa a navegação básica para a página inicial."""
        print("\n🧪 Teste: Navegação para AI Studio")
        success = automator.navigate_to_studio_home()
        assert success, "A navegação para a página inicial do AI Studio falhou."

    def test_chat_creation(self, automator):
        """Testa a criação de um novo chat."""
        print("\n🧪 Teste: Criação de Novo Chat")
        success = automator.create_new_chat()
        assert success, "A criação de um novo chat falhou."

    def test_message_input_detection(self, automator):
        """Testa a detecção do campo de mensagem."""
        print("\n🧪 Teste: Detecção de Campo de Mensagem")
        # Assegura que um chat foi criado antes de procurar o input
        if not automator.current_chat_url:
            automator.create_new_chat()

        input_field = automator.find_message_input()
        assert input_field is not None, "O campo de entrada de mensagem não foi encontrado."

    def test_complete_interaction(self, automator):
        """Testa uma interação completa, enviando uma mensagem e esperando uma resposta."""
        print("\n🧪 Teste: Interação Completa")
        test_message = "Olá! Responda apenas 'Funcionando!' para confirmar que você recebeu esta mensagem."
        result = automator.complete_interaction(test_message)
        assert result is not None, "O método complete_interaction retornou None."
        assert "response" in result and result["response"], "A interação falhou ou não houve resposta."
        assert len(result["response"]) > 0, "A resposta recebida está vazia."

    def test_conversation_saving(self, automator):
        """Testa a funcionalidade de salvar a conversa."""
        print("\n🧪 Teste: Salvamento de Conversas")
        # Garante que há algo para salvar
        if not automator.conversation_history:
            automator.complete_interaction("Mensagem de teste para salvar.")

        conversation_file = automator.save_conversation("test_conversation.json")
        assert conversation_file is not None, "O salvamento da conversa retornou None."
        assert os.path.exists(conversation_file), f"O arquivo de conversa '{conversation_file}' não foi encontrado."
