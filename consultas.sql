-- NextPath – consultas SQL do dashboard
-- (as mesmas executadas pelo app.py; ver queries.py)

-- KPI 1 – Total de jovens cadastrados
-- Recursos: COUNT
SELECT COUNT(*) AS total
FROM usuario;

-- KPI 2 – Testes vocacionais realizados
-- Recursos: COUNT + JOIN
SELECT COUNT(*) AS total
FROM teste_vocacional t
JOIN usuario u ON u.id = t.usuario_id;

-- KPI 3 – Maior compatibilidade já registrada (MAX + SUBQUERY + JOIN)
-- Recursos: MAX · SUBQUERY · JOIN
SELECT r.compatibilidade, c.nome AS curso, i.nome AS instituicao
FROM recomendacao r
JOIN curso c       ON c.id = r.curso_id
JOIN instituicao i ON i.id = c.instituicao_id
WHERE r.compatibilidade = (SELECT MAX(compatibilidade) FROM recomendacao)
ORDER BY r.id
LIMIT 1;

-- KPI 4 – Menor mensalidade entre cursos de instituições privadas (MIN + SUBQUERY + JOIN)
-- Recursos: MIN · SUBQUERY · JOIN
SELECT c.mensalidade, c.nome AS curso, i.nome AS instituicao
FROM curso c
JOIN instituicao i ON i.id = c.instituicao_id
WHERE i.tipo = 'Privada'
  AND c.mensalidade = (SELECT MIN(c2.mensalidade)
                       FROM curso c2
                       JOIN instituicao i2 ON i2.id = c2.instituicao_id
                       WHERE i2.tipo = 'Privada')
LIMIT 1;

-- KPI 5 – Pontuação média nos testes
-- Recursos: AVG
SELECT ROUND(AVG(pontuacao), 1) AS media
FROM teste_vocacional;

-- Gráfico de barras – Cursos mais recomendados (GROUP BY + HAVING + JOIN)
-- Recursos: GROUP BY · HAVING · JOIN
SELECT c.nome || ' – ' || i.nome AS curso,
       COUNT(*)                     AS recomendacoes
FROM recomendacao r
JOIN curso c       ON c.id = r.curso_id
JOIN instituicao i ON i.id = c.instituicao_id
GROUP BY c.id
HAVING COUNT(*) >= 15
ORDER BY recomendacoes DESC
LIMIT 8;

-- Gráfico de rosca – Áreas de carreira mais recomendadas (GROUP BY + JOIN)
-- Recursos: GROUP BY · JOIN
SELECT a.nome AS area,
       COUNT(*)  AS recomendacoes
FROM recomendacao r
JOIN curso c         ON c.id = r.curso_id
JOIN area_carreira a ON a.id = c.area_id
GROUP BY a.id
ORDER BY recomendacoes DESC;

-- Gráfico de linhas – Testes realizados por mês (GROUP BY)
-- Recursos: GROUP BY
SELECT strftime('%Y-%m', data_teste) AS mes,
       COUNT(*)                       AS testes
FROM teste_vocacional
GROUP BY mes
ORDER BY mes;

-- Tabela – Jovens com pontuação média acima da média geral (HAVING + SUBQUERY + JOIN)
-- Recursos: HAVING · SUBQUERY · JOIN
SELECT u.nome, u.cidade,
       COUNT(t.id)                 AS testes,
       ROUND(AVG(t.pontuacao), 1)  AS media
FROM usuario u
JOIN teste_vocacional t ON t.usuario_id = u.id
GROUP BY u.id
HAVING AVG(t.pontuacao) > (SELECT AVG(pontuacao) FROM teste_vocacional)
ORDER BY media DESC, u.nome
LIMIT 6;
