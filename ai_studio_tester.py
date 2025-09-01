#!/usr/bin/env python3
"""
🚀 AI Studio - Teste de Acesso Direto
Testa se conseguimos acessar AI Studio sem login
"""

import requests
import json
import time
from pathlib import Path

class AIStudioTester:
    def __init__(self):
        self.session = requests.Session()
        
        # Headers para simular navegador
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
    def test_urls(self):
        """Testa diferentes URLs do AI Studio"""
        print("🧪 TESTANDO ACESSO DIRETO AO AI STUDIO")
        print("=" * 50)
        
        urls_to_test = [
            "https://aistudio.google.com/",
            "https://aistudio.google.com/app",
            "https://aistudio.google.com/prompts",
            "https://aistudio.google.com/prompts/new_chat",
            "https://makersuite.google.com/",
            "https://bard.google.com/",
            "https://gemini.google.com/"
        ]
        
        results = {}
        
        for url in urls_to_test:
            print(f"\n🔍 Testando: {url}")
            try:
                response = self.session.get(url, timeout=10)
                print(f"   📊 Status: {response.status_code}")
                print(f"   🌐 URL final: {response.url}")
                print(f"   📏 Tamanho: {len(response.text)} bytes")
                
                # Verificar se há redirecionamento para login
                if "accounts.google.com" in response.url:
                    print("   🔐 Redirecionou para login")
                    results[url] = "LOGIN_REQUIRED"
                elif response.status_code == 200:
                    print("   ✅ Acessível!")
                    results[url] = "ACCESSIBLE"
                    
                    # Verificar conteúdo
                    if "gemini" in response.text.lower() or "ai studio" in response.text.lower():
                        print("   🎯 Contém conteúdo relevante!")
                        
                    # Salvar para análise
                    filename = f"test_{url.replace('https://', '').replace('/', '_')}.html"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"   💾 Salvo em: {filename}")
                else:
                    print(f"   ❌ Erro: {response.status_code}")
                    results[url] = f"ERROR_{response.status_code}"
                    
            except Exception as e:
                print(f"   ❌ Exceção: {e}")
                results[url] = f"EXCEPTION: {e}"
                
        return results
        
    def find_public_endpoints(self):
        """Procura endpoints públicos"""
        print("\n🔍 PROCURANDO ENDPOINTS PÚBLICOS")
        print("=" * 50)
        
        public_paths = [
            "/api/models",
            "/api/chat",
            "/api/generate",
            "/v1/models",
            "/health",
            "/status",
            "/.well-known/openapi",
            "/docs",
            "/swagger",
            "/api/docs"
        ]
        
        base_urls = [
            "https://aistudio.google.com",
            "https://makersuite.google.com"
        ]
        
        for base in base_urls:
            print(f"\n🌐 Base: {base}")
            for path in public_paths:
                url = f"{base}{path}"
                try:
                    response = self.session.get(url, timeout=5)
                    if response.status_code != 404:
                        print(f"   ✅ {path} -> {response.status_code}")
                        if response.status_code == 200:
                            print(f"      📏 {len(response.text)} bytes")
                except:
                    pass
                    
    def check_authentication_methods(self):
        """Verifica métodos de autenticação"""
        print("\n🔐 VERIFICANDO MÉTODOS DE AUTENTICAÇÃO")
        print("=" * 50)
        
        # Tentar com diferentes tipos de auth
        auth_headers = {
            "API Key": {"X-API-Key": "test", "Authorization": "Bearer test"},
            "OAuth": {"Authorization": "Bearer test_token"},
            "Session": {"Cookie": "session=test"}
        }
        
        test_url = "https://aistudio.google.com/api/models"
        
        for auth_type, headers in auth_headers.items():
            print(f"\n🔑 Testando {auth_type}:")
            try:
                temp_headers = self.session.headers.copy()
                temp_headers.update(headers)
                
                response = requests.get(test_url, headers=temp_headers, timeout=5)
                print(f"   📊 Status: {response.status_code}")
                
                if response.status_code != 404:
                    print(f"   📝 Response: {response.text[:200]}...")
                    
            except Exception as e:
                print(f"   ❌ Erro: {e}")
                
    def test_gemini_api(self):
        """Testa acesso direto à API do Gemini"""
        print("\n💎 TESTANDO API GEMINI DIRETA")
        print("=" * 50)
        
        gemini_urls = [
            "https://generativelanguage.googleapis.com/v1/models",
            "https://ai.google.dev/api",
            "https://developers.generativeai.google/api"
        ]
        
        for url in gemini_urls:
            print(f"\n🔍 Testando: {url}")
            try:
                response = self.session.get(url, timeout=10)
                print(f"   📊 Status: {response.status_code}")
                if response.status_code == 200:
                    print(f"   📝 Conteúdo: {response.text[:300]}...")
            except Exception as e:
                print(f"   ❌ Erro: {e}")
                
    def run_complete_test(self):
        """Executa teste completo"""
        print("🌟 AI STUDIO - TESTE COMPLETO DE ACESSO")
        print("=" * 60)
        
        # 1. Testar URLs principais
        results = self.test_urls()
        
        # 2. Procurar endpoints públicos
        self.find_public_endpoints()
        
        # 3. Verificar métodos de auth
        self.check_authentication_methods()
        
        # 4. Testar API Gemini
        self.test_gemini_api()
        
        # 5. Resumo
        print("\n📊 RESUMO DOS TESTES")
        print("=" * 50)
        for url, status in results.items():
            print(f"🌐 {url}")
            print(f"   {status}")
            
        print("\n✅ Teste completo finalizado!")
        return results

def main():
    """Função principal"""
    tester = AIStudioTester()
    results = tester.run_complete_test()
    
    # Verificar se encontrou algo útil
    accessible_urls = [url for url, status in results.items() if status == "ACCESSIBLE"]
    
    if accessible_urls:
        print(f"\n🎉 {len(accessible_urls)} URL(s) acessível(is) encontrada(s)!")
        for url in accessible_urls:
            print(f"✅ {url}")
        return 0
    else:
        print("\n❌ Nenhuma URL diretamente acessível encontrada")
        print("💡 Login será necessário")
        return 1

if __name__ == "__main__":
    exit(main())
