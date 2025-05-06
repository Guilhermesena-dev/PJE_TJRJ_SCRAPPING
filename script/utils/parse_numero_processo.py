'''
Módulo utilitário para parse de número de processo no padrão CNJ.
'''
##divide o numero de processo para colar na pagina de consulta do pje 
def parse_numero_processo(numero_completo: str) -> tuple:
    """
    Faz o parse de um número de processo no formato:
      3000396-77.2025.8.06.0010
    Divide em partes:
      - Parte Sequencial: "3000396-77"
      - Ano: "2025"
      - Ramo de Justiça: "8"
      - Tribunal: "06"
      - Órgão: "0010" (opcional)

    Retorna uma tupla (ramo, tribunal, sequencial_completo), onde:
      sequencial_completo será, por exemplo, "3000396-77.2025.0010".

    Exemplo:
      >>> parse_numero_processo("3000396-77.2025.8.06.0010")
      ('8', '06', '3000396-77.2025.0010')
    """
    partes = numero_completo.split('.')
    if len(partes) < 4:
        raise ValueError(f"Formato de processo inesperado (poucas partes): '{numero_completo}'")

    parte_sequencial = partes[0]
    parte_ano        = partes[1]
    parte_ramo       = partes[2]
    parte_tribunal   = partes[3]
    parte_orgao      = partes[4] if len(partes) >= 5 else ""

    if parte_orgao:
        sequencial_completo = f"{parte_sequencial}.{parte_ano}.{parte_orgao}"
    else:
        sequencial_completo = f"{parte_sequencial}.{parte_ano}"

    return parte_ramo, parte_tribunal, sequencial_completo
