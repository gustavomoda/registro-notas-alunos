"""
Modelo de dados para Disciplina
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Disciplina:
    """
    Representa uma disciplina no sistema

    Attributes:
        id: Identificador único da disciplina
        nome: Nome da disciplina
        ano: Ano letivo
        semestre: Semestre (1 ou 2)
    """

    id: Optional[int]
    nome: str
    ano: int
    semestre: int

    def __post_init__(self):
        """Validações após inicialização"""
        if not self.nome or len(self.nome.strip()) == 0:
            raise ValueError("Nome da disciplina é obrigatório")

        if self.ano < 2020 or self.ano > 2030:
            raise ValueError("Ano deve estar entre 2020 e 2030")

        if self.semestre not in [1, 2]:
            raise ValueError("Semestre deve ser 1 ou 2")

        # Normaliza os dados
        self.nome = self.nome.strip()
