"""
Modelo de dados para Matrícula
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Matricula:
    """
    Representa uma matrícula de aluno em disciplina
    
    Attributes:
        id: Identificador único da matrícula
        id_aluno: ID do aluno matriculado
        id_disciplina: ID da disciplina
    """
    id: Optional[int]
    id_aluno: int
    id_disciplina: int
    
    def __post_init__(self):
        """Validações após inicialização"""
        if self.id_aluno <= 0:
            raise ValueError("ID do aluno deve ser maior que zero")
        
        if self.id_disciplina <= 0:
            raise ValueError("ID da disciplina deve ser maior que zero") 