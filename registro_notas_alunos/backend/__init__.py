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
from registro_notas_alunos.backend.aluno import Aluno, AlunoService
from registro_notas_alunos.backend.disciplina import (Disciplina,
                                                      DisciplinaService)
# Importa infraestrutura
from registro_notas_alunos.backend.lib.database import DatabaseConnection
from registro_notas_alunos.backend.matricula import Matricula, MatriculaService
from registro_notas_alunos.backend.notas import Notas, NotasService

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
