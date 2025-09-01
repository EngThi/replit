#!/usr/bin/env python3
"""
Debug simples - verificar página de escolha de conta
"""

import sys
import time
sys.path.append('/workspaces/replit')

from playwright.sync_api import sync_playwright

def debug_simple():
    print("🔍 DEBUG SIMPLES - PÁGINA DE ESCOLHA")
    print("=" * 40)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-web-security']
        )
        
        context = browser.new_context(
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = context.new_page()
        
        try:
            print("🔗 Acessando AI Studio...")
            page.goto("https://aistudio.google.com/u/3/prompts/new_chat", timeout=20000)
            time.sleep(3)
            
            url = page.url
            print(f"📍 URL atual: {url}")
            
            if "accountchooser" in url:
                print("✅ Na página de escolha de conta!")
                
                # Capturar screenshot
                page.screenshot(path="account_chooser_simple.png")
                print("📸 Screenshot salvo: account_chooser_simple.png")
                
                # Procurar por texto da conta
                has_thiago = page.locator('text=thiago').count() > 0
                has_email = page.locator('text=thiago.edu511@gmail.com').count() > 0
                
                print(f"🔍 Texto 'thiago' encontrado: {has_thiago}")
                print(f"🔍 Email encontrado: {has_email}")
                
                if has_email:
                    print("✅ Email encontrado! Tentando clicar...")
                    try:
                        page.click('text=thiago.edu511@gmail.com', timeout=5000)
                        print("✅ Clique realizado!")
                        
                        time.sleep(5)
                        new_url = page.url
                        print(f"📍 Nova URL: {new_url}")
                        
                        if new_url != url:
                            print("🎉 URL mudou! Login progrediu!")
                        else:
                            print("⚠️ URL não mudou - problema no clique")
                            
                    except Exception as e:
                        print(f"❌ Erro ao clicar: {e}")
                else:
                    print("⚠️ Email não encontrado na página")
                    
            else:
                print("⚠️ Não é uma página de escolha de conta")
                print(f"URL: {url}")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
        finally:
            time.sleep(2)
            browser.close()

if __name__ == "__main__":
    debug_simple()
