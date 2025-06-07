"""
Configurações globais dos testes unitários
"""

import os
import sys
from unittest.mock import MagicMock, Mock

import pytest

# Adiciona o diretório raiz ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from registro_notas_alunos.backend.aluno.model import Aluno
from registro_notas_alunos.backend.disciplina.model import Disciplina
from registro_notas_alunos.backend.lib.database import DatabaseConnection
from registro_notas_alunos.backend.matricula.model import Matricula
from registro_notas_alunos.backend.notas.model import Notas


@pytest.fixture
def mock_db():
    """Mock da conexão com banco de dados"""
    db_mock = Mock(spec=DatabaseConnection)
    db_mock.execute_query = MagicMock()
    db_mock.get_connection = MagicMock()
    return db_mock


@pytest.fixture
def sample_aluno():
    """Aluno de exemplo para testes"""
    return Aluno(id=1, nome="João Silva", matricula="2024001")


@pytest.fixture
def sample_aluno_novo():
    """Aluno novo sem ID para testes de criação"""
    return Aluno(id=None, nome="Maria Santos", matricula="2024002")


@pytest.fixture
def sample_disciplina():
    """Disciplina de exemplo para testes"""
    return Disciplina(id=1, nome="Matemática", ano=2024, semestre=1)


@pytest.fixture
def sample_disciplina_nova():
    """Disciplina nova sem ID para testes de criação"""
    return Disciplina(id=None, nome="Física", ano=2024, semestre=2)


@pytest.fixture
def sample_matricula():
    """Matrícula de exemplo para testes"""
    return Matricula(id=1, id_aluno=1, id_disciplina=1)


@pytest.fixture
def sample_matricula_nova():
    """Matrícula nova sem ID para testes de criação"""
    return Matricula(id=None, id_aluno=1, id_disciplina=1)


@pytest.fixture
def sample_notas():
    """Notas de exemplo para testes"""
    return Notas(id=1, id_matricula=1, sm1=8.5, sm2=7.0, av=9.0, avs=8.0)


@pytest.fixture
def sample_notas_nova():
    """Notas novas sem ID para testes de criação"""
    return Notas(id=None, id_matricula=1, sm1=8.5, sm2=7.0, av=9.0, avs=8.0)


@pytest.fixture
def mock_db_results():
    """Resultados mock comuns do banco"""
    return {
        "aluno_row": (1, "João Silva", "2024001"),
        "disciplina_row": (1, "Matemática", 2024, 1),
        "matricula_row": (1, 1, 1),
        "notas_row": (1, 1, 8.5, 7.0, 9.0, 8.0),
        "insert_result": [(1,)],  # ID retornado pelo INSERT
        "empty_result": [],
    }
