import time
import json
from pathlib import Path
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.login import login
from utils.login_button import login_button
from utils.bookmarklet import activate_bookmarklet
from utils.json import salvar_processo_em_json
from utils.parse_numero_processo import parse_numero_processo
from access.detalhes_access import fechar_detalhe_processo
from access.abrir_detalhe import abrir_detalhes_do_processo


def acessar_sites(driver, usuario, senha, output_dir: str = None):
    try:
        # Login no PJe
        login_url = "https://tjrj.pje.jus.br/1g/QuadroAviso/listViewQuadroAvisoMensagem.seam?cid=97699"
        driver.get(login_url)
        login(driver, usuario, senha)
        login_button(driver)
        time.sleep(1)

        main_tab = driver.current_window_handle
        terceira_url = "https://tjrj.pje.jus.br/1g/Processo/ConsultaProcesso/listView.seam"
        driver.switch_to.window(main_tab)
        driver.switch_to.new_window('tab')
        driver.get(terceira_url)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # Entrada manual do número de processo
        numero = input("Digite o número do processo: ").strip()
        if not numero:
            print("Nenhum número digitado. Encerrando.")
            return

        salvar_processo_em_json(numero)

        # Lê todos os processos armazenados
        project_root = Path(__file__).parent.parent.parent
        base_dir = Path(output_dir) if output_dir else project_root / "Dados_json"
        json_path = base_dir / "processos.json"

        with open(json_path, "r", encoding="utf-8") as f:
            dados = json.load(f)

        numeros = [item["Número do Processo"] for item in dados if "Número do Processo" in item]
        print(f'🔢 Total de processos armazenados: {len(numeros)}')

        bm_path = Path(__file__).parent.parent / "bookmarklet" / "consulta_bookmarklet.js"

        for num in numeros:
            try:
                print(f"\n--- Processando CNJ {num}")
                ramo, tribunal, seq = parse_numero_processo(num)
                seq_parts = seq.split('.')
                princ, dig = seq_parts[0].split('-', 1)
                ano = seq_parts[1]
                org = seq_parts[2] if len(seq_parts) > 2 else ''
                campos = {
                    "fPP:numeroProcesso:numeroSequencial": princ,
                    "fPP:numeroProcesso:numeroDigitoVerificador": dig,
                    "fPP:numeroProcesso:Ano": ano,
                    "fPP:numeroProcesso:ramoJustica": ramo,
                    "fPP:numeroProcesso:respectivoTribunal": tribunal,
                    "fPP:numeroProcesso:NumeroOrgaoJustica": org,
                }

                for fld, val in campos.items():
                    el = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, fld)))
                    el.clear()
                    el.send_keys(val)

                orig = abrir_detalhes_do_processo(driver)
                if orig:
                    detalhes = activate_bookmarklet(driver, str(bm_path))
                    print(f"📋 Detalhes extraídos do processo:")
                    for k, v in detalhes.items():
                        print(f"  - {k}: {v}")

                    # Salva os dados do processo individualmente
                    nome_arquivo = f"{num.replace('.', '_').replace('-', '_')}.json"
                    detalhes_path = base_dir / nome_arquivo
                    with open(detalhes_path, "w", encoding="utf-8") as f:
                        json.dump(detalhes, f, ensure_ascii=False, indent=2)
                    print(f"💾 Salvo em {detalhes_path}")

                    time.sleep(1)
                    fechar_detalhe_processo(driver, orig)

            except Exception as e:
                print(f"⚠️ Erro ao processar {num}: {e}")
                continue

    except Exception as e:
        print("❌ Erro inesperado:", e)
        raise
