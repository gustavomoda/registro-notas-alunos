-- Inserir alunos
INSERT INTO
    aluno (nome, matricula)
VALUES ('Tony Stark', '2025001'),
    ('Steve Rogers', '2025002'),
    ('Natasha Romanoff', '2025003'),
    ('Bruce Banner', '2025004'),
    ('Thor Odinson', '2025005'),
    ('Clint Barton', '2025006'),
    ('Wanda Maximoff', '2025007'),
    ('Peter Parker', '2025008'),
    ('Carol Danvers', '2025009'),
    ('Stephen Strange', '2025010');

-- Inserir disciplinas 2025/1
INSERT INTO
    disciplina (nome, ano, semestre)
VALUES ('RAD em Python', 2025, 1),
    ('Álgebra Linear', 2025, 1),
    ('POO em Java', 2025, 1),
    (
        'Estrutura Dados em C',
        2025,
        1
    ),
    ('Banco de Dados', 2025, 1),
    (
        'Engenharia de Software',
        2025,
        1
    );

-- Inserir disciplinas 2025/2
INSERT INTO
    disciplina (nome, ano, semestre)
VALUES ('RAD em Python', 2025, 2),
    ('Álgebra Linear', 2025, 2),
    ('POO em Java', 2025, 2),
    (
        'Estrutura Dados em C',
        2025,
        2
    ),
    ('Banco de Dados', 2025, 2),
    (
        'Engenharia de Software',
        2025,
        2
    );

-- Inserir disciplinas 2024/2 (semestre anterior)
INSERT INTO
    disciplina (nome, ano, semestre)
VALUES (
        'Fundamentos de Programação',
        2024,
        2
    ),
    (
        'Matemática Discreta',
        2024,
        2
    ),
    (
        'Lógica de Programação',
        2024,
        2
    );

-- Matricular alunos nas disciplinas 2025/1
INSERT INTO
    matricula (id_aluno, id_disciplina)
SELECT a.id, d.id
FROM aluno a
    CROSS JOIN disciplina d
WHERE
    d.ano = 2025
    AND d.semestre = 1;

-- Matricular alguns alunos em disciplinas 2024/2 (histórico)
INSERT INTO
    matricula (id_aluno, id_disciplina)
SELECT a.id, d.id
FROM aluno a
    CROSS JOIN disciplina d
WHERE
    d.ano = 2024
    AND d.semestre = 2
    AND a.matricula IN (
        '2025001',
        '2025002',
        '2025003',
        '2025004',
        '2025005'
    );

-- Inserir notas para Tony Stark (perfil: engenheiro brilhante mas inconsistente)
INSERT INTO
    notas (
        id_matricula,
        sm1,
        sm2,
        av,
        avs
    )
SELECT m.id, 0.7, 0.8, 5, 8
FROM
    matricula m
    JOIN aluno a ON m.id_aluno = a.id
    JOIN disciplina d ON m.id_disciplina = d.id
WHERE
    a.nome = 'Tony Stark'
    AND d.nome = 'RAD em Python'
    AND d.ano = 2025
    AND d.semestre = 1;

INSERT INTO
    notas (
        id_matricula,
        sm1,
        sm2,
        av,
        avs
    )
SELECT m.id, 0.9, 1.0, 8, NULL
FROM
    matricula m
    JOIN aluno a ON m.id_aluno = a.id
    JOIN disciplina d ON m.id_disciplina = d.id
WHERE
    a.nome = 'Tony Stark'
    AND d.nome = 'Álgebra Linear'
    AND d.ano = 2025
    AND d.semestre = 1;

INSERT INTO
    notas (
        id_matricula,
        sm1,
        sm2,
        av,
        avs
    )
SELECT
    m.id,
    CASE
        WHEN d.nome = 'POO em Java' THEN 1.0
        WHEN d.nome = 'Estrutura Dados em C' THEN 0.8
        WHEN d.nome = 'Banco de Dados' THEN 0.6
        ELSE 0.9
    END,
    CASE
        WHEN d.nome = 'POO em Java' THEN 0.9
        WHEN d.nome = 'Estrutura Dados em C' THEN 1.0
        WHEN d.nome = 'Banco de Dados' THEN 0.7
        ELSE 0.8
    END,
    CASE
        WHEN d.nome = 'POO em Java' THEN 9
        WHEN d.nome = 'Estrutura Dados em C' THEN 9
        WHEN d.nome = 'Banco de Dados' THEN 7
        ELSE 7
    END,
    NULL
FROM
    matricula m
    JOIN aluno a ON m.id_aluno = a.id
    JOIN disciplina d ON m.id_disciplina = d.id
WHERE
    a.nome = 'Tony Stark'
    AND d.nome IN (
        'POO em Java',
        'Estrutura Dados em C',
        'Banco de Dados',
        'Engenharia de Software'
    )
    AND d.ano = 2025
    AND d.semestre = 1;

-- Inserir notas para Steve Rogers (perfil: líder disciplinado - consistentemente bom)
INSERT INTO
    notas (id_matricula, sm1, sm2, av, avs)
