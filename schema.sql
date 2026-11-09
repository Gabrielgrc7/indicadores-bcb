-- Estrutura do banco "indicadores"

CREATE TABLE series (
    codigo   INTEGER PRIMARY KEY,
    nome     TEXT NOT NULL,
    unidade  TEXT NOT NULL
);

CREATE TABLE valores (
    codigo  INTEGER REFERENCES series(codigo),
    data    DATE NOT NULL,
    valor   NUMERIC(12,4) NOT NULL,
    PRIMARY KEY (codigo, data)
);

INSERT INTO series (codigo, nome, unidade) VALUES
    (432, 'Selic meta',              '% ao ano'),
    (433, 'IPCA mensal',             '% no mês'),
    (1,   'Dólar comercial (venda)', 'R$');
