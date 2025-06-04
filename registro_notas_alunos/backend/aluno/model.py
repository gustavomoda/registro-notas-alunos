"""
Modelo de dados para Aluno
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Aluno:
    """
    Representa um aluno no sistema
    
    Attributes:
        id: Identificador único do aluno
        nome: Nome completo do aluno
        matricula: Número de matrícula único
    """
    id: Optional[int]
    nome: str
    matricula: str
    
    def __post_init__(self):
        """Validações após inicialização"""
        if not self.nome or len(self.nome.strip()) == 0:
            raise ValueError("Nome do aluno é obrigatório")
        
        if not self.matricula or len(self.matricula.strip()) == 0:
            raise ValueError("Matrícula do aluno é obrigatória")
        
        # Normaliza os dados
        self.nome = self.nome.strip()
        self.matricula = self.matricula.strip() 