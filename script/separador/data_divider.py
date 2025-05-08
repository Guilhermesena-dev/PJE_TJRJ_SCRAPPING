import os
import re
import time
import json
import pandas as pd
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Caminhos de input e output (duas pastas separadas)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(PROJECT_ROOT, "Dados_json", "in")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "Dados_json", "out")

# garante existência das pastas
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def parse_polo(s):
    s = str(s)
    # captura substring de Procuradoria
    m = re.search(r'(Procuradoria.*)$', s, flags=re.IGNORECASE)
    procuradoria = m.group(1).strip() if m else ''

    # remove parte de Procuradoria e separa tokens
    sem_proc = re.sub(r'(?:\s*-\s*Procuradoria.*)$', '', s, flags=re.IGNORECASE)
    tokens = [tok.strip() for tok in sem_proc.split(' - ')]

    # extrai campos
    nome = tokens[0] if tokens else ''
    cpf = next((m.group(1) for tok in tokens
                if (m := re.search(r'CPF[:\s]*([\d\.\-]+)', tok, flags=re.IGNORECASE))), '')
    cnpj = next((m.group(1) for tok in tokens
                 if (m := re.search(r'CNPJ[:\s]*([0-9./-]+)', tok, flags=re.IGNORECASE))), '')
    oab = next((tok for tok in tokens if tok.upper().startswith('OAB')), '')
    advogado = ''
    for i, tok in enumerate(tokens):
        if tok.upper().startswith('OAB') and i > 0:
            prev = tokens[i-1]
            advogado = prev.split(')', 1)[-1].strip() if ')' in prev else prev
            break

    return {
        'NOME': nome,
        'CPF': cpf,
        'CNPJ': cnpj,
        'OAB': oab,
        'ADVOGADO': advogado,
        'PROCURADORIA': procuradoria
    }

def process_file(path):
    """Lê JSON de INPUT_DIR, parse polos e salva JSON em OUTPUT_DIR mantendo formato original."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERRO] lendo {path}: {e}")
        return

    original_is_dict = isinstance(data, dict)
    records = [data] if original_is_dict else data
    output = []

    for rec in records:
        rec_out = rec.copy()
        # extrai polos
        ativo_fields = parse_polo(rec.get('Polo ativo', ''))
        passivo_fields = parse_polo(rec.get('Polo passivo', ''))
        # adiciona novos campos
        for k, v in ativo_fields.items():
            rec_out[f"{k}(ATIVO)"] = v
        for k, v in passivo_fields.items():
            rec_out[f"{k}(PASSIVO)"] = v
        output.append(rec_out)

    # seleciona formato de saída
    output_data = output[0] if original_is_dict else output

    # salva JSON mantendo indentação legível
    basename = os.path.splitext(os.path.basename(path))[0]
    out_path = os.path.join(OUTPUT_DIR, f"{basename}_separado.json")
    try:
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)
        print(f"[OK] {os.path.basename(path)} → {os.path.basename(out_path)}")
    except Exception as e:
        print(f"[ERRO] salvando {out_path}: {e}")

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        filename = os.path.basename(event.src_path).lower()
        if filename.endswith('.json') and not filename.endswith('_separado.json'):
            time.sleep(1)
            process_file(event.src_path)

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(Handler(), INPUT_DIR, recursive=False)
    observer.start()
    print(f"Observando {INPUT_DIR} ...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
