import os

from dotenv import load_dotenv
from psycopg2 import pool

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()


class DatabaseConnection:
    _instance = None
    _pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._initialize_pool()
        return cls._instance

    @classmethod
    def _initialize_pool(cls):
        if cls._pool is None:
            try:
                cls._pool = pool.SimpleConnectionPool(
                    minconn=1,
                    maxconn=10,
                    host=os.getenv("DB_HOST"),
                    port=os.getenv("DB_PORT"),
                    database=os.getenv("DB_NAME"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                )
            except Exception as e:
                print(f"Erro ao criar pool de conexões: {e}")
                raise

    def get_connection(self):
        """Retorna uma conexão do pool"""
        return self._pool.getconn()

    def release_connection(self, conn):
        """Libera uma conexão de volta para o pool"""
        self._pool.putconn(conn)

    def execute_query(self, query, params=None):
        """Executa uma query e retorna os resultados"""
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                # Retorna dados para SELECT e comandos com RETURNING
                query_upper = query.strip().upper()
                if query_upper.startswith("SELECT") or "RETURNING" in query_upper:
                    result = cur.fetchall()
                    # Também faz commit para comandos com RETURNING (INSERT, UPDATE, DELETE)
                    if not query_upper.startswith("SELECT"):
                        conn.commit()
                    return result
                conn.commit()
                return None
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Erro ao executar query: {e}")
            raise
        finally:
            if conn:
                self.release_connection(conn)

    def close(self):
        """Fecha o pool de conexões"""
        if self._pool:
            self._pool.closeall()
            self._pool = None
