"""
Testes unitários para os models
"""

import os
import sys

import pytest

# Adiciona o diretório raiz ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from registro_notas_alunos.backend.aluno.model import Aluno
from registro_notas_alunos.backend.disciplina.model import Disciplina
from registro_notas_alunos.backend.matricula.model import Matricula
from registro_notas_alunos.backend.notas.model import Notas


class TestAlunoModel:
    """Testes para o modelo Aluno"""

    def test_aluno_criacao_valida(self):
        """Testa criação válida de aluno"""
        aluno = Aluno(id=1, nome="João Silva", matricula="2024001")

        assert aluno.id == 1
        assert aluno.nome == "João Silva"
        assert aluno.matricula == "2024001"

    def test_aluno_criacao_sem_id(self):
        """Testa criação de aluno sem ID (para inserção)"""
        aluno = Aluno(id=None, nome="Maria Santos", matricula="2024002")

        assert aluno.id is None
        assert aluno.nome == "Maria Santos"
        assert aluno.matricula == "2024002"

    def test_aluno_normalizacao_dados(self):
        """Testa normalização de dados (remoção de espaços)"""
        aluno = Aluno(id=1, nome="  João Silva  ", matricula="  2024001  ")

        assert aluno.nome == "João Silva"
        assert aluno.matricula == "2024001"

    def test_aluno_nome_vazio(self):
        """Testa validação de nome vazio"""
        with pytest.raises(ValueError, match="Nome do aluno é obrigatório"):
            Aluno(id=1, nome="", matricula="2024001")

    def test_aluno_nome_apenas_espacos(self):
        """Testa validação de nome com apenas espaços"""
        with pytest.raises(ValueError, match="Nome do aluno é obrigatório"):
            Aluno(id=1, nome="   ", matricula="2024001")

    def test_aluno_matricula_vazia(self):
        """Testa validação de matrícula vazia"""
        with pytest.raises(ValueError, match="Matrícula do aluno é obrigatória"):
            Aluno(id=1, nome="João Silva", matricula="")

    def test_aluno_matricula_apenas_espacos(self):
        """Testa validação de matrícula com apenas espaços"""
        with pytest.raises(ValueError, match="Matrícula do aluno é obrigatória"):
            Aluno(id=1, nome="João Silva", matricula="   ")


class TestDisciplinaModel:
    """Testes para o modelo Disciplina"""

    def test_disciplina_criacao_valida(self):
        """Testa criação válida de disciplina"""
        disciplina = Disciplina(id=1, nome="Matemática", ano=2024, semestre=1)

        assert disciplina.id == 1
        assert disciplina.nome == "Matemática"
        assert disciplina.ano == 2024
        assert disciplina.semestre == 1

    def test_disciplina_criacao_sem_id(self):
        """Testa criação de disciplina sem ID"""
        disciplina = Disciplina(id=None, nome="Física", ano=2024, semestre=2)

        assert disciplina.id is None
        assert disciplina.nome == "Física"
        assert disciplina.ano == 2024
        assert disciplina.semestre == 2

    def test_disciplina_normalizacao_nome(self):
        """Testa normalização do nome"""
        disciplina = Disciplina(id=1, nome="  Matemática  ", ano=2024, semestre=1)

        assert disciplina.nome == "Matemática"

    def test_disciplina_nome_vazio(self):
        """Testa validação de nome vazio"""
        with pytest.raises(ValueError, match="Nome da disciplina é obrigatório"):
            Disciplina(id=1, nome="", ano=2024, semestre=1)

    def test_disciplina_ano_invalido(self):
        """Testa validação de ano inválido"""
        with pytest.raises(ValueError, match="Ano deve estar entre 2020 e 2030"):
            Disciplina(id=1, nome="Matemática", ano=1999, semestre=1)

    def test_disciplina_semestre_invalido_baixo(self):
        """Testa validação de semestre inválido (menor que 1)"""
        with pytest.raises(ValueError, match="Semestre deve ser 1 ou 2"):
            Disciplina(id=1, nome="Matemática", ano=2024, semestre=0)

    def test_disciplina_semestre_invalido_alto(self):
        """Testa validação de semestre inválido (maior que 2)"""
        with pytest.raises(ValueError, match="Semestre deve ser 1 ou 2"):
            Disciplina(id=1, nome="Matemática", ano=2024, semestre=3)


