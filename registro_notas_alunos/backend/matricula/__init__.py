"""
Pacote Matrícula - Gerenciamento de Vínculos
===========================================

Modelo e serviços para operações com matrículas.
"""

from registro_notas_alunos.backend.matricula.model import Matricula
from registro_notas_alunos.backend.matricula.service import MatriculaService

__all__ = ["Matricula", "MatriculaService"]
