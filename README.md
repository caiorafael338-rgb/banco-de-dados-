# NextPath – Dashboard de Orientação de Carreira

**Aluno:** Caio _(complete: sobrenome e matrícula)_
**Curso:** Engenharia de Software – UNIFSA
**Disciplina:** Banco de Dados · **Apresentação:** 25/11/2026

## Contexto
O **NextPath** é uma plataforma de orientação de carreira e educação para jovens de 15 a 22 anos.
O jovem faz um teste vocacional e recebe recomendações de cursos com um percentual de compatibilidade.
Este trabalho evolui o sistema com um **dashboard** que transforma os dados da plataforma em indicadores
para apoiar decisões: quais cursos e áreas estão em alta, como o uso cresce ao longo do tempo e quem se destaca.

## Tecnologias
- Python 3 + **Flask** (back-end e telas)
- **SQLite** (banco de dados, criado automaticamente a partir dos scripts SQL)
- **Chart.js** (gráficos, arquivo local em `static/`, funciona sem internet)
- HTML + CSS

## Modelo de dados
```
instituicao (1) ──< curso >── (1) area_carreira
usuario (1) ──< teste_vocacional (1) ──< recomendacao >── (1) curso
```
| Tabela | Papel |
|---|---|
| `usuario` | Jovens cadastrados (15–22 anos) |
| `teste_vocacional` | Testes feitos por cada jovem (data, duração, pontuação) |
| `recomendacao` | Cursos sugeridos em cada teste, com compatibilidade 0–100 |
| `curso` | Cursos (duração, mensalidade), ligados a área e instituição |
| `area_carreira` / `instituicao` | Classificações de apoio |

## Dashboard
| Elemento | Tipo | Recursos SQL |
|---|---|---|
| Jovens cadastrados | KPI | COUNT |
| Testes realizados | KPI | COUNT, JOIN |
| Maior compatibilidade registrada | KPI | **MAX**, **SUBQUERY**, **JOIN** |
| Menor mensalidade (rede privada) | KPI | **MIN**, **SUBQUERY**, **JOIN** |
| Pontuação média | KPI | AVG |
| Cursos mais recomendados | Gráfico de barras | **GROUP BY**, **HAVING**, **JOIN** |
| Áreas em alta | Gráfico de rosca | GROUP BY, JOIN |
| Testes por mês | Gráfico de linhas | GROUP BY |
| Jovens acima da média geral | Tabela | **HAVING**, **SUBQUERY**, **JOIN** |

Cada bloco tem o botão **"Ver consulta SQL"**, que mostra a consulta real usada. Nenhum valor é fixo no código:
tudo vem do banco. A tela **Cadastro** permite inserir um jovem e um teste e ver os indicadores mudarem.

## Como executar
```bash
git clone <URL-DO-REPOSITORIO>
cd nextpath-dashboard
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
python app.py
```
Abra http://127.0.0.1:5000. Na primeira execução o arquivo `nextpath.db` é criado a partir de
`schema.sql` e `seed.sql`. Para recriar os dados do zero, apague `nextpath.db` e execute de novo.

## Arquivos
- `schema.sql` – criação das tabelas
- `seed.sql` – inserção dos dados (120 jovens, 148 testes, 444 recomendações, 34 cursos)
- `consultas.sql` – todas as consultas SQL dos indicadores e gráficos
- `queries.py` – as mesmas consultas, usadas pelo app
- `gerar_seed.py` – gerador (semente fixa) do `seed.sql`
- `app.py`, `templates/`, `static/` – aplicação
