"""
Backend do Sistema de Registro de Notas
======================================

Arquitetura baseada em package-as-services seguindo princípios SOLID.

Cada entidade tem seu próprio pacote com model e service:
- Aluno: Gerenciamento de estudantes
- Disciplina: Gerenciamento de matérias
- Matricula: Gerenciamento de vínculos
- Notas: Gerenciamento de avaliações
"""

# Importa models
from .aluno import Aluno, AlunoService
from .disciplina import Disciplina, DisciplinaService
from .matricula import Matricula, MatriculaService
from .notas import Notas, NotasService

# Importa infraestrutura
from .lib.database import DatabaseConnection

__all__ = [
    "Aluno",
    "AlunoService",
    "Disciplina",
    "DisciplinaService",
    "Matricula",
    "MatriculaService",
    "Notas",
    "NotasService",
    "DatabaseConnection",
]
