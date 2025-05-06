from pathlib import Path
from selenium.webdriver.remote.webdriver import WebDriver

##executa o bookmarklet
def activate_bookmarklet(driver: WebDriver,
                         bookmarklet_file_path: str,
                         timeout: int = 600):
    """
    Lê um bookmarklet JavaScript async e o executa aguardando o retorno via execute_async_script.
    O arquivo JS deve terminar retornando a variável 'lines' a partir de seu IIFE assíncrono.
    """
    # Ajusta timeout de script
    try:
        driver.set_script_timeout(timeout)
    except Exception:
        pass

    # Carrega o JS
    raw_js = Path(bookmarklet_file_path).read_text(encoding='utf-8').strip()
    if raw_js.startswith('javascript:'):
        raw_js = raw_js[len('javascript:'):].strip()
    raw_js = raw_js.rstrip(';')

    # Envolve em execute_async_script
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
    result = driver.execute_async_script(async_wrapper)

    if isinstance(result, dict) and result.get('__error'):
        raise RuntimeError(result['__error'])

    return result
