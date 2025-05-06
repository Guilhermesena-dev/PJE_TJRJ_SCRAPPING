import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from utils.bookmarklet import activate_bookmarklet
from utils.json import salvar_processo_em_json


def export_detalhe_to_json(driver, output_dir: str = None) -> Path:
    """
    Executa o bookmarklet de consulta na aba de detalhes do processo,
    converte os dados retornados em uma lista de dicionários e salva em um arquivo JSON na pasta 'Planilhas'.

    O nome do arquivo será "detalhe_extraido YYYY-MM-DD HH-MM-SS.json".

    Parâmetros:
    - driver: instância Selenium WebDriver já na aba de detalhes.
    - output_dir: diretório onde o JSON será salvo (padrão: pasta 'Planilhas').

    Retorna:
    - Path para o arquivo JSON gerado.
    """
    project_root = Path(__file__).parent.parent.parent
    default_dir = project_root / "Dados_json_completos"
    base_dir = Path(output_dir) if output_dir else default_dir
    base_dir.mkdir(parents=True, exist_ok=True)

    bookmarklet_path = project_root / "bookmarklets" / "consulta_bookmarklet.js"
    if not bookmarklet_path.is_file():
        raise FileNotFoundError(f"Bookmarklet de consulta não encontrado em: {bookmarklet_path}")

    linhas = activate_bookmarklet(driver, str(bookmarklet_path))
    if linhas is None:
        raise ValueError("Bookmarklet de consulta não retornou dados. Verifique `return linhas;` no JS.")
    if isinstance(linhas, str):
        linhas = linhas.split("\n")

    table = [linha.split("\t") for linha in linhas]
    if not table or not table[0]:
        raise ValueError("Nenhum dado válido retornado pelo bookmarklet de consulta.")
    
    headers, rows = table[0], table[1:]
    df = pd.DataFrame(rows, columns=headers)

    # Renomeia colunas caso existam polos
    df.rename(columns={
        'Polo Ativo': 'Polo_Ativo',
        'Polo Passivo': 'Polo_Passivo'
    }, inplace=True)

    # Salva como JSON
    registros = df.to_dict(orient="records")
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    filename = f"detalhe_extraido {timestamp}.json"
    output_path = base_dir / filename

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(registros, f, ensure_ascii=False, indent=2)

    print(f"📄 Dados de detalhes exportados para: {output_path}")
    return output_path
