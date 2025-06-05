"""
Testes unitários para MatriculaService
"""

import os
import sys
from unittest.mock import Mock

import pytest

# Adiciona o diretório raiz ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from registro_notas_alunos.backend.matricula.model import Matricula
from registro_notas_alunos.backend.matricula.service import MatriculaService


class TestMatriculaService:
    """Testes para MatriculaService"""

    def test_init_com_db_connection(self):
        """Testa inicialização com conexão fornecida"""
        mock_db = Mock()
        service = MatriculaService(mock_db)

        assert service.db == mock_db

    def test_init_sem_db_connection(self):
        """Testa inicialização sem conexão"""
        service = MatriculaService()

        assert service.db is not None

    def test_criar_sucesso(self):
        """Testa criação de matrícula com sucesso"""
        mock_db = Mock()
        mock_db.execute_query.side_effect = [
            [],  # buscar_por_aluno_disciplina (não existe)
            [(1,)],  # INSERT RETURNING id
        ]

        service = MatriculaService(mock_db)
        matricula = Matricula(id=None, id_aluno=1, id_disciplina=1)
        id_criado = service.criar(matricula)

        assert id_criado == 1
        assert mock_db.execute_query.call_count == 2

    def test_criar_matricula_duplicada(self):
        """Testa criação de matrícula que já existe"""
        mock_db = Mock()
        # buscar_por_aluno_disciplina retorna matrícula existente
        mock_db.execute_query.return_value = [(1, 1, 1)]

        service = MatriculaService(mock_db)
        matricula = Matricula(id=None, id_aluno=1, id_disciplina=1)

        with pytest.raises(Exception, match="Matrícula já existe"):
            service.criar(matricula)

    def test_criar_matricula_com_id(self):
        """Testa criação com ID preenchido (deve falhar)"""
        mock_db = Mock()
        service = MatriculaService(mock_db)
        matricula = Matricula(id=1, id_aluno=1, id_disciplina=1)

        with pytest.raises(ValueError, match="Matrícula para criação não deve ter ID"):
            service.criar(matricula)

    def test_buscar_por_id_encontrado(self):
        """Testa busca por ID que encontra matrícula"""
        mock_db = Mock()
        mock_db.execute_query.return_value = [(1, 1, 1)]

        service = MatriculaService(mock_db)
        matricula = service.buscar_por_id(1)

        assert matricula is not None
        assert matricula.id == 1
        assert matricula.id_aluno == 1
        assert matricula.id_disciplina == 1

    def test_buscar_por_id_nao_encontrado(self):
        """Testa busca por ID que não encontra matrícula"""
        mock_db = Mock()
        mock_db.execute_query.return_value = []

        service = MatriculaService(mock_db)
        matricula = service.buscar_por_id(1)

        assert matricula is None

    def test_buscar_por_id_invalido(self):
        """Testa busca com ID inválido"""
        mock_db = Mock()
        service = MatriculaService(mock_db)

        with pytest.raises(ValueError, match="ID deve ser maior que zero"):
            service.buscar_por_id(0)

    def test_buscar_por_aluno_disciplina_encontrado(self):
        """Testa busca por aluno e disciplina que encontra"""
        mock_db = Mock()
        mock_db.execute_query.return_value = [(1, 1, 1)]

        service = MatriculaService(mock_db)
        matricula = service.buscar_por_aluno_disciplina(1, 1)

        assert matricula is not None
        assert matricula.id_aluno == 1
        assert matricula.id_disciplina == 1

    def test_buscar_por_aluno_disciplina_nao_encontrado(self):
        """Testa busca por aluno e disciplina que não encontra"""
        mock_db = Mock()
        mock_db.execute_query.return_value = []

        service = MatriculaService(mock_db)
        matricula = service.buscar_por_aluno_disciplina(1, 1)

        assert matricula is None

    def test_listar_todas_com_resultados(self):
        """Testa listagem de todas as matrículas com resultados"""
        mock_db = Mock()
        mock_db.execute_query.return_value = [
            (1, "João Silva", "2024001", "Matemática"),
            (2, "Maria Santos", "2024002", "Física"),
        ]

        service = MatriculaService(mock_db)
        matriculas = service.listar_todas()

        assert len(matriculas) == 2
        assert matriculas[0][1] == "João Silva"  # Nome do aluno
        assert matriculas[1][1] == "Maria Santos"

    def test_listar_todas_sem_resultados(self):
        """Testa listagem quando não há matrículas"""
        mock_db = Mock()
        mock_db.execute_query.return_value = []

        service = MatriculaService(mock_db)
        matriculas = service.listar_todas()

        assert matriculas == []

    def test_listar_por_aluno_com_resultados(self):
        """Testa listagem por aluno com resultados"""
        mock_db = Mock()
        mock_db.execute_query.return_value = [(1, "Matemática", 2024, 1)]

        service = MatriculaService(mock_db)
        matriculas = service.listar_por_aluno(1)

        assert len(matriculas) == 1
        assert matriculas[0][1] == "Matemática"  # Nome da disciplina

    def test_listar_por_aluno_id_invalido(self):
        """Testa listagem por aluno com ID inválido"""
        mock_db = Mock()
        service = MatriculaService(mock_db)

        with pytest.raises(ValueError, match="ID do aluno deve ser maior que zero"):
            service.listar_por_aluno(0)

    def test_listar_por_disciplina_com_resultados(self):
        """Testa listagem por disciplina com resultados"""
        mock_db = Mock()
        mock_db.execute_query.return_value = [(1, "João Silva", "2024001")]

        service = MatriculaService(mock_db)
        matriculas = service.listar_por_disciplina(1)

        assert len(matriculas) == 1
        assert matriculas[0][1] == "João Silva"  # Nome do aluno

    def test_listar_por_disciplina_id_invalido(self):
        """Testa listagem por disciplina com ID inválido"""
        mock_db = Mock()
        service = MatriculaService(mock_db)

        with pytest.raises(ValueError, match="ID da disciplina deve ser maior que zero"):
            service.listar_por_disciplina(0)

    def test_excluir_sucesso(self):
        """Testa exclusão de matrícula com sucesso"""
        mock_db = Mock()
        mock_db.execute_query.side_effect = [
            [(1, 1, 1)],  # buscar_por_id
            None,  # delete
        ]

        service = MatriculaService(mock_db)
        service.excluir(1)

        assert mock_db.execute_query.call_count == 2

    def test_excluir_id_invalido(self):
        """Testa exclusão com ID inválido"""
        mock_db = Mock()
        service = MatriculaService(mock_db)

        with pytest.raises(ValueError, match="ID deve ser maior que zero"):
            service.excluir(0)

    def test_excluir_matricula_nao_encontrada(self):
        """Testa exclusão de matrícula não encontrada"""
        mock_db = Mock()
        mock_db.execute_query.return_value = []  # buscar_por_id retorna vazio

        service = MatriculaService(mock_db)

        with pytest.raises(Exception, match="Matrícula não encontrada"):
            service.excluir(999)

    def test_excluir_por_aluno_disciplina_sucesso(self):
        """Testa exclusão por aluno e disciplina"""
        mock_db = Mock()
        mock_db.execute_query.side_effect = [
            [(1, 1, 1)],  # buscar_por_aluno_disciplina
            [(1, 1, 1)],  # buscar_por_id (dentro do excluir)
            None,  # delete
        ]

        service = MatriculaService(mock_db)
        service.excluir_por_aluno_disciplina(1, 1)

        assert mock_db.execute_query.call_count == 3
