import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
##Abre aba de detalhes dentro do processo 
def abrir_detalhe_processo(driver, timeout: int = 30) -> tuple[str, str]:
    """
    Abre em nova aba o detalhe do processo e retorna (original_handle, new_handle).
    """
    original_handle = driver.current_window_handle

    # 1) Localiza o link de detalhe
    process_link = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//a[contains(@class, 'btn-link') and contains(@class, 'btn-condensed')]"
        ))
    )

    # 2) Extrai ID e monta URL
    id_attr = process_link.get_attribute("id")
    partes = id_attr.split(":")
    if len(partes) < 3:
        raise RuntimeError(f"ID inesperado no link de detalhe: '{id_attr}'")
    processo_id = partes[2]
    detail_url = (
        f"https://tjrj.pje.jus.br/1g/Processo/ConsultaProcesso/Detalhe/"
        f"listProcessoCompletoAdvogado.seam?id={processo_id}"
    )

    # 3) Abre em nova aba
    driver.execute_script("window.open(arguments[0], '_blank');", detail_url)
    WebDriverWait(driver, timeout).until(lambda d: len(d.window_handles) > 1)

    # 4) Foca na nova aba
    new_handle = driver.window_handles[-1]
    driver.switch_to.window(new_handle)
    print(f"[DETALHE] Aba aberta: {detail_url}")

    return original_handle, new_handle
##fecha aba para busca de novo processo 

def fechar_detalhe_processo(driver, original_handle: str):
    """
    Fecha a aba atual (detalhe) e retorna o foco para a aba original.
    """
    driver.close()
    print("[DETALHE] Aba de detalhe fechada.")
    driver.switch_to.window(original_handle)
    print(f"[DETALHE] Foco retornado para a aba original: {original_handle}")
