# indicadores-bcb

Coleta de indicadores econômicos do Banco Central do Brasil (Selic, IPCA e dólar) e armazenamento em PostgreSQL para análise.

## Objetivo

Montar um pipeline de dados simples e completo: buscar séries históricas na API pública do Banco Central, guardar em um banco relacional e, em seguida, analisar e visualizar os dados. O projeto faz parte do meu portfólio de dados.

Indicadores coletados (últimos 5 anos):

| Código SGS | Indicador               | Unidade  |
|-----------:|-------------------------|----------|
| 432        | Selic meta              | % ao ano |
| 433        | IPCA mensal             | % no mês |
| 1          | Dólar comercial (venda) | R$       |

## Arquitetura

```
API SGS do Banco Central  →  Python (coleta.py)  →  PostgreSQL  →  Power BI (em desenvolvimento)
```

- **API SGS do Banco Central**: fonte pública dos dados, em JSON.
- **Python**: `coleta.py` usa `requests` para buscar as séries e `psycopg` para gravar no banco.
- **PostgreSQL**: banco `indicadores`. A gravação usa `INSERT ... ON CONFLICT DO NOTHING`, então o script pode ser rodado várias vezes sem duplicar registros.
- **Power BI**: dashboard em desenvolvimento.

## Como rodar

Pré-requisitos: Python 3 e PostgreSQL instalados.

1. Crie e ative o ambiente virtual:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Instale as dependências:

   ```powershell
   pip install -r requirements.txt
   ```

3. Crie o banco e as tabelas:

   ```powershell
   createdb -U postgres indicadores
   psql -U postgres -d indicadores -f schema.sql
   ```

4. Defina a senha do PostgreSQL na variável de ambiente `PG_SENHA` (a senha nunca fica no código):

   ```powershell
   $env:PG_SENHA = "sua_senha"
   ```

5. Rode a coleta:

   ```powershell
   python coleta.py
   ```

Depois disso, as consultas de exemplo em `consultas.sql` podem ser executadas no `psql` ou em outro cliente SQL.

## Estrutura das tabelas

**series**: cadastro dos indicadores.

| Coluna  | Tipo    | Descrição                      |
|---------|---------|--------------------------------|
| codigo  | INTEGER | Código da série no SGS (PK)    |
| nome    | TEXT    | Nome do indicador              |
| unidade | TEXT    | Unidade de medida              |

**valores**: observações de cada indicador.

| Coluna | Tipo          | Descrição                              |
|--------|---------------|----------------------------------------|
| codigo | INTEGER       | Código da série (FK para `series`)     |
| data   | DATE          | Data da observação                     |
| valor  | NUMERIC(12,4) | Valor do indicador                     |

Chave primária de `valores`: `(codigo, data)`.

## Arquivos

- `coleta.py`: busca as séries na API e grava no banco.
- `schema.sql`: criação das tabelas e cadastro das séries.
- `consultas.sql`: consultas de exemplo (JOIN, agregação, máximo).
- `requirements.txt`: dependências Python.

## Próximos passos

- Criar views com indicadores derivados (ex.: IPCA acumulado em 12 meses, juro real).
- Construir o dashboard no Power BI.
- Escrever o dicionário de dados.
- Agendar a coleta na AWS.
