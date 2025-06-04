-- Tabela de Alunos
CREATE TABLE aluno (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  matricula VARCHAR(20) UNIQUE NOT NULL
);

-- Tabela de Disciplinas
CREATE TABLE disciplina (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  ano INTEGER NOT NULL,
  semestre INTEGER NOT NULL
);

-- Tabela de Matrículas
CREATE TABLE matricula (
  id SERIAL PRIMARY KEY,
  id_aluno INTEGER REFERENCES aluno(id) ON DELETE CASCADE,
  id_disciplina INTEGER REFERENCES disciplina(id) ON DELETE CASCADE,
  UNIQUE (id_aluno, id_disciplina)
);

-- Tabela de Notas
CREATE TABLE notas (
  id SERIAL PRIMARY KEY,
  id_matricula INTEGER REFERENCES matricula(id) ON DELETE CASCADE,
  sm1 REAL DEFAULT 0.0,
  sm2 REAL DEFAULT 0.0,
  av REAL DEFAULT 0.0,
  avs REAL DEFAULT 0.0,
  nf REAL DEFAULT 0.0,
  situacao VARCHAR(20) DEFAULT 'Em Avaliação'
);
