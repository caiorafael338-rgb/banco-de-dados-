"""NextPath – Dashboard de indicadores (Flask + SQLite)."""
import os
import sqlite3
from datetime import date

from flask import Flask, g, redirect, render_template, request, url_for, flash

from queries import QUERIES

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "nextpath.db")

app = Flask(__name__)
app.secret_key = "nextpath-dev"


def init_db():
    """Cria o banco a partir de schema.sql + seed.sql na primeira execução."""
    if os.path.exists(DB_PATH):
        return
    con = sqlite3.connect(DB_PATH)
    for arq in ("schema.sql", "seed.sql"):
        with open(os.path.join(BASE, arq), encoding="utf-8") as f:
            con.executescript(f.read())
    con.close()


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def run(key):
    return [dict(r) for r in get_db().execute(QUERIES[key][2]).fetchall()]


@app.route("/")
def dashboard():
    one = lambda k: (run(k) or [{}])[0]
    mensal = run("grafico_mensal")
    nomes_mes = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
    data = {
        "kpi": {
            "usuarios": one("kpi_usuarios"),
            "testes": one("kpi_testes"),
            "max": one("kpi_max_compat"),
            "min": one("kpi_min_mensalidade"),
            "media": one("kpi_media_pontuacao"),
        },
        "cursos": run("grafico_cursos"),
        "areas": run("grafico_areas"),
        "mensal": [{"mes": f"{nomes_mes[int(m['mes'][5:]) - 1]}/{m['mes'][2:4]}", "testes": m["testes"]} for m in mensal],
        "destaques": run("tabela_destaques"),
    }
    sqls = {k: {"titulo": v[0], "recursos": v[1], "sql": v[2]} for k, v in QUERIES.items()}
    return render_template("dashboard.html", d=data, sqls=sqls)


@app.route("/cadastro")
def cadastro():
    db = get_db()
    return render_template(
        "cadastro.html",
        usuarios=db.execute("SELECT id, nome FROM usuario ORDER BY nome").fetchall(),
        cursos=db.execute(
            "SELECT c.id, c.nome, i.nome AS inst FROM curso c JOIN instituicao i ON i.id = c.instituicao_id "
            "ORDER BY c.nome, i.nome"
        ).fetchall(),
    )


@app.post("/usuarios")
def novo_usuario():
    f = request.form
    try:
        idade = int(f["idade"])
        if not 15 <= idade <= 22:
            raise ValueError
        db = get_db()
        db.execute(
            "INSERT INTO usuario (nome, idade, cidade, escolaridade, data_cadastro) VALUES (?, ?, ?, ?, ?)",
            (f["nome"].strip(), idade, f["cidade"].strip(), f["escolaridade"], date.today().isoformat()),
        )
        db.commit()
        flash("Jovem cadastrado. O dashboard já reflete o novo registro.")
    except (ValueError, KeyError):
        flash("Não foi possível cadastrar: informe nome e uma idade entre 15 e 22 anos.")
        return redirect(url_for("cadastro"))
    return redirect(url_for("dashboard"))


@app.post("/testes")
def novo_teste():
    f = request.form
    try:
        pont, comp, dur = int(f["pontuacao"]), int(f["compatibilidade"]), int(f["duracao"])
        if not (0 <= pont <= 100 and 0 <= comp <= 100 and dur > 0):
            raise ValueError
        db = get_db()
        cur = db.execute(
            "INSERT INTO teste_vocacional (usuario_id, data_teste, duracao_min, pontuacao) VALUES (?, ?, ?, ?)",
            (int(f["usuario_id"]), date.today().isoformat(), dur, pont),
        )
        db.execute(
            "INSERT INTO recomendacao (teste_id, curso_id, compatibilidade) VALUES (?, ?, ?)",
            (cur.lastrowid, int(f["curso_id"]), comp),
        )
        db.commit()
        flash("Teste registrado. Veja os indicadores atualizados.")
    except (ValueError, KeyError):
        flash("Não foi possível registrar: confira pontuação e compatibilidade (0 a 100) e a duração.")
        return redirect(url_for("cadastro"))
    return redirect(url_for("dashboard"))


init_db()

if __name__ == "__main__":
    app.run(debug=True)
