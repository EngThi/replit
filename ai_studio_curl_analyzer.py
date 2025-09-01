#!/usr/bin/env python3
"""
🚀 AI Studio - Sistema Híbrido Final
Simula navegador real com curl e sessões
"""

import subprocess
import json
import time
import os
from pathlib import Path
from credentials_manager import CredentialsManager

class AIStudioCURL:
    def __init__(self):
        self.credentials = CredentialsManager()
        self.session_file = Path("curl_session.txt")
        self.results_file = Path("curl_results.json")
        
    def setup_session(self):
        """Configura sessão curl com cookies"""
        print("🔧 Configurando sessão CURL...")
        
        # Limpar sessão anterior
        if self.session_file.exists():
            self.session_file.unlink()
            
        # Headers para simular Chrome
        self.headers = [
            "-H", "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "-H", "Accept-Language: en-US,en;q=0.5",
            "-H", "Accept-Encoding: gzip, deflate, br",
            "-H", "DNT: 1",
            "-H", "Connection: keep-alive",
            "-H", "Upgrade-Insecure-Requests: 1",
            "-H", "Sec-Fetch-Dest: document",
            "-H", "Sec-Fetch-Mode: navigate",
            "-H", "Sec-Fetch-Site: none"
        ]
        
        return True
        
    def curl_get(self, url, save_cookies=True, follow_redirects=True):
        """Executa GET com curl"""
        cmd = ["curl", "-s", "-L" if follow_redirects else "", "--compressed"]
        
        # Adicionar headers
        cmd.extend(self.headers)
        
        # Gerenciar cookies
        if save_cookies:
            cmd.extend(["-c", str(self.session_file)])
        if self.session_file.exists():
            cmd.extend(["-b", str(self.session_file)])
            
        # URL
        cmd.append(url)
        
        # Remover strings vazias
        cmd = [x for x in cmd if x]
        
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            # Decodificar bytes para string
            if result.returncode == 0:
                try:
                    content = result.stdout.decode('utf-8', errors='ignore')
                    return content, True
                except:
                    # Fallback para latin-1 se UTF-8 falhar
                    content = result.stdout.decode('latin-1', errors='ignore')
                    return content, True
            else:
                return "", False
        except subprocess.TimeoutExpired:
            return "", False
            
    def curl_post(self, url, data=None, form_data=None):
        """Executa POST com curl"""
        cmd = ["curl", "-s", "-L"]
        
        # Adicionar headers
        cmd.extend(self.headers)
        
        # Cookies
        if self.session_file.exists():
            cmd.extend(["-b", str(self.session_file)])
        cmd.extend(["-c", str(self.session_file)])
        
        # Dados
        if form_data:
            for key, value in form_data.items():
                cmd.extend(["-d", f"{key}={value}"])
        elif data:
            cmd.extend(["-d", data])
            
        # URL
        cmd.append(url)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.stdout, result.returncode == 0
        except subprocess.TimeoutExpired:
            return "", False
            
    def test_direct_access(self):
        """Testa acesso direto aos serviços"""
        print("\n🧪 TESTANDO ACESSO DIRETO")
        print("=" * 50)
        
        results = {}
        
        # URLs para testar
        test_urls = [
            ("AI Studio Welcome", "https://aistudio.google.com/"),
            ("AI Studio Chat", "https://aistudio.google.com/prompts/new_chat"),
            ("Gemini", "https://gemini.google.com/"),
            ("API Gemini", "https://generativelanguage.googleapis.com/v1/models?key=demo"),
        ]
        
        for name, url in test_urls:
            print(f"\n🔍 Testando: {name}")
            print(f"   URL: {url}")
            
            content, success = self.curl_get(url)
            
            if success:
                print(f"   ✅ Acessível ({len(content)} bytes)")
                
                # Verificar se precisa de login
                if "accounts.google.com" in content:
                    print("   🔐 Requer login")
                    results[name] = "LOGIN_REQUIRED"
                elif "authentication" in content.lower() or "sign in" in content.lower():
                    print("   🔐 Requer autenticação")
                    results[name] = "AUTH_REQUIRED" 
                elif len(content) > 1000:
                    print("   ✅ Conteúdo completo")
                    results[name] = "ACCESSIBLE"
                    
                    # Salvar conteúdo para análise
                    filename = f"curl_{name.lower().replace(' ', '_')}.html"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"   💾 Salvo: {filename}")
                else:
                    print("   ⚠️ Conteúdo suspeito")
                    results[name] = "SUSPICIOUS"
            else:
                print("   ❌ Inacessível")
                results[name] = "ERROR"
                
        return results
        
    def test_gemini_chat(self):
        """Testa chat direto com Gemini"""
        print("\n💬 TESTANDO CHAT GEMINI")
        print("=" * 50)
        
        # Acessar Gemini
        content, success = self.curl_get("https://gemini.google.com/")
        
        if not success:
            print("❌ Falha ao acessar Gemini")
            return False
            
        print("✅ Gemini acessado")
        
        # Procurar por API endpoints ou tokens
        if "data-init-data" in content or "_init_data" in content:
            print("🔍 Dados de inicialização encontrados")
            
            # Extrair dados iniciais
            import re
            
            # Procurar por tokens ou IDs de sessão
            patterns = [
                r'"session[^"]*":"([^"]+)"',
                r'"token[^"]*":"([^"]+)"',
                r'"key[^"]*":"([^"]+)"',
                r'data-init-data="([^"]*)"'
            ]
            
            tokens = []
            for pattern in patterns:
                matches = re.findall(pattern, content)
                tokens.extend(matches)
                
            if tokens:
                print(f"🔑 {len(tokens)} token(s) encontrado(s)")
                for i, token in enumerate(tokens[:3]):  # Mostrar apenas os primeiros 3
                    print(f"   Token {i+1}: {token[:20]}...")
                return True
            else:
                print("⚠️ Nenhum token encontrado")
                
        print("💡 Gemini requer JavaScript para funcionar completamente")
        return False
        
    def check_api_access(self):
        """Verifica acesso direto às APIs"""
        print("\n🔌 TESTANDO ACESSO ÀS APIs")
        print("=" * 50)
        
        apis = [
            ("Gemini API v1", "https://generativelanguage.googleapis.com/v1/models"),
            ("AI Studio API", "https://aistudio.google.com/api/models"),
            ("Makersuite API", "https://makersuite.google.com/api/models"),
        ]
        
        for name, url in apis:
            print(f"\n🔍 {name}")
            content, success = self.curl_get(url)
            
            if success:
                print(f"   📊 Resposta: {len(content)} bytes")
                
                if "error" in content.lower():
                    print("   ❌ Erro na API")
                    # Tentar ver o erro
                    try:
                        error_data = json.loads(content)
                        error_msg = error_data.get('error', {}).get('message', 'Erro desconhecido')
                        print(f"   💬 {error_msg}")
                    except:
                        print(f"   💬 {content[:100]}...")
                elif "models" in content.lower():
                    print("   ✅ API funcionando!")
                    try:
                        data = json.loads(content)
                        if 'models' in data:
                            print(f"   🤖 {len(data['models'])} modelo(s) disponível(is)")
                    except:
                        pass
            else:
                print("   ❌ Falha na conexão")
                
    def test_alternative_access(self):
        """Testa métodos alternativos de acesso"""
        print("\n🔄 TESTANDO MÉTODOS ALTERNATIVOS")
        print("=" * 50)
        
        # Testar com diferentes User-Agents
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0"
        ]
        
        for i, ua in enumerate(user_agents):
            print(f"\n🌐 User-Agent {i+1}:")
            
            # Modificar headers temporariamente
            original_headers = self.headers.copy()
            self.headers[1] = f"User-Agent: {ua}"
            
            content, success = self.curl_get("https://aistudio.google.com/")
            
            if success and len(content) > 1000:
                print(f"   ✅ Funcionou ({len(content)} bytes)")
                if "accounts.google.com" in content:
                    print("   🔐 Requer login")
                else:
                    print("   ✅ Acesso direto possível")
            else:
                print("   ❌ Não funcionou")
                
            # Restaurar headers
            self.headers = original_headers
            
    def generate_report(self, results):
        """Gera relatório final"""
        print("\n📊 RELATÓRIO FINAL")
        print("=" * 60)
        
        accessible_count = sum(1 for status in results.values() if status == "ACCESSIBLE")
        login_required_count = sum(1 for status in results.values() if status == "LOGIN_REQUIRED")
        
        print(f"✅ Serviços acessíveis: {accessible_count}")
        print(f"🔐 Requerem login: {login_required_count}")
        print(f"📊 Total testado: {len(results)}")
        
        print("\n🎯 ESTRATÉGIAS RECOMENDADAS:")
        
        if accessible_count > 0:
            print("1. ✅ Usar serviços diretamente acessíveis")
            for service, status in results.items():
                if status == "ACCESSIBLE":
                    print(f"   - {service}")
        
        if login_required_count > 0:
            print("2. 🔐 Implementar login automático para:")
            for service, status in results.items():
                if status == "LOGIN_REQUIRED":
                    print(f"   - {service}")
                    
        print("3. 🎯 Alternativas:")
        print("   - Usar API oficial do Gemini com chave")
        print("   - Implementar proxy/bridge personalizado")
        print("   - Usar endpoints públicos encontrados")
        
        # Salvar relatório
        report_data = {
            "timestamp": time.time(),
            "results": results,
            "accessible_count": accessible_count,
            "login_required_count": login_required_count
        }
        
        with open(self.results_file, 'w') as f:
            json.dump(report_data, f, indent=2)
            
        print(f"\n💾 Relatório salvo: {self.results_file}")
        
    def run_complete_analysis(self):
        """Executa análise completa"""
        print("🌟 AI STUDIO - ANÁLISE COMPLETA VIA CURL")
        print("🎯 Descobrindo métodos de acesso sem GUI")
        print("=" * 60)
        
        # Setup
        self.setup_session()
        
        # Testes
        results = self.test_direct_access()
        self.test_gemini_chat()
        self.check_api_access()
        self.test_alternative_access()
        
        # Relatório
        self.generate_report(results)
        
        return results

def main():
    """Função principal"""
    analyzer = AIStudioCURL()
    results = analyzer.run_complete_analysis()
    
    # Verificar se encontrou algo útil
    accessible = [k for k, v in results.items() if v == "ACCESSIBLE"]
    
    if accessible:
        print(f"\n🎉 SUCESSO! {len(accessible)} serviço(s) acessível(is)")
        return 0
    else:
        print("\n💡 Todos os serviços requerem login/auth")
        print("🔧 Implementar automação de login será necessário")
        return 1

if __name__ == "__main__":
    exit(main())
