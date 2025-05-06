from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from access.detalhes_access import abrir_detalhe_processo, fechar_detalhe_processo

def abrir_detalhes_do_processo(driver, tempo_espera=30):
    """
    Clica para abrir o processo na tela de consulta e espera os detalhes carregarem.
    Retorna orig, _ do abrir_detalhe_processo().
    """
    try:
        # Espera botão de pesquisa estar clicável
        btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "fPP:searchProcessos"))
        )
        try:
            btn.click()
        except:
            driver.execute_script('arguments[0].click()', btn)

        # Espera as linhas da tabela aparecerem
        WebDriverWait(driver, tempo_espera).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'tr.rich-table-row'))
        )

        # Abre detalhes
        orig, _ = abrir_detalhe_processo(driver)

        # Aguarda o conteúdo da aba detalhes
        WebDriverWait(driver, tempo_espera).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#maisDetalhes'))
        )

        return orig

    except Exception as e:
        print("❌ Erro ao abrir detalhes do processo:", e)
        return None
