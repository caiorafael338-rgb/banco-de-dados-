-- NextPath – Dashboard de Orientação de Carreira
-- Esquema do banco de dados (SQLite)

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS recomendacao;
DROP TABLE IF EXISTS teste_vocacional;
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS curso;
DROP TABLE IF EXISTS area_carreira;
DROP TABLE IF EXISTS instituicao;

CREATE TABLE instituicao (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    nome   TEXT NOT NULL UNIQUE,
    cidade TEXT NOT NULL,
    tipo   TEXT NOT NULL CHECK (tipo IN ('Pública', 'Privada'))
);

CREATE TABLE area_carreira (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE
);

CREATE TABLE curso (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    nome              TEXT NOT NULL,
    area_id           INTEGER NOT NULL REFERENCES area_carreira(id),
    instituicao_id    INTEGER NOT NULL REFERENCES instituicao(id),
    duracao_semestres INTEGER NOT NULL CHECK (duracao_semestres > 0),
    mensalidade       REAL    NOT NULL CHECK (mensalidade >= 0)
);

CREATE TABLE usuario (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    nome           TEXT NOT NULL,
    idade          INTEGER NOT NULL CHECK (idade BETWEEN 15 AND 22),
    cidade         TEXT NOT NULL,
    escolaridade   TEXT NOT NULL,
    data_cadastro  TEXT NOT NULL            -- AAAA-MM-DD
);

CREATE TABLE teste_vocacional (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id  INTEGER NOT NULL REFERENCES usuario(id),
    data_teste  TEXT    NOT NULL,           -- AAAA-MM-DD
    duracao_min INTEGER NOT NULL CHECK (duracao_min > 0),
    pontuacao   INTEGER NOT NULL CHECK (pontuacao BETWEEN 0 AND 100)
);

CREATE TABLE recomendacao (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    teste_id       INTEGER NOT NULL REFERENCES teste_vocacional(id),
    curso_id       INTEGER NOT NULL REFERENCES curso(id),
    compatibilidade INTEGER NOT NULL CHECK (compatibilidade BETWEEN 0 AND 100)
);

CREATE INDEX idx_teste_usuario ON teste_vocacional(usuario_id);
CREATE INDEX idx_reco_teste    ON recomendacao(teste_id);
CREATE INDEX idx_reco_curso    ON recomendacao(curso_id);