SELECT m.id,
    ROUND((0.8 + (RANDOM() * 0.2))::numeric, 1), -- 0.8 a 1.0 com 1 casa
    ROUND((0.8 + (RANDOM() * 0.2))::numeric, 1), -- 0.8 a 1.0 com 1 casa
    ROUND(7.5 + (RANDOM() * 1.5)), -- 8 a 9 inteiros
    NULL
FROM matricula m
    JOIN aluno a ON m.id_aluno = a.id
    JOIN disciplina d ON m.id_disciplina = d.id
WHERE
    a.nome = 'Steve Rogers'
    AND d.ano = 2025 AND d.semestre = 1;

-- Inserir notas para Natasha Romanoff (perfil: estratégica - boa em tudo)
INSERT INTO
    notas (id_matricula, sm1, sm2, av, avs)
SELECT m.id,
    ROUND((0.7 + (RANDOM() * 0.3))::numeric, 1), -- 0.7 a 1.0 com 1 casa
    ROUND((0.7 + (RANDOM() * 0.3))::numeric, 1), -- 0.7 a 1.0 com 1 casa
    ROUND(6.8 + (RANDOM() * 2.0)), -- 7 a 9 inteiros
    CASE WHEN RANDOM() < 0.3 THEN ROUND(7.0 + (RANDOM() * 2.5)) ELSE NULL END
FROM matricula m
    JOIN aluno a ON m.id_aluno = a.id
    JOIN disciplina d ON m.id_disciplina = d.id
WHERE
    a.nome = 'Natasha Romanoff'
    AND d.ano = 2025 AND d.semestre = 1;

-- Inserir notas para Bruce Banner (perfil: cientista instável - altos e baixos)
INSERT INTO
    notas (id_matricula, sm1, sm2, av, avs)
SELECT m.id,
    CASE WHEN RANDOM() < 0.5 THEN ROUND((0.9 + (RANDOM() * 0.1))::numeric, 1)
         ELSE ROUND((0.4 + (RANDOM() * 0.3))::numeric, 1) END,
    CASE WHEN RANDOM() < 0.5 THEN ROUND((0.8 + (RANDOM() * 0.2))::numeric, 1)
         ELSE ROUND((0.3 + (RANDOM() * 0.4))::numeric, 1) END,
    CASE WHEN RANDOM() < 0.4 THEN ROUND(8.0 + (RANDOM() * 1.5))
         ELSE ROUND(4.5 + (RANDOM() * 2.0)) END,
    CASE WHEN RANDOM() < 0.4 THEN ROUND(7.5 + (RANDOM() * 2.0)) ELSE NULL END
FROM matricula m
    JOIN aluno a ON m.id_aluno = a.id
    JOIN disciplina d ON m.id_disciplina = d.id
WHERE
    a.nome = 'Bruce Banner'
    AND d.ano = 2025 AND d.semestre = 1;

-- Inserir notas para Thor Odinson (perfil: guerreiro nobre - esforçado mas não acadêmico)
INSERT INTO
    notas (id_matricula, sm1, sm2, av, avs)
SELECT m.id,
    ROUND((0.5 + (RANDOM() * 0.4))::numeric, 1), -- 0.5 a 0.9 com 1 casa
    ROUND((0.5 + (RANDOM() * 0.4))::numeric, 1), -- 0.5 a 0.9 com 1 casa
    CASE WHEN d.nome LIKE '%Java%' OR d.nome LIKE '%Python%' THEN ROUND(5.0 + (RANDOM() * 2.5))
         ELSE ROUND(4.5 + (RANDOM() * 3.0)) END,
    CASE WHEN RANDOM() < 0.6 THEN ROUND(6.0 + (RANDOM() * 3.0)) ELSE NULL END
FROM matricula m
    JOIN aluno a ON m.id_aluno = a.id
    JOIN disciplina d ON m.id_disciplina = d.id
WHERE
    a.nome = 'Thor Odinson'
    AND d.ano = 2025 AND d.semestre = 1;

-- Inserir notas para Clint Barton (perfil: precisão sob pressão - irregular mas pode surpreender)
INSERT INTO
    notas (id_matricula, sm1, sm2, av, avs)
SELECT m.id,
    ROUND((0.3 + (RANDOM() * 0.5))::numeric, 1), -- 0.3 a 0.8 com 1 casa
    ROUND((0.4 + (RANDOM() * 0.5))::numeric, 1), -- 0.4 a 0.9 com 1 casa
    ROUND(3.5 + (RANDOM() * 4.0)), -- 4 a 8 inteiros
    CASE WHEN RANDOM() < 0.7 THEN ROUND(5.5 + (RANDOM() * 4.0)) ELSE NULL END
FROM matricula m
    JOIN aluno a ON m.id_aluno = a.id
    JOIN disciplina d ON m.id_disciplina = d.id
WHERE
    a.nome = 'Clint Barton'
    AND d.ano = 2025 AND d.semestre = 1;

-- Inserir notas para Wanda Maximoff (perfil: poder instável - excelente ou regular)
INSERT INTO
    notas (id_matricula, sm1, sm2, av, avs)
