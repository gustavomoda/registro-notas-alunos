"""
Serviço para operações com Matrícula
"""

from typing import List, Optional, Tuple
from ..lib.database import DatabaseConnection
from .model import Matricula


class MatriculaService:
    """
    Serviço responsável pelas operações de negócio relacionadas a Matrícula
    """
    
    def __init__(self, db_connection: Optional[DatabaseConnection] = None):
        """
        Inicializa o serviço
        
        Args:
            db_connection: Conexão com banco de dados (opcional)
        """
        self.db = db_connection or DatabaseConnection()
    
    def criar(self, matricula: Matricula) -> int:
        """
        Cria uma nova matrícula no sistema
        
        Args:
            matricula: Dados da matrícula a ser criada
            
        Returns:
            int: ID da matrícula criada
            
        Raises:
            ValueError: Se dados inválidos
            Exception: Se matrícula já existe ou erro na criação
        """
        if matricula.id is not None:
            raise ValueError("Matrícula para criação não deve ter ID")
        
        # Verifica se matrícula já existe
        if self.buscar_por_aluno_disciplina(matricula.id_aluno, matricula.id_disciplina):
            raise Exception("Aluno já matriculado nesta disciplina")
        
        query = "INSERT INTO matricula (id_aluno, id_disciplina) VALUES (%s, %s) RETURNING id"
        result = self.db.execute_query(query, (matricula.id_aluno, matricula.id_disciplina))
        
        if not result:
            raise Exception("Erro ao criar matrícula")
        
        return result[0][0]
    
    def buscar_por_id(self, id: int) -> Optional[Matricula]:
        """
        Busca uma matrícula pelo ID
        
        Args:
            id: ID da matrícula
            
        Returns:
            Matrícula encontrada ou None se não encontrada
        """
        if id <= 0:
            raise ValueError("ID deve ser maior que zero")
        
        query = "SELECT id, id_aluno, id_disciplina FROM matricula WHERE id = %s"
        result = self.db.execute_query(query, (id,))
        
        if not result:
            return None
        
        row = result[0]
        return Matricula(id=row[0], id_aluno=row[1], id_disciplina=row[2])
    
    def buscar_por_aluno_disciplina(self, id_aluno: int, id_disciplina: int) -> Optional[Matricula]:
        """
        Busca matrícula por aluno e disciplina
        
        Args:
            id_aluno: ID do aluno
            id_disciplina: ID da disciplina
            
        Returns:
            Matrícula encontrada ou None se não encontrada
        """
        if id_aluno <= 0:
            raise ValueError("ID do aluno deve ser maior que zero")
        if id_disciplina <= 0:
            raise ValueError("ID da disciplina deve ser maior que zero")
        
        query = "SELECT id, id_aluno, id_disciplina FROM matricula WHERE id_aluno = %s AND id_disciplina = %s"
        result = self.db.execute_query(query, (id_aluno, id_disciplina))
        
        if not result:
            return None
        
        row = result[0]
        return Matricula(id=row[0], id_aluno=row[1], id_disciplina=row[2])
    
    def listar_por_disciplina(self, id_disciplina: int) -> List[Tuple[int, str, str]]:
        """
        Lista matrículas de uma disciplina com dados do aluno
        
        Args:
            id_disciplina: ID da disciplina
            
        Returns:
            Lista de tuplas (id_matricula, nome_aluno, matricula_aluno)
        """
        if id_disciplina <= 0:
            raise ValueError("ID da disciplina deve ser maior que zero")
        
        query = """
            SELECT m.id, a.nome, a.matricula 
            FROM matricula m 
            JOIN aluno a ON m.id_aluno = a.id 
            WHERE m.id_disciplina = %s 
            ORDER BY a.nome
        """
        return self.db.execute_query(query, (id_disciplina,))
    
    def listar_por_aluno(self, id_aluno: int) -> List[Tuple[int, str, int, int]]:
        """
        Lista matrículas de um aluno com dados da disciplina
        
        Args:
            id_aluno: ID do aluno
            
        Returns:
            Lista de tuplas (id_matricula, nome_disciplina, ano, semestre)
        """
        if id_aluno <= 0:
            raise ValueError("ID do aluno deve ser maior que zero")
        
        query = """
            SELECT m.id, d.nome, d.ano, d.semestre 
            FROM matricula m 
            JOIN disciplina d ON m.id_disciplina = d.id 
            WHERE m.id_aluno = %s 
            ORDER BY d.ano, d.semestre, d.nome
        """
        return self.db.execute_query(query, (id_aluno,))
    
    def listar_todas(self) -> List[Tuple[int, str, str, str]]:
        """
        Lista todas as matrículas com dados do aluno e disciplina
        
        Returns:
            Lista de tuplas (id_matricula, nome_aluno, matricula_aluno, nome_disciplina)
        """
        query = """
            SELECT m.id, a.nome, a.matricula, d.nome as disciplina 
            FROM matricula m 
            JOIN aluno a ON m.id_aluno = a.id 
            JOIN disciplina d ON m.id_disciplina = d.id 
            ORDER BY d.nome, a.nome
        """
        return self.db.execute_query(query)
    
    def excluir(self, id: int) -> None:
        """
        Exclui uma matrícula do sistema
        
        Args:
            id: ID da matrícula a ser excluída
        """
        if id <= 0:
            raise ValueError("ID deve ser maior que zero")
        
        # Verifica se matrícula existe
        if not self.buscar_por_id(id):
            raise Exception(f"Matrícula com ID {id} não encontrada")
        
        query = "DELETE FROM matricula WHERE id = %s"
        self.db.execute_query(query, (id,))
    
    def excluir_por_aluno_disciplina(self, id_aluno: int, id_disciplina: int) -> None:
        """
        Exclui matrícula por aluno e disciplina
        
        Args:
            id_aluno: ID do aluno
            id_disciplina: ID da disciplina
        """
        matricula = self.buscar_por_aluno_disciplina(id_aluno, id_disciplina)
        if not matricula:
            raise Exception("Matrícula não encontrada")
        
        self.excluir(matricula.id) 