"""
Pacote Notas - Gerenciamento de Avaliações
=========================================

Modelo e serviços para operações com notas e avaliações.
"""

from registro_notas_alunos.backend.notas.model import Notas
from registro_notas_alunos.backend.notas.service import NotasService

__all__ = ["Notas", "NotasService"]
