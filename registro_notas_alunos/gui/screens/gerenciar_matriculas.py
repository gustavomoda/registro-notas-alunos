import logging
import tkinter as tk
from tkinter import messagebox, ttk

from registro_notas_alunos.backend import (AlunoService, DisciplinaService,
                                           MatriculaService)
from registro_notas_alunos.backend.lib.database import DatabaseConnection
from registro_notas_alunos.backend.matricula.model import Matricula
from registro_notas_alunos.backend.matricula.service import \
    MatriculaJaExisteException

logger = logging.getLogger(__name__)


class GerenciarMatriculasScreen:
    def __init__(self, parent):
        self.parent = parent
        self.db = DatabaseConnection()
        self.matricula_service = MatriculaService(self.db)
        self.aluno_service = AlunoService(self.db)
        self.disciplina_service = DisciplinaService(self.db)
        self.selected_matricula = None
        self.create_window()

    def create_window(self):
        """Cria a janela de gerenciamento de matrículas"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Cadastro de Matrículas")
        self.window.geometry("1000x650")
        self.window.resizable(True, True)

        self.center_window()
        self.create_widgets()
        self.load_combos()
        self.refresh_table()

    def center_window(self):
        """Centraliza a janela na tela"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        """Cria os widgets da tela"""
        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Título
        title_label = ttk.Label(main_frame, text="Gerenciar Matrículas", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Frame formulário
        form_frame = ttk.LabelFrame(main_frame, text="Dados da Matrícula", padding="10")
        form_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 15))

        # Aluno
        ttk.Label(form_frame, text="Aluno:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.aluno_combo = ttk.Combobox(form_frame, width=40, state="readonly")
        self.aluno_combo.grid(row=0, column=1, pady=5, padx=(10, 0))

        # Disciplina
        ttk.Label(form_frame, text="Disciplina:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.disciplina_combo = ttk.Combobox(form_frame, width=40, state="readonly")
        self.disciplina_combo.grid(row=1, column=1, pady=5, padx=(10, 0))

        # Botões
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=15)

        buttons = [
            ("Incluir", self.incluir_matricula),
            ("Excluir", self.excluir_matricula),
            ("Atualizar", self.refresh_table),
            ("Limpar", self.limpar_campos),
        ]

        for i, (text, command) in enumerate(buttons):
            ttk.Button(button_frame, text=text, command=command).grid(row=0, column=i, padx=5)

        # Tabela
        table_frame = ttk.LabelFrame(main_frame, text="Lista de Matrículas", padding="10")
        table_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(0, 15))

        columns = ("ID", "Aluno", "Matrícula", "Disciplina", "Ano", "Semestre")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        # Configurar colunas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Aluno", text="Aluno")
        self.tree.heading("Matrícula", text="Matrícula")
        self.tree.heading("Disciplina", text="Disciplina")
        self.tree.heading("Ano", text="Ano")
        self.tree.heading("Semestre", text="Semestre")

        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Aluno", width=200, anchor=tk.W)
        self.tree.column("Matrícula", width=120, anchor=tk.CENTER)
        self.tree.column("Disciplina", width=200, anchor=tk.W)
        self.tree.column("Ano", width=60, anchor=tk.CENTER)
        self.tree.column("Semestre", width=80, anchor=tk.CENTER)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Botão fechar
        ttk.Button(main_frame, text="Fechar", command=self.window.destroy).grid(
            row=3, column=0, columnspan=3, pady=15
        )

        # Configurar redimensionamento
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

    def load_combos(self):
        """Carrega dados nos comboboxes"""
        try:
            # Carregar alunos
            alunos = self.aluno_service.listar_todos()
            self.alunos_dict = {f"{aluno.nome} ({aluno.matricula})": aluno.id for aluno in alunos}
            self.aluno_combo["values"] = list(self.alunos_dict.keys())

            # Carregar disciplinas
            disciplinas = self.disciplina_service.listar_todas()
            self.disciplinas_dict = {
                f"{disc.nome} ({disc.ano}/{disc.semestre})": disc.id for disc in disciplinas
            }
            self.disciplina_combo["values"] = list(self.disciplinas_dict.keys())

        except Exception as e:
            logger.error(f"Erro ao carregar combos: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar dados:\n{str(e)}")

    def refresh_table(self):
        """Atualiza a tabela"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            matriculas = self.matricula_service.listar_todas()

            for mat in matriculas:
                self.tree.insert("", tk.END, values=mat)

            logger.info(f"Tabela matrículas atualizada - {len(matriculas)} registros")

        except Exception as e:
            logger.error(f"Erro ao atualizar tabela matrículas: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar matrículas:\n{str(e)}")

    def on_select(self, event):
        """Evento seleção"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item["values"]
            self.selected_matricula = values[0]

    def incluir_matricula(self):
        """Inclui matrícula"""
        aluno_sel = self.aluno_combo.get()
        disciplina_sel = self.disciplina_combo.get()

        if not aluno_sel or not disciplina_sel:
            messagebox.showerror("Erro", "Selecione aluno e disciplina!")
            return

        try:
            id_aluno = self.alunos_dict[aluno_sel]
            id_disciplina = self.disciplinas_dict[disciplina_sel]

            if not id_aluno or not id_disciplina:
                messagebox.showerror("Erro", "Erro interno: IDs não encontrados!")
                return

            matricula = Matricula(id=None, id_aluno=id_aluno, id_disciplina=id_disciplina)
            self.matricula_service.criar(matricula)
            self.refresh_table()
            self.limpar_campos(manter_aluno=True)
            logger.info(f"Matrícula incluída: aluno {id_aluno} -> disciplina {id_disciplina}")

        except MatriculaJaExisteException as e:
            logger.info(f"Tentativa de incluir matrícula duplicada: {e}")
            messagebox.showinfo("Informação", "O aluno já está matriculado!")
        except Exception as e:
            logger.error(f"Erro ao incluir matrícula: {e}")
            messagebox.showerror("Erro", "Erro ao salvar, entre em contato com o Suporte")

    def excluir_matricula(self):
        """Exclui matrícula"""
        if not self.selected_matricula:
            messagebox.showerror("Erro", "Selecione uma matrícula!")
            return

        if messagebox.askyesno("Confirmar", "Excluir matrícula selecionada?"):
            try:
                self.matricula_service.deletar(int(self.selected_matricula))
                self.refresh_table()
                self.limpar_campos()
                logger.info(f"Matrícula excluída ID {self.selected_matricula}")

            except Exception as e:
                logger.error(f"Erro ao excluir matrícula: {e}")
                messagebox.showerror("Erro", "Erro ao salvar, entre em contato com o Suporte")

    def limpar_campos(self, manter_aluno=False):
        """Limpa campos"""
        if not manter_aluno:
            self.aluno_combo.set("")
        self.disciplina_combo.set("")
        self.selected_matricula = None
        self.tree.selection_remove(self.tree.selection())
