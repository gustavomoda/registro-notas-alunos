"""
Value Objects para o módulo de Notas
"""

from dataclasses import dataclass
from typing import Optional

from registro_notas_alunos.backend.disciplina.model import Disciplina


@dataclass
class AlunoNotaApuradoVO:
    """
    Value Object que representa a nota apurada de um aluno em uma disciplina
    """

    id_nota: int
    nome_aluno: str
    disciplina: Disciplina
    sm1: Optional[float]
    sm2: Optional[float]
    av: Optional[float]
    avs: Optional[float]
    nota_final: float
    situacao: str

    def is_aprovado(self) -> bool:
        """
        Verifica se o aluno foi aprovado

        Returns:
            bool: True se aprovado, False caso contrário
        """
        return self.situacao == "APROVADO"

    def is_reprovado(self) -> bool:
        """
        Verifica se o aluno foi reprovado

        Returns:
            bool: True se reprovado, False caso contrário
        """
        return self.situacao == "REPROVADO"

    def is_pendente(self) -> bool:
        """
        Verifica se a situação está pendente (notas incompletas)

        Returns:
            bool: True se pendente, False caso contrário
        """
        return self.situacao == "PENDENTE"

    def get_sm1_display(self) -> str:
        """Retorna SM1 para exibição"""
        return str(self.sm1) if self.sm1 is not None else ""

    def get_sm2_display(self) -> str:
        """Retorna SM2 para exibição"""
        return str(self.sm2) if self.sm2 is not None else ""

    def get_av_display(self) -> str:
        """Retorna AV para exibição"""
        return str(self.av) if self.av is not None else ""

    def get_avs_display(self) -> str:
        """Retorna AVS para exibição"""
        return str(self.avs) if self.avs is not None else ""

    def get_nota_final_display(self) -> str:
        """Retorna nota final formatada para exibição"""
        if self.is_pendente():
            return "--"
        return f"{self.nota_final:.2f}".replace(".", ",")
