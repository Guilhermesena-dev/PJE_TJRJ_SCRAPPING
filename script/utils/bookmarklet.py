from pathlib import Path
from selenium.webdriver.remote.webdriver import WebDriver

def activate_bookmarklet(driver: WebDriver,
                         bookmarklet_file_path: str,
                         timeout: int = 600) -> dict:
    """
    Lê e executa um bookmarklet JavaScript async, aguarda retorno e converte os dados
    extraídos em um dicionário {campo: valor}. Espera que o JS retorne `lines`.
    
    Retorna:
    - dict com os dados do processo (campos da primeira linha + valores da segunda)
    """
    try:
        driver.set_script_timeout(timeout)
    except Exception:
        pass

    # Lê o JS do arquivo e ajusta o conteúdo
    raw_js = Path(bookmarklet_file_path).read_text(encoding='utf-8').strip()
    if raw_js.startswith('javascript:'):
        raw_js = raw_js[len('javascript:'):].strip()
    raw_js = raw_js.rstrip(';')

    # Envolve em script assíncrono com callback
    async_wrapper = f"""
var callback = arguments[arguments.length - 1];
(async function() {{
  try {{
    const lines = await ({raw_js});
    callback(lines);
  }} catch (e) {{
    callback({{__error: e.toString()}}); 
  }}
}})();
"""

    # Executa o JS
    result = driver.execute_async_script(async_wrapper)

    if isinstance(result, dict) and result.get('__error'):
        raise RuntimeError(result['__error'])

    # Converte para lista de linhas, se for string
    if isinstance(result, str):
        result = result.strip().split("\n")

    # Processa linhas: primeira = headers, segunda = valores
    if not result or len(result) < 2:
        raise ValueError("Bookmarklet não retornou dados suficientes.")

    headers = result[0].split("\t")
    values = result[1].split("\t")
    parsed = dict(zip(headers, values))

    print(f"📝 Campos extraídos: {list(parsed.keys())}")
    return parsed
