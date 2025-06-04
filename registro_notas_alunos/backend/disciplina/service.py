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
    
    def criar(self, disciplina: Disciplina) -> int:
        """
        Cria uma nova disciplina no sistema
        
        Args:
            disciplina: Dados da disciplina a ser criada
            
        Returns:
            int: ID da disciplina criada
        """
        if disciplina.id is not None:
            raise ValueError("Disciplina para criação não deve ter ID")
        
        query = "INSERT INTO disciplina (nome, ano, semestre) VALUES (%s, %s, %s) RETURNING id"
        result = self.db.execute_query(query, (disciplina.nome, disciplina.ano, disciplina.semestre))
        
        if not result:
            raise Exception("Erro ao criar disciplina")
        
        return result[0][0]
    
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
        
        return [
            Disciplina(id=row[0], nome=row[1], ano=row[2], semestre=row[3])
            for row in results
        ]
    
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
        
        return [
            Disciplina(id=row[0], nome=row[1], ano=row[2], semestre=row[3])
            for row in results
        ]
    
    def atualizar(self, disciplina: Disciplina) -> None:
        """
        Atualiza dados de uma disciplina
        
        Args:
            disciplina: Dados atualizados da disciplina
        """
        if disciplina.id is None or disciplina.id <= 0:
            raise ValueError("Disciplina deve ter ID válido para atualização")
        
        # Verifica se disciplina existe
        if not self.buscar_por_id(disciplina.id):
            raise Exception(f"Disciplina com ID {disciplina.id} não encontrada")
        
        query = "UPDATE disciplina SET nome = %s, ano = %s, semestre = %s WHERE id = %s"
        self.db.execute_query(query, (disciplina.nome, disciplina.ano, disciplina.semestre, disciplina.id))
    
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
            raise Exception(f"Disciplina com ID {id} não encontrada")
        
        query = "DELETE FROM disciplina WHERE id = %s"
        self.db.execute_query(query, (id,)) 