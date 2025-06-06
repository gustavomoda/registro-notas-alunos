"""
Pacote Aluno - Gerenciamento de Estudantes
=========================================

Modelo e serviços para operações com alunos.
"""

from registro_notas_alunos.backend.aluno.model import Aluno
from registro_notas_alunos.backend.aluno.service import AlunoService

__all__ = ["Aluno", "AlunoService"]
