import logging
import tkinter as tk
from tkinter import messagebox, ttk

from registro_notas_alunos.backend import DisciplinaService
from registro_notas_alunos.backend.lib.database import DatabaseConnection

logger = logging.getLogger(__name__)


class GerenciarDisciplinasScreen:
    def __init__(self, parent):
        self.parent = parent
        self.db = DatabaseConnection()
        self.disciplina_service = DisciplinaService(self.db)
        self.selected_disciplina = None
        self.create_window()

    def create_window(self):
        """Cria a janela de gerenciamento de disciplinas"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Cadastro de Disciplinas")
        self.window.geometry("950x600")
        self.window.resizable(True, True)

        self.center_window()
        self.create_widgets()
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
        title_label = ttk.Label(
            main_frame, text="Gerenciar Disciplinas", font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))

        # Frame formulário
        form_frame = ttk.LabelFrame(main_frame, text="Dados da Disciplina", padding="10")
        form_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 15))

        # Campos
        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.nome_entry = ttk.Entry(form_frame, width=35)
        self.nome_entry.grid(row=0, column=1, pady=5, padx=(10, 20))

        ttk.Label(form_frame, text="Ano:").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.ano_entry = ttk.Entry(form_frame, width=10)
        self.ano_entry.grid(row=0, column=3, pady=5, padx=(10, 20))

        ttk.Label(form_frame, text="Semestre:").grid(row=0, column=4, sticky=tk.W, pady=5)
        self.semestre_combo = ttk.Combobox(form_frame, values=["1", "2"], width=8, state="readonly")
        self.semestre_combo.grid(row=0, column=5, pady=5, padx=(10, 0))

        # Botões
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=1, column=0, columnspan=6, pady=15)

        buttons = [
            ("Incluir", self.incluir_disciplina),
            ("Alterar", self.alterar_disciplina),
            ("Excluir", self.excluir_disciplina),
            ("Atualizar", self.refresh_table),
            ("Limpar", self.limpar_campos),
        ]

        for i, (text, command) in enumerate(buttons):
            ttk.Button(button_frame, text=text, command=command).grid(row=0, column=i, padx=5)

        # Tabela
        table_frame = ttk.LabelFrame(main_frame, text="Lista de Disciplinas", padding="10")
        table_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=(0, 15))

        columns = ("ID", "Nome", "Ano", "Semestre")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        # Configurar colunas
        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.column("ID", width=60, anchor=tk.CENTER)
        self.tree.column("Nome", width=350, anchor=tk.W)
        self.tree.column("Ano", width=80, anchor=tk.CENTER)
        self.tree.column("Semestre", width=100, anchor=tk.CENTER)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Botão fechar
        ttk.Button(main_frame, text="Fechar", command=self.window.destroy).grid(
            row=3, column=0, columnspan=4, pady=15
        )

        # Configurar redimensionamento
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

    def refresh_table(self):
        """Atualiza a tabela"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            disciplinas = self.disciplina_service.listar_todas()

            for disc in disciplinas:
                self.tree.insert("", tk.END, values=(disc.id, disc.nome, disc.ano, disc.semestre))

            logger.info(f"Tabela disciplinas atualizada - {len(disciplinas)} registros")

        except Exception as e:
            logger.error(f"Erro ao atualizar tabela disciplinas: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar disciplinas:\n{str(e)}")

    def on_select(self, event):
        """Evento seleção"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item["values"]

            self.nome_entry.delete(0, tk.END)
            self.nome_entry.insert(0, values[1])
            self.ano_entry.delete(0, tk.END)
            self.ano_entry.insert(0, values[2])
            self.semestre_combo.set(values[3])

            self.selected_disciplina = values[0]

    def incluir_disciplina(self):
        """Inclui disciplina"""
        nome = self.nome_entry.get().strip()
        ano = self.ano_entry.get().strip()
        semestre = self.semestre_combo.get()

        if not nome or not ano or not semestre:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        try:
            ano = int(ano)
            semestre = int(semestre)

            self.disciplina_service.criar(nome=nome, ano=ano, semestre=semestre)
            self.refresh_table()
            self.limpar_campos()
            logger.info(f"Disciplina incluída: {nome} - {ano}/{semestre}")

        except Exception as e:
            logger.error(f"Erro ao incluir disciplina: {e}")
            error_msg = str(e)

            if "já existe" in error_msg:
                messagebox.showerror("Erro", "Esta disciplina já existe!")
            else:
                messagebox.showerror("Erro", "Erro ao salvar, entre em contato com o Suporte")

    def alterar_disciplina(self):
        """Altera disciplina selecionada"""
        if not self.selected_disciplina or not isinstance(self.selected_disciplina, int):
            messagebox.showerror("Erro", "Selecione uma disciplina!")
            return

        nome = self.nome_entry.get().strip()
        ano = self.ano_entry.get().strip()
        semestre = self.semestre_combo.get()

        if not nome or not ano or not semestre:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        try:
            ano = int(ano)
            semestre = int(semestre)

            self.disciplina_service.atualizar(
                id=int(self.selected_disciplina),
                nome=nome,
                ano=ano,
                semestre=semestre,
            )
            self.refresh_table()
            self.limpar_campos()
            logger.info(f"Disciplina alterada ID {self.selected_disciplina}")

        except Exception as e:
            logger.error(f"Erro ao alterar disciplina: {e}")
            error_msg = str(e)

            if "já existe" in error_msg:
                messagebox.showerror("Erro", "Esta disciplina já existe!")
            elif "não encontrada" in error_msg:
                messagebox.showerror("Erro", "Disciplina não encontrada!")
            else:
                messagebox.showerror("Erro", "Erro ao salvar, entre em contato com o Suporte")

    def excluir_disciplina(self):
        """Exclui disciplina"""
        if not self.selected_disciplina or not isinstance(self.selected_disciplina, int):
            messagebox.showerror("Erro", "Selecione uma disciplina!")
            return

        nome = self.nome_entry.get().strip()

        if messagebox.askyesno("Confirmar", f"Excluir disciplina:\n{nome}?"):
            try:
                self.disciplina_service.deletar(self.selected_disciplina)
                messagebox.showinfo("Sucesso", "Disciplina excluída!")
                self.refresh_table()
                self.limpar_campos()
                logger.info(f"Disciplina excluída ID {self.selected_disciplina}")

            except Exception as e:
                logger.error(f"Erro ao excluir disciplina: {e}")
                messagebox.showerror("Erro", "Erro ao salvar, entre em contato com o Suporte")

    def limpar_campos(self):
        """Limpa campos"""
        self.nome_entry.delete(0, tk.END)
        self.ano_entry.delete(0, tk.END)
        self.semestre_combo.set("")
        self.selected_disciplina = None
        self.tree.selection_remove(self.tree.selection())
