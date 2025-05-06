import json
from pathlib import Path
import sys

def salvar_processo_em_json(numero_processo: str):
    """
    Adiciona um número de processo como dicionário {"Número do Processo": ...}
    a um arquivo JSON dentro da pasta especificada.
    Cria a pasta e o arquivo se não existirem.
    """
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent.parent.parent
        
 

    # Caminho do arquivo
    arquivo_path = base_path / "Dados_json" / "processos.json"

    # Carrega os dados existentes (se houver)
    if arquivo_path.exists():
        with open(arquivo_path, "r", encoding="utf-8") as f:
            try:
                dados = json.load(f)
            except json.JSONDecodeError:
                dados = []
    else:
        dados = []

    # Checa se já existe o processo
    ja_existe = any(d.get("Número do Processo") == numero_processo for d in dados)

    # Adiciona se ainda não estiver
    if not ja_existe:
        dados.append({"Número do Processo": numero_processo})
        with open(arquivo_path, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        print(f"Número {numero_processo} salvo em {arquivo_path}")
    else:
        print(f"Número {numero_processo} já está salvo.")
