"""
Serviço para operações com Disciplina
"""

from typing import List, Optional

from ..lib.database import DatabaseConnection
from .model import Disciplina


class DisciplinaService:
    """
    Serviço responsável pelas operações de negócio relacionadas a Disciplina
    """

    def __init__(self, db_connection: Optional[DatabaseConnection] = None):
        """
        Inicializa o serviço

        Args:
            db_connection: Conexão com banco de dados (opcional)
        """
        self.db = db_connection or DatabaseConnection()

    def criar(self, nome: str, ano: int, semestre: int) -> int:
        """
        Cria uma nova disciplina no sistema

        Args:
            nome: Nome da disciplina
            ano: Ano da disciplina
            semestre: Semestre da disciplina

        Returns:
            int: ID da disciplina criada

        Raises:
            ValueError: Se dados inválidos
            Exception: Se disciplina já existe ou erro na criação
        """
        disciplina = Disciplina(id=None, nome=nome, ano=ano, semestre=semestre)

        try:
            query = (
                "INSERT INTO disciplina (nome, ano, semestre) VALUES (%s, %s, %s) " "RETURNING id"
            )
            result = self.db.execute_query(
                query, (disciplina.nome, disciplina.ano, disciplina.semestre)
            )

            if not result:
                raise Exception("Erro ao criar disciplina")

            return result[0][0]
        except Exception as e:
            # Captura erros de constraint do banco
            if "duplicate key" in str(e) or "unique constraint" in str(e):
                raise Exception("Disciplina já existe")
            raise e

    def buscar_por_id(self, id: int) -> Optional[Disciplina]:
        """
        Busca uma disciplina pelo ID

        Args:
            id: ID da disciplina

        Returns:
            Disciplina encontrada ou None se não encontrada
        """
        if id <= 0:
            raise ValueError("ID deve ser maior que zero")

        query = "SELECT id, nome, ano, semestre FROM disciplina WHERE id = %s"
        result = self.db.execute_query(query, (id,))

        if not result:
            return None

        row = result[0]
        return Disciplina(id=row[0], nome=row[1], ano=row[2], semestre=row[3])

    def listar_todas(self) -> List[Disciplina]:
        """
        Lista todas as disciplinas cadastradas

        Returns:
            Lista de disciplinas ordenada por nome
        """
        query = "SELECT id, nome, ano, semestre FROM disciplina ORDER BY nome"
        results = self.db.execute_query(query)

        return [Disciplina(id=row[0], nome=row[1], ano=row[2], semestre=row[3]) for row in results]

    def listar_por_periodo(self, ano: int, semestre: int) -> List[Disciplina]:
        """
        Lista disciplinas de um período específico

        Args:
            ano: Ano letivo
            semestre: Semestre (1 ou 2)

        Returns:
            Lista de disciplinas do período especificado
        """
        if semestre not in [1, 2]:
            raise ValueError("Semestre deve ser 1 ou 2")

        query = "SELECT id, nome, ano, semestre FROM disciplina WHERE ano = %s AND semestre = %s ORDER BY nome"
        results = self.db.execute_query(query, (ano, semestre))

        return [Disciplina(id=row[0], nome=row[1], ano=row[2], semestre=row[3]) for row in results]

    def atualizar(self, id: int, nome: str, ano: int, semestre: int) -> None:
        """
        Atualiza dados de uma disciplina

        Args:
            id: ID da disciplina
            nome: Nome atualizado
            ano: Ano atualizado
            semestre: Semestre atualizado

        Raises:
            ValueError: Se ID inválido
            Exception: Se disciplina não encontrada
        """
        if id <= 0:
            raise ValueError("ID deve ser maior que zero")

        # Verifica se disciplina existe
        if not self.buscar_por_id(id):
            raise Exception("Disciplina não encontrada")

        try:
            disciplina = Disciplina(id=id, nome=nome, ano=ano, semestre=semestre)
            query = "UPDATE disciplina SET nome = %s, ano = %s, semestre = %s " "WHERE id = %s"
            self.db.execute_query(
                query,
                (disciplina.nome, disciplina.ano, disciplina.semestre, disciplina.id),
            )
        except Exception as e:
            # Captura erros de constraint do banco
            if "duplicate key" in str(e) or "unique constraint" in str(e):
                raise Exception("Disciplina já existe")
            raise e

    def excluir(self, id: int) -> None:
        """
        Exclui uma disciplina do sistema

        Args:
            id: ID da disciplina a ser excluída
        """
        if id <= 0:
            raise ValueError("ID deve ser maior que zero")

        # Verifica se disciplina existe
        if not self.buscar_por_id(id):
            raise Exception("Disciplina não encontrada")

        query = "DELETE FROM disciplina WHERE id = %s"
        self.db.execute_query(query, (id,))

    def deletar(self, id: int) -> None:
        """
        Deleta uma disciplina do sistema

        Args:
            id: ID da disciplina a ser deletada
        """
        self.excluir(id)
