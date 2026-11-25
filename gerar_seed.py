"""Gera o seed.sql (dados coerentes com o contexto NextPath). Semente fixa = resultado reproduzível."""
import random
from datetime import date, timedelta

rnd = random.Random(2026)

INSTITUICOES = [
    ("UFPI", "Teresina", "Pública"), ("UESPI", "Teresina", "Pública"),
    ("IFPI", "Teresina", "Pública"), ("UFDPar", "Parnaíba", "Pública"),
    ("UNIFSA", "Teresina", "Privada"), ("Uninassau", "Teresina", "Privada"),
    ("CEUPI", "Teresina", "Privada"), ("Facid", "Teresina", "Privada"),
]
AREAS = ["Tecnologia", "Saúde", "Engenharias", "Direito e Gestão",
         "Educação", "Artes e Design", "Ciências Agrárias", "Comunicação"]

# (nome, área, instituição, semestres, mensalidade, peso de popularidade)
CURSOS = [
    ("Engenharia de Software", "Tecnologia", "UNIFSA", 8, 1290, 10),
    ("Ciência da Computação", "Tecnologia", "UFPI", 8, 0, 9),
    ("Sistemas de Informação", "Tecnologia", "UESPI", 8, 0, 5),
    ("Análise e Desenvolvimento de Sistemas", "Tecnologia", "IFPI", 6, 0, 8),
    ("Ciência de Dados", "Tecnologia", "Uninassau", 8, 980, 4),
    ("Medicina", "Saúde", "UFPI", 12, 0, 9),
    ("Enfermagem", "Saúde", "UESPI", 10, 0, 6),
    ("Odontologia", "Saúde", "UNIFSA", 10, 2450, 4),
    ("Fisioterapia", "Saúde", "Facid", 10, 1150, 3),
    ("Psicologia", "Saúde", "CEUPI", 10, 1320, 8),
    ("Nutrição", "Saúde", "Uninassau", 8, 890, 3),
    ("Engenharia Civil", "Engenharias", "UFPI", 10, 0, 5),
    ("Engenharia Elétrica", "Engenharias", "IFPI", 10, 0, 3),
    ("Engenharia Mecânica", "Engenharias", "UNIFSA", 10, 1180, 2),
    ("Engenharia de Produção", "Engenharias", "CEUPI", 10, 1050, 3),
    ("Arquitetura e Urbanismo", "Engenharias", "Facid", 10, 1480, 4),
    ("Direito", "Direito e Gestão", "UESPI", 10, 0, 7),
    ("Direito", "Direito e Gestão", "UNIFSA", 10, 1650, 8),
    ("Administração", "Direito e Gestão", "UFPI", 8, 0, 5),
    ("Ciências Contábeis", "Direito e Gestão", "Uninassau", 8, 640, 3),
    ("Gestão de Recursos Humanos", "Direito e Gestão", "CEUPI", 4, 520, 2),
    ("Pedagogia", "Educação", "UESPI", 8, 0, 4),
    ("Letras – Português", "Educação", "UFPI", 8, 0, 2),
    ("Matemática (Licenciatura)", "Educação", "IFPI", 8, 0, 2),
    ("Educação Física", "Educação", "UNIFSA", 8, 780, 3),
    ("Design Gráfico", "Artes e Design", "Uninassau", 6, 590, 5),
    ("Design de Interiores", "Artes e Design", "Facid", 6, 570, 2),
    ("Artes Visuais", "Artes e Design", "UFPI", 8, 0, 1),
    ("Agronomia", "Ciências Agrárias", "UFPI", 10, 0, 2),
    ("Medicina Veterinária", "Ciências Agrárias", "UNIFSA", 10, 1890, 3),
    ("Zootecnia", "Ciências Agrárias", "UESPI", 10, 0, 1),
    ("Jornalismo", "Comunicação", "UFPI", 8, 0, 2),
    ("Publicidade e Propaganda", "Comunicação", "CEUPI", 8, 720, 3),
    ("Marketing", "Comunicação", "Uninassau", 6, 610, 4),
    ("Cinema e Audiovisual", "Comunicação", "Facid", 6, 680, 1),
]

NOMES = ["Ana", "Beatriz", "Carlos", "Daniel", "Eduarda", "Felipe", "Gabriela", "Heitor",
         "Isabela", "João", "Karen", "Lucas", "Maria", "Nathan", "Olívia", "Pedro",
         "Rafaela", "Samuel", "Taís", "Vinícius", "Yasmin", "Davi", "Laura", "Matheus",
         "Júlia", "Arthur", "Sofia", "Bruno", "Alice", "Enzo"]
