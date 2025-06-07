"""
Modelo de dados para Notas
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Notas:
    """
    Representa as notas de um aluno em uma disciplina

    Attributes:
        id: Identificador único do registro de notas
        id_matricula: ID da matrícula relacionada
        sm1: Nota da Suplementar 1 (0.0 a 1.0)
        sm2: Nota da Suplementar 2 (0.0 a 1.0)
        av: Nota da Avaliação (0.0 a 10.0)
        avs: Nota da Avaliação Substitutiva (0.0 a 10.0)
        nf: Nota Final calculada
        situacao: Situação do aluno (Aprovado/Reprovado/Em Avaliação)
    """

    id: Optional[int]
    id_matricula: int
    sm1: Optional[float] = 0.0
    sm2: Optional[float] = 0.0
    av: Optional[float] = 0.0
    avs: Optional[float] = 0.0
    nf: float = 0.0
    situacao: str = "Em Avaliação"

    def __post_init__(self):
        """Validações após inicialização"""
        if self.id_matricula <= 0:
            raise ValueError("ID da matrícula deve ser maior que zero")

        self._validar_notas()

    def _validar_notas(self):
        """Valida se as notas estão dentro dos limites permitidos"""
        if self.sm1 is not None and not (0.0 <= self.sm1 <= 1.0):
            raise ValueError("SM1 deve estar entre 0.0 e 1.0")

        if self.sm2 is not None and not (0.0 <= self.sm2 <= 1.0):
            raise ValueError("SM2 deve estar entre 0.0 e 1.0")

        if self.av is not None and not (0.0 <= self.av <= 10.0):
            raise ValueError("AV deve estar entre 0.0 e 10.0")

        if self.avs is not None and not (0.0 <= self.avs <= 10.0):
            raise ValueError("AVS deve estar entre 0.0 e 10.0")

    def calcular_nota_final(self) -> float:
        """
        Calcula a nota final baseada nas regras do sistema

        Returns:
            float: Nota final calculada
        """
        # Usa AVS se for maior que AV, tratando None como 0
        av_valor = self.av if self.av is not None else 0.0
        avs_valor = self.avs if self.avs is not None else 0.0
        nota_av = max(av_valor, avs_valor)

        # Calcula pontos extras (máximo 2 pontos), tratando None como 0
        sm1_valor = self.sm1 if self.sm1 is not None else 0.0
        sm2_valor = self.sm2 if self.sm2 is not None else 0.0
        pontos_extras = min(sm1_valor, 1.0) + min(sm2_valor, 1.0)

        # Nota final é a soma da nota AV com os pontos extras
        self.nf = nota_av + pontos_extras

        # Atualiza situação
        self.situacao = "Aprovado" if self.nf >= 6.0 else "Reprovado"

        return self.nf
