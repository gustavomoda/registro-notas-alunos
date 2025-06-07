"""
Testes unitários para AlunoService
"""

import os
import sys
from unittest.mock import Mock

import pytest

from registro_notas_alunos.backend.aluno.service import AlunoService

# Adiciona o diretório raiz ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


class TestAlunoService:
    """Testes para AlunoService"""

    def test_init_com_db_connection(self):
        """Testa inicialização com conexão fornecida"""
        mock_db = Mock()
        service = AlunoService(mock_db)

        assert service.db == mock_db

    def test_init_sem_db_connection(self):
        """Testa inicialização sem conexão (cria nova)"""
        service = AlunoService()

        assert service.db is not None

    def test_criar_sucesso(self):
        """Testa criação de aluno com sucesso"""
        mock_db = Mock()
        mock_db.execute_query.side_effect = [
            [],  # buscar_por_matricula (não existe)
            [(1,)],  # INSERT RETURNING id
        ]

        service = AlunoService(mock_db)
        id_criado = service.criar(nome="João Silva", matricula="2024001")

        assert id_criado == 1
        assert mock_db.execute_query.call_count == 2

    def test_criar_matricula_duplicada(self):
        """Testa criação com matrícula duplicada"""
        mock_db = Mock()
        # buscar_por_matricula retorna aluno existente
        mock_db.execute_query.return_value = [(1, "Outro Aluno", "2024001")]

        service = AlunoService(mock_db)

        with pytest.raises(Exception, match="Aluno já existe"):
            service.criar(nome="João Silva", matricula="2024001")

    def test_criar_sem_resultado(self):
        """Testa criação que falha sem retornar resultado"""
        mock_db = Mock()
        mock_db.execute_query.side_effect = [
            [],  # buscar_por_matricula (não existe)
            [],  # INSERT falha
        ]

        service = AlunoService(mock_db)

        with pytest.raises(Exception, match="Erro ao criar aluno"):
            service.criar(nome="João Silva", matricula="2024001")

    def test_buscar_por_id_encontrado(self):
        """Testa busca por ID que encontra aluno"""
        mock_db = Mock()
        mock_db.execute_query.return_value = [(1, "João Silva", "2024001")]

        service = AlunoService(mock_db)
        aluno = service.buscar_por_id(1)

        assert aluno is not None
        assert aluno.id == 1
        assert aluno.nome == "João Silva"
        assert aluno.matricula == "2024001"

    def test_buscar_por_id_nao_encontrado(self):
        """Testa busca por ID que não encontra aluno"""
        mock_db = Mock()
        mock_db.execute_query.return_value = []

        service = AlunoService(mock_db)
        aluno = service.buscar_por_id(1)

        assert aluno is None

    def test_buscar_por_id_invalido(self):
        """Testa busca com ID inválido"""
        mock_db = Mock()
        service = AlunoService(mock_db)

        with pytest.raises(ValueError, match="ID deve ser maior que zero"):
            service.buscar_por_id(0)

    def test_buscar_por_matricula_encontrado(self):
        """Testa busca por matrícula que encontra aluno"""
        mock_db = Mock()
        mock_db.execute_query.return_value = [(1, "João Silva", "2024001")]

        service = AlunoService(mock_db)
        aluno = service.buscar_por_matricula("2024001")

        assert aluno is not None
        assert aluno.matricula == "2024001"

    def test_buscar_por_matricula_nao_encontrado(self):
        """Testa busca por matrícula que não encontra aluno"""
        mock_db = Mock()
        mock_db.execute_query.return_value = []

        service = AlunoService(mock_db)
        aluno = service.buscar_por_matricula("2024001")

        assert aluno is None

    def test_buscar_por_matricula_vazia(self):
        """Testa busca com matrícula vazia"""
        mock_db = Mock()
        service = AlunoService(mock_db)

        with pytest.raises(ValueError, match="Matrícula é obrigatória"):
            service.buscar_por_matricula("")

    def test_buscar_por_matricula_espacos(self):
        """Testa busca com matrícula apenas espaços"""
        mock_db = Mock()
        service = AlunoService(mock_db)

        with pytest.raises(ValueError, match="Matrícula é obrigatória"):
            service.buscar_por_matricula("   ")

    def test_listar_todos_com_resultados(self):
        """Testa listagem de todos os alunos com resultados"""
        mock_db = Mock()
        mock_db.execute_query.return_value = [
            (1, "João Silva", "2024001"),
            (2, "Maria Santos", "2024002"),
        ]

        service = AlunoService(mock_db)
        alunos = service.listar_todos()

        assert len(alunos) == 2
        assert alunos[0].nome == "João Silva"
        assert alunos[1].nome == "Maria Santos"

    def test_listar_todos_sem_resultados(self):
        """Testa listagem quando não há alunos"""
        mock_db = Mock()
        mock_db.execute_query.return_value = []

        service = AlunoService(mock_db)
        alunos = service.listar_todos()

        assert alunos == []

    def test_atualizar_sucesso(self):
        """Testa atualização de aluno com sucesso"""
        mock_db = Mock()
        mock_db.execute_query.side_effect = [
            [(1, "João Silva", "2024001")],  # buscar_por_id
            [],  # buscar_por_matricula (nova matricula não existe)
            None,  # update
        ]

        service = AlunoService(mock_db)
        service.atualizar(id=1, nome="João Santos", matricula="2024003")

        assert mock_db.execute_query.call_count == 3

    def test_atualizar_mesmo_aluno_mesma_matricula(self):
        """Testa atualização mantendo a mesma matrícula"""
        mock_db = Mock()
        mock_db.execute_query.side_effect = [
            [(1, "João Silva", "2024001")],  # buscar_por_id
            [(1, "João Silva", "2024001")],  # buscar_por_matricula (mesmo)
            None,  # update
        ]

        service = AlunoService(mock_db)
        service.atualizar(id=1, nome="João Santos", matricula="2024001")

        assert mock_db.execute_query.call_count == 3

    def test_atualizar_matricula_duplicada(self):
        """Testa atualização com matrícula já em uso por outro aluno"""
        mock_db = Mock()
        mock_db.execute_query.side_effect = [
            [(1, "João Silva", "2024001")],  # buscar_por_id
            [(2, "Outro Aluno", "2024002")],  # buscar_por_matricula (outro)
        ]

        service = AlunoService(mock_db)

        with pytest.raises(Exception, match="Aluno já existe"):
            service.atualizar(id=1, nome="João Santos", matricula="2024002")

    def test_atualizar_id_invalido(self):
        """Testa atualização com ID inválido"""
        mock_db = Mock()
        service = AlunoService(mock_db)

        with pytest.raises(ValueError, match="ID deve ser maior que zero"):
            service.atualizar(id=0, nome="João", matricula="2024001")

    def test_atualizar_aluno_nao_encontrado(self):
        """Testa atualização de aluno não encontrado"""
        mock_db = Mock()
        mock_db.execute_query.return_value = []  # buscar_por_id retorna vazio

        service = AlunoService(mock_db)

        with pytest.raises(Exception, match="Aluno não encontrado"):
            service.atualizar(id=999, nome="João", matricula="2024001")

    def test_deletar_sucesso(self):
        """Testa exclusão de aluno com sucesso"""
        mock_db = Mock()
        mock_db.execute_query.side_effect = [
            [(1, "João Silva", "2024001")],  # buscar_por_id
            None,  # delete
        ]

        service = AlunoService(mock_db)
        service.deletar(1)

        assert mock_db.execute_query.call_count == 2

    def test_deletar_id_invalido(self):
        """Testa exclusão com ID inválido"""
        mock_db = Mock()
        service = AlunoService(mock_db)

        with pytest.raises(ValueError, match="ID deve ser maior que zero"):
            service.deletar(0)

    def test_deletar_aluno_nao_encontrado(self):
        """Testa exclusão de aluno não encontrado"""
        mock_db = Mock()
        mock_db.execute_query.return_value = []  # buscar_por_id retorna vazio

        service = AlunoService(mock_db)

        with pytest.raises(Exception, match="Aluno não encontrado"):
            service.deletar(999)

    def test_excluir_alias(self):
        """Testa que excluir é alias para deletar"""
        mock_db = Mock()
        mock_db.execute_query.side_effect = [
            [(1, "João Silva", "2024001")],  # buscar_por_id
            None,  # delete
        ]

        service = AlunoService(mock_db)
        service.excluir(1)

        # Deve ter chamado o mesmo fluxo que deletar
        assert mock_db.execute_query.call_count == 2