SELECT m.id,
    CASE WHEN d.nome IN ('RAD em Python', 'POO em Java') THEN ROUND((0.9 + (RANDOM() * 0.1))::numeric, 1)
         ELSE ROUND((0.5 + (RANDOM() * 0.4))::numeric, 1) END,
    CASE WHEN d.nome IN ('RAD em Python', 'POO em Java') THEN ROUND((0.8 + (RANDOM() * 0.2))::numeric, 1)
         ELSE ROUND((0.6 + (RANDOM() * 0.3))::numeric, 1) END,
    CASE WHEN d.nome IN ('RAD em Python', 'POO em Java', 'Engenharia de Software')
         THEN ROUND(8.5 + (RANDOM() * 1.3))
         ELSE ROUND(5.8 + (RANDOM() * 1.7)) END,
    CASE WHEN RANDOM() < 0.3 THEN ROUND(7.0 + (RANDOM() * 2.5)) ELSE NULL END
FROM matricula m
    JOIN aluno a ON m.id_aluno = a.id
    JOIN disciplina d ON m.id_disciplina = d.id
WHERE
    a.nome = 'Wanda Maximoff'
    AND d.ano = 2025 AND d.semestre = 1;

-- Inserir notas para Peter Parker (perfil: jovem prodígio - bom mas ainda aprendendo)
INSERT INTO
    notas (id_matricula, sm1, sm2, av, avs)
SELECT m.id,
    ROUND((0.7 + (RANDOM() * 0.3))::numeric, 1), -- 0.7 a 1.0 com 1 casa
    ROUND((0.6 + (RANDOM() * 0.4))::numeric, 1), -- 0.6 a 1.0 com 1 casa
    ROUND(7.0 + (RANDOM() * 2.5)), -- 7 a 10 inteiros
    CASE WHEN RANDOM() < 0.2 THEN ROUND(8.0 + (RANDOM() * 1.8)) ELSE NULL END
FROM matricula m
    JOIN aluno a ON m.id_aluno = a.id
    JOIN disciplina d ON m.id_disciplina = d.id
WHERE
    a.nome = 'Peter Parker'
    AND d.ano = 2025 AND d.semestre = 1;

-- Inserir notas para Carol Danvers (perfil: líder exemplar - consistentemente excelente)
INSERT INTO
    notas (id_matricula, sm1, sm2, av, avs)
SELECT m.id,
    ROUND((0.9 + (RANDOM() * 0.1))::numeric, 1), -- 0.9 a 1.0 com 1 casa
    ROUND((0.9 + (RANDOM() * 0.1))::numeric, 1), -- 0.9 a 1.0 com 1 casa
    ROUND(8.8 + (RANDOM() * 1.2)), -- 9 a 10 inteiros
    NULL
FROM matricula m
    JOIN aluno a ON m.id_aluno = a.id
    JOIN disciplina d ON m.id_disciplina = d.id
WHERE
    a.nome = 'Carol Danvers'
    AND d.ano = 2025 AND d.semestre = 1;

-- Inserir notas para Stephen Strange (perfil: perfeccionista - excelente mas crítico consigo mesmo)
INSERT INTO
    notas (id_matricula, sm1, sm2, av, avs)
SELECT m.id,
    ROUND((0.8 + (RANDOM() * 0.2))::numeric, 1), -- 0.8 a 1.0 com 1 casa
    ROUND((0.7 + (RANDOM() * 0.3))::numeric, 1), -- 0.7 a 1.0 com 1 casa
    CASE WHEN d.nome LIKE '%Álgebra%' OR d.nome LIKE '%Estrutura%'
         THEN ROUND(9.0 + (RANDOM() * 1.0))
         ELSE ROUND(7.8 + (RANDOM() * 1.7)) END,
    CASE WHEN RANDOM() < 0.15 THEN ROUND(8.5 + (RANDOM() * 1.5)) ELSE NULL END
FROM matricula m
    JOIN aluno a ON m.id_aluno = a.id
    JOIN disciplina d ON m.id_disciplina = d.id
WHERE
    a.nome = 'Stephen Strange'
    AND d.ano = 2025 AND d.semestre = 1;

-- Inserir algumas notas históricas randomizadas (2024/2)
INSERT INTO
    notas (id_matricula, sm1, sm2, av, avs)
SELECT m.id,
    ROUND((0.6 + (RANDOM() * 0.4))::numeric, 1), -- 0.6 a 1.0 com 1 casa
    ROUND((0.7 + (RANDOM() * 0.3))::numeric, 1), -- 0.7 a 1.0 com 1 casa
    ROUND(6.5 + (RANDOM() * 2.8)), -- 7 a 9 inteiros
    CASE WHEN RANDOM() < 0.25 THEN ROUND(7.0 + (RANDOM() * 2.5)) ELSE NULL END
FROM matricula m
    JOIN aluno a ON m.id_aluno = a.id
    JOIN disciplina d ON m.id_disciplina = d.id
WHERE
    a.nome IN ('Tony Stark', 'Steve Rogers', 'Natasha Romanoff', 'Bruce Banner', 'Thor Odinson')
    AND d.ano = 2024 AND d.semestre = 2;