class TestMatriculaModel:
    """Testes para o modelo Matricula"""

    def test_matricula_criacao_valida(self):
        """Testa criação válida de matrícula"""
        matricula = Matricula(id=1, id_aluno=1, id_disciplina=1)

        assert matricula.id == 1
        assert matricula.id_aluno == 1
        assert matricula.id_disciplina == 1

    def test_matricula_criacao_sem_id(self):
        """Testa criação de matrícula sem ID"""
        matricula = Matricula(id=None, id_aluno=1, id_disciplina=1)

        assert matricula.id is None
        assert matricula.id_aluno == 1
        assert matricula.id_disciplina == 1

    def test_matricula_id_aluno_invalido(self):
        """Testa validação de ID do aluno inválido"""
        with pytest.raises(ValueError, match="ID do aluno deve ser maior que zero"):
            Matricula(id=1, id_aluno=0, id_disciplina=1)

    def test_matricula_id_disciplina_invalido(self):
        """Testa validação de ID da disciplina inválido"""
        with pytest.raises(ValueError, match="ID da disciplina deve ser maior que zero"):
            Matricula(id=1, id_aluno=1, id_disciplina=0)


class TestNotasModel:
    """Testes para o modelo Notas"""

    def test_notas_criacao_valida(self):
        """Testa criação válida de notas"""
        notas = Notas(id=1, id_matricula=1, sm1=0.5, sm2=0.7, av=9.0, avs=8.0)

        assert notas.id == 1
        assert notas.id_matricula == 1
        assert notas.sm1 == 0.5
        assert notas.sm2 == 0.7
        assert notas.av == 9.0
        assert notas.avs == 8.0

    def test_notas_criacao_sem_id(self):
        """Testa criação de notas sem ID"""
        notas = Notas(id=None, id_matricula=1, sm1=0.5, sm2=0.7, av=9.0, avs=8.0)

        assert notas.id is None
        assert notas.id_matricula == 1

    def test_notas_calculo_nf(self):
        """Testa cálculo da nota final"""
        notas = Notas(id=1, id_matricula=1, sm1=0.8, sm2=0.7, av=9.0, avs=8.0)

        # Calcula a nota final usando o método
        nf = notas.calcular_nota_final()

        # AVS = 8.0, AV = 9.0, usa a maior (9.0)
        # Pontos extras = min(0.8, 1.0) + min(0.7, 1.0) = 0.8 + 0.7 = 1.5
        # NF = 9.0 + 1.5 = 10.5
        assert nf == 10.5
        assert notas.nf == 10.5

    def test_notas_situacao_aprovado(self):
        """Testa situação aprovado (NF >= 6.0)"""
        notas = Notas(id=1, id_matricula=1, sm1=0.8, sm2=0.7, av=5.0, avs=4.0)

        notas.calcular_nota_final()
        assert notas.situacao == "Aprovado"  # 5.0 + 1.5 = 6.5 >= 6.0

    def test_notas_situacao_reprovado(self):
        """Testa situação reprovado (NF < 6.0)"""
        notas = Notas(id=1, id_matricula=1, sm1=0.2, sm2=0.3, av=4.0, avs=3.0)

        notas.calcular_nota_final()
        assert notas.situacao == "Reprovado"  # 4.0 + 0.5 = 4.5 < 6.0

    def test_notas_id_matricula_invalido(self):
        """Testa validação de ID da matrícula inválido"""
        with pytest.raises(ValueError, match="ID da matrícula deve ser maior que zero"):
            Notas(id=1, id_matricula=0, sm1=0.8, sm2=0.7, av=9.0, avs=8.0)

    def test_notas_sm1_negativa(self):
        """Testa validação de SM1 negativa"""
        with pytest.raises(ValueError, match="SM1 deve estar entre 0.0 e 1.0"):
            Notas(id=1, id_matricula=1, sm1=-1.0, sm2=0.7, av=9.0, avs=8.0)

    def test_notas_sm2_maior_que_1(self):
        """Testa validação de SM2 maior que 1.0"""
        with pytest.raises(ValueError, match="SM2 deve estar entre 0.0 e 1.0"):
            Notas(id=1, id_matricula=1, sm1=0.8, sm2=1.1, av=9.0, avs=8.0)

    def test_notas_av_invalida(self):
        """Testa validação de AV inválida"""
        with pytest.raises(ValueError, match="AV deve estar entre 0.0 e 10.0"):
            Notas(id=1, id_matricula=1, sm1=0.8, sm2=0.7, av=15.0, avs=8.0)

    def test_notas_avs_invalida(self):
        """Testa validação de AVS inválida"""
        with pytest.raises(ValueError, match="AVS deve estar entre 0.0 e 10.0"):
            Notas(id=1, id_matricula=1, sm1=0.8, sm2=0.7, av=9.0, avs=-2.0)
