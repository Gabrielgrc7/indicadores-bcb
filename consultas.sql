-- Consultas de exemplo sobre o banco "indicadores"

-- a) Valores de 2026 de cada indicador, com nome e unidade da série,
--    ordenados por nome e pela data mais recente primeiro.
SELECT s.nome, s.unidade, v.data, v.valor
FROM valores v
JOIN series s ON s.codigo = v.codigo
WHERE v.data >= DATE '2026-01-01'
  AND v.data <  DATE '2027-01-01'
ORDER BY s.nome, v.data DESC;

-- b) Quantidade de registros por indicador.
SELECT s.nome, COUNT(*) AS registros
FROM valores v
JOIN series s ON s.codigo = v.codigo
GROUP BY s.nome
ORDER BY registros DESC;

-- c) Maior valor do dólar (série 1) e a data em que ocorreu.
SELECT data, valor
FROM valores
WHERE codigo = 1
ORDER BY valor DESC
LIMIT 1;
