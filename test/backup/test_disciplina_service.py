"""
Testes unitários para DisciplinaService
"""

import os
import sys
from unittest.mock import Mock

import pytest

# Adiciona o diretório raiz ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from registro_notas_alunos.backend.disciplina.service import DisciplinaService


class TestDisciplinaService:
    """Testes para DisciplinaService"""

    def test_init_com_db_connection(self):
        """Testa inicialização com conexão fornecida"""
        mock_db = Mock()
        service = DisciplinaService(mock_db)

        assert service.db == mock_db

    def test_init_sem_db_connection(self):
        """Testa inicialização sem conexão"""
        service = DisciplinaService()

        assert service.db is not None

    def test_criar_sucesso(self):
        """Testa criação de disciplina com sucesso"""
        mock_db = Mock()
        mock_db.execute_query.side_effect = [
            [],  # buscar_por_nome_ano_semestre retorna vazio (não existe)
            [(1,)],  # insert retorna ID criado
        ]

        service = DisciplinaService(mock_db)
        id_criado = service.criar(nome="Matemática", ano=2024, semestre=1)

        assert id_criado == 1
        assert mock_db.execute_query.call_count == 2
        # Primeira chamada: buscar_por_nome_ano_semestre
        buscar_call = mock_db.execute_query.call_args_list[0]
        assert (
            "SELECT id, nome, ano, semestre FROM disciplina "
            "WHERE nome = %s AND ano = %s AND semestre = %s"
        ) in buscar_call[0][0]
        assert buscar_call[0][1] == ("Matemática", 2024, 1)
        # Segunda chamada: insert
        insert_call = mock_db.execute_query.call_args_list[1]
        assert "INSERT INTO disciplina" in insert_call[0][0]
        assert insert_call[0][1] == ("Matemática", 2024, 1)

    def test_criar_disciplina_ja_existe(self):
        """Testa criação de disciplina que já existe"""
        mock_db = Mock()
        mock_db.execute_query.return_value = [
            (1, "Matemática", 2024, 1)
        ]  # disciplina já existe

        service = DisciplinaService(mock_db)

        with pytest.raises(Exception, match="Disciplina já existe"):
            service.criar(nome="Matemática", ano=2024, semestre=1)

    def test_criar_sem_resultado(self):
        """Testa criação que falha sem retornar resultado"""
        mock_db = Mock()
        mock_db.execute_query.side_effect = [
            [],  # buscar_por_nome_ano_semestre retorna vazio
            [],  # insert não retorna resultado
        ]

        service = DisciplinaService(mock_db)

        with pytest.raises(Exception, match="Erro ao criar disciplina"):
            service.criar(nome="Matemática", ano=2024, semestre=1)

    def test_buscar_por_nome_ano_semestre_encontrado(self):
        """Testa busca por nome, ano e semestre que encontra disciplina"""
        mock_db = Mock()
        mock_db.execute_query.return_value = [(1, "Matemática", 2024, 1)]

        service = DisciplinaService(mock_db)
        disciplina = service.buscar_por_nome_ano_semestre("Matemática", 2024, 1)

        assert disciplina is not None
        assert disciplina.id == 1
        assert disciplina.nome == "Matemática"
        assert disciplina.ano == 2024
        assert disciplina.semestre == 1
        mock_db.execute_query.assert_called_once_with(
            (
                "SELECT id, nome, ano, semestre FROM disciplina "
                "WHERE nome = %s AND ano = %s AND semestre = %s"
            ),
            ("Matemática", 2024, 1),
        )

    def test_buscar_por_nome_ano_semestre_nao_encontrado(self):
        """Testa busca por nome, ano e semestre que não encontra disciplina"""
        mock_db = Mock()
        mock_db.execute_query.return_value = []

        service = DisciplinaService(mock_db)
        disciplina = service.buscar_por_nome_ano_semestre("Física", 2024, 2)

        assert disciplina is None
        mock_db.execute_query.assert_called_once_with(
            (
                "SELECT id, nome, ano, semestre FROM disciplina "
                "WHERE nome = %s AND ano = %s AND semestre = %s"
            ),
            ("Física", 2024, 2),
        )

    def test_buscar_por_id_encontrado(self):
        """Testa busca por ID que encontra disciplina"""
        mock_db = Mock()
        mock_db.execute_query.return_value = [(1, "Matemática", 2024, 1)]

        service = DisciplinaService(mock_db)
        disciplina = service.buscar_por_id(1)

        assert disciplina is not None
        assert disciplina.id == 1
        assert disciplina.nome == "Matemática"
        assert disciplina.ano == 2024
        assert disciplina.semestre == 1

    def test_buscar_por_id_nao_encontrado(self):
        """Testa busca por ID que não encontra disciplina"""
        mock_db = Mock()
        mock_db.execute_query.return_value = []

        service = DisciplinaService(mock_db)
        disciplina = service.buscar_por_id(1)

        assert disciplina is None

    def test_buscar_por_id_invalido(self):
        """Testa busca com ID inválido"""
        mock_db = Mock()
        service = DisciplinaService(mock_db)

        with pytest.raises(ValueError, match="ID deve ser maior que zero"):
            service.buscar_por_id(0)

    def test_listar_todas_com_resultados(self):
        """Testa listagem de todas as disciplinas com resultados"""
        mock_db = Mock()
        mock_db.execute_query.return_value = [
            (1, "Matemática", 2024, 1),
            (2, "Física", 2024, 2),
        ]

        service = DisciplinaService(mock_db)
        disciplinas = service.listar_todas()

        assert len(disciplinas) == 2
        assert disciplinas[0].nome == "Matemática"
        assert disciplinas[1].nome == "Física"

    def test_listar_todas_sem_resultados(self):
        """Testa listagem quando não há disciplinas"""
        mock_db = Mock()
        mock_db.execute_query.return_value = []

        service = DisciplinaService(mock_db)
        disciplinas = service.listar_todas()

        assert disciplinas == []

    def test_listar_por_periodo_com_resultados(self):
        """Testa listagem por período com resultados"""
        mock_db = Mock()
        mock_db.execute_query.return_value = [(1, "Matemática", 2024, 1)]

        service = DisciplinaService(mock_db)
        disciplinas = service.listar_por_periodo(2024, 1)

        assert len(disciplinas) == 1
        assert disciplinas[0].ano == 2024
        assert disciplinas[0].semestre == 1

    def test_listar_por_periodo_semestre_invalido(self):
        """Testa listagem por período com semestre inválido"""
        mock_db = Mock()
        service = DisciplinaService(mock_db)

        with pytest.raises(ValueError, match="Semestre deve ser 1 ou 2"):
            service.listar_por_periodo(2024, 3)

    def test_atualizar_sucesso(self):
        """Testa atualização de disciplina com sucesso"""
        mock_db = Mock()
        mock_db.execute_query.side_effect = [
            [(1, "Matemática", 2024, 1)],  # buscar_por_id
            None,  # update
        ]

        service = DisciplinaService(mock_db)
        service.atualizar(id=1, nome="Matemática Avançada", ano=2024, semestre=2)

        assert mock_db.execute_query.call_count == 2
        # Verifica se o UPDATE foi chamado
        update_call = mock_db.execute_query.call_args_list[1]
        assert "UPDATE disciplina" in update_call[0][0]

    def test_atualizar_id_invalido(self):
        """Testa atualização com ID inválido"""
        mock_db = Mock()
        service = DisciplinaService(mock_db)

        with pytest.raises(ValueError, match="ID deve ser maior que zero"):
            service.atualizar(id=0, nome="Matemática", ano=2024, semestre=1)

    def test_atualizar_disciplina_nao_encontrada(self):
        """Testa atualização de disciplina não encontrada"""
        mock_db = Mock()
        mock_db.execute_query.return_value = []  # buscar_por_id retorna vazio

        service = DisciplinaService(mock_db)

        with pytest.raises(Exception, match="Disciplina não encontrada"):
            service.atualizar(id=999, nome="Matemática", ano=2024, semestre=1)

    def test_excluir_sucesso(self):
        """Testa exclusão de disciplina com sucesso"""
        mock_db = Mock()
        mock_db.execute_query.side_effect = [
            [(1, "Matemática", 2024, 1)],  # buscar_por_id
            None,  # delete
        ]

        service = DisciplinaService(mock_db)
        service.excluir(1)

        assert mock_db.execute_query.call_count == 2
        # Verifica se o DELETE foi chamado
        delete_call = mock_db.execute_query.call_args_list[1]
        assert "DELETE FROM disciplina" in delete_call[0][0]

    def test_excluir_id_invalido(self):
        """Testa exclusão com ID inválido"""
        mock_db = Mock()
        service = DisciplinaService(mock_db)

        with pytest.raises(ValueError, match="ID deve ser maior que zero"):
            service.excluir(0)

    def test_excluir_disciplina_nao_encontrada(self):
        """Testa exclusão de disciplina não encontrada"""
        mock_db = Mock()
        mock_db.execute_query.return_value = []  # buscar_por_id retorna vazio

        service = DisciplinaService(mock_db)

        with pytest.raises(Exception, match="Disciplina não encontrada"):
            service.excluir(999)

    def test_deletar_alias(self):
        """Testa que deletar é alias para excluir"""
        mock_db = Mock()
        mock_db.execute_query.side_effect = [
            [(1, "Matemática", 2024, 1)],  # buscar_por_id
            None,  # delete
        ]

        service = DisciplinaService(mock_db)
        service.deletar(1)

        # Deve ter chamado o mesmo fluxo que excluir
        assert mock_db.execute_query.call_count == 2
