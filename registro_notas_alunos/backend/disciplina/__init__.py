"""
Pacote Disciplina - Gerenciamento de Matérias
============================================

Modelo e serviços para operações com disciplinas.
"""

from registro_notas_alunos.backend.disciplina.model import Disciplina
from registro_notas_alunos.backend.disciplina.service import DisciplinaService

__all__ = ["Disciplina", "DisciplinaService"]
