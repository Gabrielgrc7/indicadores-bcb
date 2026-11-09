import os
from datetime import date, datetime, timedelta

import psycopg
import requests

SERIES = [432, 433, 1]  # Selic, IPCA, Dólar
URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"

CONEXAO = (
    "host=localhost port=5432 dbname=indicadores user=postgres "
    f"password={os.getenv('PG_SENHA', 'sua_senha_aqui')}"
)


def buscar_serie(codigo, inicio, fim):
    """Pede ao Banco Central os valores de uma série entre duas datas."""
    params = {
        "formato": "json",
        "dataInicial": inicio.strftime("%d/%m/%Y"),
        "dataFinal": fim.strftime("%d/%m/%Y"),
    }
    resposta = requests.get(URL.format(codigo=codigo), params=params, timeout=30)
    resposta.raise_for_status()
    # A API devolve: [{"data": "01/10/2026", "valor": "15.00"}, ...]
    return [
        (codigo, datetime.strptime(item["data"], "%d/%m/%Y").date(), float(item["valor"]))
        for item in resposta.json()
    ]


def main():
    fim = date.today()
    inicio = fim - timedelta(days=365 * 5)  # últimos 5 anos

    with psycopg.connect(CONEXAO) as conn:
        with conn.cursor() as cur:
            for codigo in SERIES:
                linhas = buscar_serie(codigo, inicio, fim)
                cur.executemany(
                    """
                    INSERT INTO valores (codigo, data, valor)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (codigo, data) DO NOTHING
                    """,
                    linhas,
                )
                print(f"Série {codigo}: {len(linhas)} registros")


if __name__ == "__main__":
    main()