from pathlib import Path
import pandas as pd

def pesquisar_processos_por_numero(driver=None, planilhas_dir: str = None):
    """
    Lê o JSON mais recente em /Planilhas, extrai a coluna "Número do Processo"
    e retorna a lista de números (str).
    """
    project_root = Path(__file__).parent.parent
    default_dir = project_root / "Dados_json"
    planilhas_path = Path(planilhas_dir) if planilhas_dir else default_dir

    arquivos = list(planilhas_path.glob("Processos extraidos *.json"))
    if not arquivos:
        raise FileNotFoundError(f"Nenhum arquivo JSON encontrado em {planilhas_path}")
    
    ultimo = max(arquivos, key=lambda f: f.stat().st_mtime)

    df = pd.read_json(ultimo, dtype=str)
    df.columns = df.columns.str.strip()
    numeros = df["Número do Processo"].dropna().unique().tolist()
    print(f"Encontrados {len(numeros)} processos em {ultimo.name}")

    return numeros
