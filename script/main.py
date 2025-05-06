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
    # Configurações do Chrome
    chrome_options = Options()
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-notifications")
    # chrome_options.add_argument("--headless")  # se preferir sem UI

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    try:
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
