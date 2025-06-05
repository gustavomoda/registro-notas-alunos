"""
Serviço para operações com Notas
"""

from typing import List, Optional, Tuple

from ..lib.database import DatabaseConnection
from .model import Notas


class NotasService:
    """
    Serviço responsável pelas operações de negócio relacionadas a Notas
    """

    def __init__(self, db_connection: Optional[DatabaseConnection] = None):
        """
        Inicializa o serviço

        Args:
            db_connection: Conexão com banco de dados (opcional)
        """
        self.db = db_connection or DatabaseConnection()

    def criar(self, notas: Notas) -> int:
        """
        Cria um novo registro de notas no sistema

        Args:
            notas: Dados das notas a serem criadas

        Returns:
            int: ID do registro de notas criado

        Raises:
            ValueError: Se dados inválidos
            Exception: Se notas já existem ou erro na criação
        """
        if notas.id is not None:
            raise ValueError("Notas para criação não devem ter ID")

        # Verifica se já existem notas para esta matrícula
        if self.buscar_por_matricula(notas.id_matricula):
            raise Exception("Notas já existem")

        try:
            # Calcula nota final antes de salvar
            notas.calcular_nota_final()

            query = """
                INSERT INTO notas (id_matricula, sm1, sm2, av, avs, nf, situacao)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            params = (
                notas.id_matricula,
                notas.sm1,
                notas.sm2,
                notas.av,
                notas.avs,
                notas.nf,
                notas.situacao,
            )
            result = self.db.execute_query(query, params)

            if not result:
                raise Exception("Erro ao criar registro de notas")

            return result[0][0]
        except Exception as e:
            # Captura erros de constraint do banco
            if "duplicate key" in str(e) or "unique constraint" in str(e):
                raise Exception("Notas já existem")
            raise e

    def buscar_por_id(self, id: int) -> Optional[Notas]:
        """
        Busca um registro de notas pelo ID

        Args:
            id: ID do registro de notas

        Returns:
            Notas encontradas ou None se não encontradas
        """
        if id <= 0:
            raise ValueError("ID deve ser maior que zero")

        query = "SELECT * FROM notas WHERE id = %s"
        result = self.db.execute_query(query, (id,))

        if not result:
            return None

        row = result[0]
        return Notas(
            id=row[0],
            id_matricula=row[1],
            sm1=row[2],
            sm2=row[3],
            av=row[4],
            avs=row[5],
            nf=row[6],
            situacao=row[7],
        )

    def buscar_por_matricula(self, id_matricula: int) -> Optional[Notas]:
        """
        Busca notas por ID da matrícula

        Args:
            id_matricula: ID da matrícula

        Returns:
            Notas encontradas ou None se não encontradas
        """
        if id_matricula <= 0:
            raise ValueError("ID da matrícula deve ser maior que zero")

        query = "SELECT * FROM notas WHERE id_matricula = %s"
        result = self.db.execute_query(query, (id_matricula,))

        if not result:
            return None

        row = result[0]
        return Notas(
            id=row[0],
            id_matricula=row[1],
            sm1=row[2],
            sm2=row[3],
            av=row[4],
            avs=row[5],
            nf=row[6],
            situacao=row[7],
        )

    def atualizar(self, notas: Notas) -> None:
        """
        Atualiza um registro de notas

        Args:
            notas: Dados atualizados das notas

        Raises:
            ValueError: Se ID inválido
            Exception: Se notas não encontradas
        """
        if notas.id is None or notas.id <= 0:
            raise ValueError("Notas devem ter ID válido para atualização")

        # Verifica se registro existe
        if not self.buscar_por_id(notas.id):
            raise Exception("Notas não encontradas")

        try:
            # Calcula nota final antes de atualizar
            notas.calcular_nota_final()

            query = """
                UPDATE notas
                SET sm1 = %s, sm2 = %s, av = %s, avs = %s, nf = %s, situacao = %s
                WHERE id = %s
            """
            params = (
                notas.sm1,
                notas.sm2,
                notas.av,
                notas.avs,
                notas.nf,
                notas.situacao,
                notas.id,
            )
            self.db.execute_query(query, params)
        except Exception as e:
            # Captura erros de constraint do banco
            if "duplicate key" in str(e) or "unique constraint" in str(e):
                raise Exception("Notas já existem")
            raise e

    def atualizar_por_matricula(self, notas: Notas) -> None:
        """
        Atualiza notas usando ID da matrícula

        Args:
            notas: Dados das notas com id_matricula
        """
        notas_existentes = self.buscar_por_matricula(notas.id_matricula)
        if not notas_existentes:
            # Se não existem notas, cria um novo registro
            self.criar(notas)
        else:
            # Se existem, atualiza o registro existente
            notas.id = notas_existentes.id
            self.atualizar(notas)

    def listar_por_disciplina(
        self, id_disciplina: int
    ) -> List[Tuple[str, str, float, float, float, float, float, str]]:
        """
        Lista notas de todos os alunos de uma disciplina

        Args:
            id_disciplina: ID da disciplina

        Returns:
            Lista de tuplas (nome_aluno, matricula_aluno, sm1, sm2, av, avs, nf, situacao)
        """
        if id_disciplina <= 0:
            raise ValueError("ID da disciplina deve ser maior que zero")

        query = """
            SELECT a.nome, a.matricula, n.sm1, n.sm2, n.av, n.avs, n.nf, n.situacao
            FROM notas n
            JOIN matricula m ON n.id_matricula = m.id
            JOIN aluno a ON m.id_aluno = a.id
            WHERE m.id_disciplina = %s
            ORDER BY a.nome
        """
        return self.db.execute_query(query, (id_disciplina,))

    def listar_por_aluno(
        self, id_aluno: int
    ) -> List[Tuple[str, int, int, float, float, float, float, float, str]]:
        """
        Lista notas de um aluno em todas as disciplinas

        Args:
            id_aluno: ID do aluno

        Returns:
            Lista de tuplas (nome_disciplina, ano, semestre, sm1, sm2, av, avs, nf, situacao)
        """
        if id_aluno <= 0:
            raise ValueError("ID do aluno deve ser maior que zero")

        query = """
            SELECT d.nome, d.ano, d.semestre, n.sm1, n.sm2, n.av, n.avs, n.nf, n.situacao
            FROM notas n
            JOIN matricula m ON n.id_matricula = m.id
            JOIN disciplina d ON m.id_disciplina = d.id
            WHERE m.id_aluno = %s
            ORDER BY d.ano, d.semestre, d.nome
        """
        return self.db.execute_query(query, (id_aluno,))

    def calcular_todas_notas_finais(self) -> int:
        """
        Recalcula todas as notas finais do sistema

        Returns:
            int: Número de registros atualizados
        """
        # Busca todos os registros de notas
        query = "SELECT * FROM notas"
        results = self.db.execute_query(query)

        contador = 0
        for row in results:
            notas = Notas(
                id=row[0],
                id_matricula=row[1],
                sm1=row[2],
                sm2=row[3],
                av=row[4],
                avs=row[5],
                nf=row[6],
                situacao=row[7],
            )

            # Recalcula e atualiza
            notas.calcular_nota_final()
            self.atualizar(notas)
            contador += 1

        return contador

    def excluir(self, id: int) -> None:
        """
        Exclui um registro de notas

        Args:
            id: ID do registro de notas a ser excluído
        """
        if id <= 0:
            raise ValueError("ID deve ser maior que zero")

        # Verifica se registro existe
        if not self.buscar_por_id(id):
            raise Exception("Notas não encontradas")

        query = "DELETE FROM notas WHERE id = %s"
        self.db.execute_query(query, (id,))

    def excluir_por_matricula(self, id_matricula: int) -> None:
        """
        Exclui notas por ID da matrícula

        Args:
            id_matricula: ID da matrícula
        """
        if id_matricula <= 0:
            raise ValueError("ID da matrícula deve ser maior que zero")

        notas = self.buscar_por_matricula(id_matricula)
        if not notas:
            raise Exception("Notas não encontradas")

        self.excluir(notas.id)
