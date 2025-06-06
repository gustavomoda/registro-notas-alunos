import logging
import sys
import tkinter as tk
from tkinter import messagebox, ttk

from registro_notas_alunos.gui.screens.gerenciar_alunos import GerenciarAlunosScreen
from registro_notas_alunos.gui.screens.gerenciar_disciplinas import (
    GerenciarDisciplinasScreen,
)
from registro_notas_alunos.gui.screens.gerenciar_matriculas import (
    GerenciarMatriculasScreen,
)
from registro_notas_alunos.gui.screens.gerenciar_notas import GerenciarNotasScreen
from registro_notas_alunos.gui.screens.relatorio_disciplina import (
    RelatorioDisciplinaScreen,
)

# Configurar logging para console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("sistema_notas.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("Sistema de Registro de Notas - Instituição de Ensino")
        self.root.geometry("600x450")
        self.root.resizable(True, True)

        # Centraliza a janela na tela
        self.center_window()

        # Loop até conseguir conectar ao banco
        self.wait_for_database_connection()

    def wait_for_database_connection(self):
        """Aguarda conexão com banco em loop - não permite usar sem banco"""
        while True:
            try:
                from registro_notas_alunos.backend.lib.database import (
                    DatabaseConnection,
                )

                db = DatabaseConnection()
                with db.get_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("SELECT 1")
                logger.info("Conexão com banco de dados estabelecida com sucesso")
                return True
            except Exception as e:
                logger.error(f"Erro na conexão com banco: {e}")
                # Mostrar mensagem e aguardar
                result = messagebox.askretrycancel(
                    "Erro de Conexão com Banco",
                    f"Não foi possível conectar ao banco de dados:\n{str(e)}\n\n"
                    "O sistema não pode funcionar sem banco de dados.\n\n"
                    "Clique 'Repetir' para tentar novamente ou 'Cancelar' para sair.",
                )
                if not result:
                    logger.info("Usuário cancelou conexão - encerrando aplicação")
                    self.root.destroy()
                    sys.exit(0)

    def check_backend_connection(self):
        """Verifica se é possível conectar ao banco de dados"""
        try:
            from registro_notas_alunos.backend.lib.database import DatabaseConnection

            db = DatabaseConnection()
            with db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Erro na verificação de conexão: {e}")
            return False

    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        """Cria os widgets da interface principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Título
        title_label = ttk.Label(
            main_frame, text="Sistema de Registro de Notas", font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Subtítulo com arquitetura
        subtitle_label = ttk.Label(
            main_frame,
            text="Arquitetura Package-as-Services | Princípios SOLID",
            font=("Arial", 10, "italic"),
        )
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        # Menu principal
        menu_label = ttk.Label(main_frame, text="Selecione uma opção:", font=("Arial", 12))
        menu_label.grid(row=2, column=0, columnspan=2, pady=(0, 15))

        # Botões do menu
        self.create_menu_buttons(main_frame)

        # Configurar redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def create_menu_buttons(self, parent):
        """Cria os botões do menu principal"""
        buttons = [
            ("Cadastro de Alunos", self.open_gerenciar_alunos, 3),
            ("Cadastro de Disciplinas", self.open_gerenciar_disciplinas, 4),
            ("Cadastro de Matrículas", self.open_gerenciar_matriculas, 5),
            ("Gerenciar Notas", self.open_gerenciar_notas, 6),
            ("Relatórios de Disciplinas", self.open_relatorio_disciplina, 7),
            ("Sair", self.quit_app, 9),
        ]

        for text, command, row in buttons:
            btn = ttk.Button(parent, text=text, command=command, width=40)
            btn.grid(row=row, column=0, columnspan=2, pady=8, padx=10, sticky="ew")

    def open_gerenciar_alunos(self):
        """Abre a tela de gerenciamento de alunos"""
        try:
            GerenciarAlunosScreen(self.root)
            logger.info("Tela de gerenciamento de alunos aberta")
        except Exception as e:
            logger.error(f"Erro ao abrir gerenciamento de alunos: {e}")
            messagebox.showerror("Erro", f"Erro ao abrir tela: {str(e)}")

    def open_gerenciar_disciplinas(self):
        """Abre a tela de gerenciamento de disciplinas"""
        try:
            GerenciarDisciplinasScreen(self.root)
            logger.info("Tela de gerenciamento de disciplinas aberta")
        except Exception as e:
            logger.error(f"Erro ao abrir gerenciamento de disciplinas: {e}")
            messagebox.showerror("Erro", f"Erro ao abrir tela: {str(e)}")

    def open_gerenciar_matriculas(self):
        """Abre a tela de gerenciamento de matrículas"""
        try:
            GerenciarMatriculasScreen(self.root)
            logger.info("Tela de gerenciamento de matrículas aberta")
        except Exception as e:
            logger.error(f"Erro ao abrir gerenciamento de matrículas: {e}")
            messagebox.showerror("Erro", f"Erro ao abrir tela: {str(e)}")

    def open_gerenciar_notas(self):
        """Abre a tela de gerenciamento de notas"""
        try:
            GerenciarNotasScreen(self.root)
            logger.info("Tela de gerenciamento de notas aberta")
        except Exception as e:
            logger.error(f"Erro ao abrir gerenciamento de notas: {e}")
            messagebox.showerror("Erro", f"Erro ao abrir tela: {str(e)}")

    def open_relatorio_disciplina(self):
        """Abre a tela de relatório por disciplina"""
        try:
            RelatorioDisciplinaScreen(self.root)
            logger.info("Tela de relatórios aberta")
        except Exception as e:
            logger.error(f"Erro ao abrir relatórios: {e}")
            messagebox.showerror("Erro", f"Erro ao abrir tela: {str(e)}")

    def quit_app(self):
        """Sai da aplicação"""
        if messagebox.askyesno("Sair", "Deseja realmente sair do sistema?"):
            logger.info("Usuário encerrou a aplicação")
            self.root.quit()

    def run(self):
        """Executa a aplicação"""
        try:
            logger.info("Iniciando aplicação")
            self.root.mainloop()
        except Exception as e:
            logger.error(f"Erro crítico na aplicação: {e}")
            messagebox.showerror("Erro Crítico", f"Erro na aplicação: {str(e)}")
            print(f"Erro crítico: {e}")