SOBRENOMES = ["Silva", "Santos", "Oliveira", "Souza", "Lima", "Carvalho", "Ferreira", "Rodrigues",
              "Alves", "Pereira", "Gomes", "Ribeiro", "Martins", "Araújo", "Costa", "Barbosa",
              "Moura", "Nunes", "Cavalcante", "Sampaio"]
CIDADES = ["Teresina"] * 8 + ["Parnaíba"] * 2 + ["Picos"] * 2 + ["Floriano", "Campo Maior",
          "Piripiri", "Timon", "Barras"]


def q(s):
    return "'" + str(s).replace("'", "''") + "'"


def escolaridade(idade):
    if idade <= 17:
        return "Ensino Médio (cursando)"
    if idade <= 19:
        return rnd.choice(["Ensino Médio (concluído)", "Ensino Médio (concluído)", "Cursinho pré-vestibular"])
    return rnd.choice(["Ensino Médio (concluído)", "Ensino Superior (cursando)", "Ensino Superior (cursando)"])


out = ["PRAGMA foreign_keys = ON;", "BEGIN TRANSACTION;", ""]

for n, c, t in INSTITUICOES:
    out.append(f"INSERT INTO instituicao (nome, cidade, tipo) VALUES ({q(n)}, {q(c)}, {q(t)});")
out.append("")
for a in AREAS:
    out.append(f"INSERT INTO area_carreira (nome) VALUES ({q(a)});")
out.append("")
inst_id = {n: i + 1 for i, (n, _, _) in enumerate(INSTITUICOES)}
area_id = {a: i + 1 for i, a in enumerate(AREAS)}
for nome, area, inst, sem, mens, _ in CURSOS:
    out.append("INSERT INTO curso (nome, area_id, instituicao_id, duracao_semestres, mensalidade) "
               f"VALUES ({q(nome)}, {area_id[area]}, {inst_id[inst]}, {sem}, {mens});")
out.append("")

inicio, fim = date(2026, 5, 4), date(2026, 11, 23)
span = (fim - inicio).days
usuarios, testes, recos = [], [], []
usados = set()
while len(usuarios) < 120:
    nome = f"{rnd.choice(NOMES)} {rnd.choice(SOBRENOMES)}"
    if nome in usados:
        continue
    usados.add(nome)
    idade = rnd.choices(range(15, 23), weights=[3, 6, 9, 9, 7, 5, 3, 2])[0]
    # cadastros crescem ao longo do tempo (produto em expansão)
    cad = inicio + timedelta(days=int(span * rnd.random() ** 0.7))
    usuarios.append((nome, idade, rnd.choice(CIDADES), escolaridade(idade), cad))

pesos = [c[5] for c in CURSOS]
for uid, (_, _, _, _, cad) in enumerate(usuarios, start=1):
    for _ in range(rnd.choices([0, 1, 2], weights=[1, 6, 3])[0]):
        dias_max = (fim - cad).days
        d = cad + timedelta(days=rnd.randint(0, max(dias_max, 0)))
        testes.append((uid, d, rnd.randint(8, 40), min(100, max(35, int(rnd.gauss(72, 14))))))

for tid in range(1, len(testes) + 1):
    escolhidos = set()
    while len(escolhidos) < 3:
        escolhidos.add(rnd.choices(range(1, len(CURSOS) + 1), weights=pesos)[0])
    base = testes[tid - 1][3]
    for cid in escolhidos:
        comp = min(99, max(50, int(rnd.gauss(base + 6, 9))))
        recos.append((tid, cid, comp))

for n, i, c, e, d in usuarios:
    out.append("INSERT INTO usuario (nome, idade, cidade, escolaridade, data_cadastro) "
               f"VALUES ({q(n)}, {i}, {q(c)}, {q(e)}, {q(d.isoformat())});")
out.append("")
for u, d, dur, p in testes:
    out.append("INSERT INTO teste_vocacional (usuario_id, data_teste, duracao_min, pontuacao) "
               f"VALUES ({u}, {q(d.isoformat())}, {dur}, {p});")
out.append("")
for t, c, comp in recos:
    out.append(f"INSERT INTO recomendacao (teste_id, curso_id, compatibilidade) VALUES ({t}, {c}, {comp});")
out += ["", "COMMIT;"]

open("seed.sql", "w", encoding="utf-8").write("\n".join(out) + "\n")
print(len(usuarios), "usuários,", len(testes), "testes,", len(recos), "recomendações")
