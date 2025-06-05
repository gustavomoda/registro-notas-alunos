"""
Serviço para operações com Aluno
"""

from typing import List, Optional

from ..lib.database import DatabaseConnection
from .model import Aluno


class AlunoService:
    """
    Serviço responsável pelas operações de negócio relacionadas a Aluno

    Implementa o padrão Service Layer, centralizando a lógica de negócio
    e mantendo a separação de responsabilidades.
    """

    def __init__(self, db_connection: Optional[DatabaseConnection] = None):
        """
        Inicializa o serviço

        Args:
            db_connection: Conexão com banco de dados (opcional)
        """
        self.db = db_connection or DatabaseConnection()

    def criar(self, nome: str, matricula: str) -> int:
        """
        Cria um novo aluno no sistema

        Args:
            nome: Nome do aluno
            matricula: Matrícula do aluno

        Returns:
            int: ID do aluno criado

        Raises:
            ValueError: Se dados inválidos
            Exception: Se matrícula já existe ou erro na criação
        """
        aluno = Aluno(id=None, nome=nome, matricula=matricula)

        # Verifica se matrícula já existe
        if self.buscar_por_matricula(aluno.matricula):
            raise Exception("Aluno já existe")

        try:
            query = (
                "INSERT INTO aluno (nome, matricula) VALUES (%s, %s) " "RETURNING id"
            )
            result = self.db.execute_query(query, (aluno.nome, aluno.matricula))

            if not result:
                raise Exception("Erro ao criar aluno")

            return result[0][0]
        except Exception as e:
            # Captura erros de constraint do banco
            if "duplicate key" in str(e) or "unique constraint" in str(e):
                raise Exception("Aluno já existe")
            raise e

    def buscar_por_id(self, id: int) -> Optional[Aluno]:
        """
        Busca um aluno pelo ID

        Args:
            id: ID do aluno

        Returns:
            Aluno encontrado ou None se não encontrado
        """
        if id <= 0:
            raise ValueError("ID deve ser maior que zero")

        query = "SELECT id, nome, matricula FROM aluno WHERE id = %s"
        result = self.db.execute_query(query, (id,))

        if not result:
            return None

        row = result[0]
        return Aluno(id=row[0], nome=row[1], matricula=row[2])

    def buscar_por_matricula(self, matricula: str) -> Optional[Aluno]:
        """
        Busca um aluno pela matrícula

        Args:
            matricula: Número de matrícula

        Returns:
            Aluno encontrado ou None se não encontrado
        """
        if not matricula or len(matricula.strip()) == 0:
            raise ValueError("Matrícula é obrigatória")

        query = "SELECT id, nome, matricula FROM aluno WHERE " "matricula = %s"
        result = self.db.execute_query(query, (matricula.strip(),))

        if not result:
            return None

        row = result[0]
        return Aluno(id=row[0], nome=row[1], matricula=row[2])

    def listar_todos(self) -> List[Aluno]:
        """
        Lista todos os alunos cadastrados

        Returns:
            Lista de alunos ordenada por nome
        """
        query = "SELECT id, nome, matricula FROM aluno ORDER BY nome, matricula"
        results = self.db.execute_query(query)

        if not results:
            return []

        return [Aluno(id=row[0], nome=row[1], matricula=row[2]) for row in results]

    def atualizar(self, id: int, nome: str, matricula: str) -> None:
        """
        Atualiza dados de um aluno

        Args:
            id: ID do aluno
            nome: Nome atualizado
            matricula: Matrícula atualizada

        Raises:
            ValueError: Se ID inválido
            Exception: Se aluno não encontrado ou matrícula já existe
        """
        if id <= 0:
            raise ValueError("ID deve ser maior que zero")

        # Verifica se aluno existe
        if not self.buscar_por_id(id):
            raise Exception("Aluno não encontrado")

        # Verifica se a matrícula já existe para outro aluno
        aluno_existente = self.buscar_por_matricula(matricula)
        if aluno_existente and aluno_existente.id != id:
            raise Exception("Aluno já existe")

        try:
            aluno = Aluno(id=id, nome=nome, matricula=matricula)
            query = "UPDATE aluno SET nome = %s, matricula = %s WHERE id = %s"
            self.db.execute_query(query, (aluno.nome, aluno.matricula, aluno.id))
        except Exception as e:
            # Captura erros de constraint do banco
            if "duplicate key" in str(e) or "unique constraint" in str(e):
                raise Exception("Aluno já existe")
            raise e

    def deletar(self, id: int) -> None:
        """
        Deleta um aluno do sistema

        Args:
            id: ID do aluno a ser deletado
        """
        if id <= 0:
            raise ValueError("ID deve ser maior que zero")

        # Verifica se aluno existe
        if not self.buscar_por_id(id):
            raise Exception("Aluno não encontrado")

        query = "DELETE FROM aluno WHERE id = %s"
        self.db.execute_query(query, (id,))

    def excluir(self, id: int) -> None:
        """
        Alias para deletar
        """
        self.deletar(id)
