import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from utils.json import salvar_processo_em_json  # ajuste conforme o nome real do arquivo
from access.pje_access import acessar_sites  # supondo que sua função acessar_sites está aqui

load_dotenv()

def main():
    chrome_options = Options()
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--headless=new")  # Headless mais moderno e menos detectável
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--window-size=1200,800")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    try:
        # Disfarçar rastros do Selenium
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
                Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
            """
        })
    
        driver.command_executor.set_timeout(600)
    except Exception:
        pass
    driver.set_script_timeout(600)
    driver.maximize_window()

    usuario = os.getenv("USUARIO_PJE")
    senha   = os.getenv("SENHA_PJE")
    print("Usuário:", usuario)
    print("Senha:", senha)

    try:
        acessar_sites(driver, usuario, senha)
        print("Concluído! Mantenha este terminal aberto até encerrar manualmente.")

        while True:
            numero = input("Digite o número do processo para salvar (ou 'sair'): ").strip()
            if numero.lower() == "sair":
                break
            elif numero:
                salvar_processo_em_json(numero)

    except KeyboardInterrupt:
        print("Encerramento solicitado pelo usuário.")
    except Exception as e:
        print("Erro inesperado:", e)
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
