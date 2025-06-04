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
            db_connection: Conexão com banco de dados (opcional, criará uma nova se não fornecida)
        """
        self.db = db_connection or DatabaseConnection()
    
    def criar(self, aluno: Aluno) -> int:
        """
        Cria um novo aluno no sistema
        
        Args:
            aluno: Dados do aluno a ser criado
            
        Returns:
            int: ID do aluno criado
            
        Raises:
            ValueError: Se dados do aluno são inválidos
            Exception: Se erro na criação
        """
        if aluno.id is not None:
            raise ValueError("Aluno para criação não deve ter ID")
        
        query = "INSERT INTO aluno (nome, matricula) VALUES (%s, %s) RETURNING id"
        result = self.db.execute_query(query, (aluno.nome, aluno.matricula))
        
        if not result:
            raise Exception("Erro ao criar aluno")
        
        return result[0][0]
    
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
        
        query = "SELECT id, nome, matricula FROM aluno WHERE matricula = %s"
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
        query = "SELECT id, nome, matricula FROM aluno ORDER BY nome"
        results = self.db.execute_query(query)
        
        return [
            Aluno(id=row[0], nome=row[1], matricula=row[2])
            for row in results
        ]
    
    def atualizar(self, aluno: Aluno) -> None:
        """
        Atualiza dados de um aluno
        
        Args:
            aluno: Dados atualizados do aluno
            
        Raises:
            ValueError: Se aluno não tem ID
            Exception: Se aluno não encontrado
        """
        if aluno.id is None or aluno.id <= 0:
            raise ValueError("Aluno deve ter ID válido para atualização")
        
        # Verifica se aluno existe
        if not self.buscar_por_id(aluno.id):
            raise Exception(f"Aluno com ID {aluno.id} não encontrado")
        
        query = "UPDATE aluno SET nome = %s, matricula = %s WHERE id = %s"
        self.db.execute_query(query, (aluno.nome, aluno.matricula, aluno.id))
    
    def excluir(self, id: int) -> None:
        """
        Exclui um aluno do sistema
        
        Args:
            id: ID do aluno a ser excluído
            
        Raises:
            ValueError: Se ID inválido
            Exception: Se aluno não encontrado
        """
        if id <= 0:
            raise ValueError("ID deve ser maior que zero")
        
        # Verifica se aluno existe
        if not self.buscar_por_id(id):
            raise Exception(f"Aluno com ID {id} não encontrado")
        
        query = "DELETE FROM aluno WHERE id = %s"
        self.db.execute_query(query, (id,)) 