import logging
import tkinter as tk
from tkinter import messagebox, ttk

from registro_notas_alunos.backend import AlunoService
from registro_notas_alunos.backend.lib.database import DatabaseConnection
from registro_notas_alunos.gui.screens.exceptions import (
    DatabaseConnectionError,
    DataNotFoundError,
    SelectionError,
    ValidationError,
)

logger = logging.getLogger(__name__)


class GerenciarAlunosScreen:
    def __init__(self, parent):
        self.parent = parent
        self.db = DatabaseConnection()
        self.aluno_service = AlunoService(self.db)
        self.selected_aluno = None
        self.create_window()

    def create_window(self):
        """Cria a janela de gerenciamento de alunos"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Cadastro de Alunos")
        self.window.geometry("900x600")
        self.window.resizable(True, True)

        # Centralizar janela
        self.center_window()

        # Criar widgets
        self.create_widgets()

        # Carregar dados iniciais
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
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Título
        title_label = ttk.Label(main_frame, text="Gerenciar Alunos", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Frame para formulário
        form_frame = ttk.LabelFrame(main_frame, text="Dados do Aluno", padding="10")
        form_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 15))

        # Campos do formulário
        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.nome_entry = ttk.Entry(form_frame, width=40)
        self.nome_entry.grid(row=0, column=1, pady=5, padx=(10, 20))

        ttk.Label(form_frame, text="Matrícula:").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.matricula_entry = ttk.Entry(form_frame, width=20)
        self.matricula_entry.grid(row=0, column=3, pady=5, padx=(10, 0))

        # Botões de ação
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=1, column=0, columnspan=4, pady=15)

        ttk.Button(button_frame, text="Incluir", command=self.incluir_aluno).grid(
            row=0, column=0, padx=5
        )

        ttk.Button(button_frame, text="Alterar", command=self.alterar_aluno).grid(
            row=0, column=1, padx=5
        )

        ttk.Button(button_frame, text="Excluir", command=self.excluir_aluno).grid(
            row=0, column=2, padx=5
        )

        ttk.Button(button_frame, text="Atualizar", command=self.refresh_table).grid(
            row=0, column=3, padx=5
        )

        ttk.Button(button_frame, text="Limpar", command=self.limpar_campos).grid(
            row=0, column=4, padx=5
        )

        # Frame para a tabela
        table_frame = ttk.LabelFrame(main_frame, text="Lista de Alunos", padding="10")
        table_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(0, 15))

        # Treeview (tabela)
        columns = ("ID", "Nome", "Matrícula")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        # Configurar colunas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Matrícula", text="Matrícula")

        self.tree.column("ID", width=60, anchor=tk.CENTER)
        self.tree.column("Nome", width=300, anchor=tk.W)
        self.tree.column("Matrícula", width=150, anchor=tk.CENTER)

        # Scrollbar para a tabela
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Grid da tabela
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Bind para seleção
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

    def refresh_table(self):
        """Atualiza a tabela com os dados dos alunos"""
        try:
            # Limpar tabela
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Buscar alunos
            alunos = self.aluno_service.listar_todos()

            # Inserir na tabela
            for aluno in alunos:
                self.tree.insert("", tk.END, values=(aluno.id, aluno.nome, aluno.matricula))

            logger.info(f"Tabela de alunos atualizada - {len(alunos)} registros")

        except Exception as e:
            logger.error(f"Erro ao atualizar tabela de alunos: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar alunos:\n{str(e)}")

    def on_select(self, event):
        """Evento de seleção na tabela"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item["values"]

            # Preencher campos
            self.nome_entry.delete(0, tk.END)
            self.nome_entry.insert(0, values[1])
            self.matricula_entry.delete(0, tk.END)
            self.matricula_entry.insert(0, values[2])

            # Guardar ID selecionado
            self.selected_aluno = values[0]

    def incluir_aluno(self):
        """Inclui um novo aluno"""
        try:
            nome = self.nome_entry.get().strip()
            matricula = self.matricula_entry.get().strip()

            if not nome or not matricula:
                raise ValidationError("Preencha todos os campos!")

            self.aluno_service.criar(nome=nome, matricula=matricula)
            self.refresh_table()
            self.limpar_campos()
            logger.info(f"Aluno incluído: {nome} - {matricula}")
            messagebox.showinfo("Sucesso", "Aluno incluído com sucesso!")

        except ValidationError as e:
            logger.warning(f"Erro de validação: {e}")
            messagebox.showerror("Erro de Validação", str(e))
        except DatabaseConnectionError as e:
            logger.error(f"Erro de conexão: {e}")
            messagebox.showerror("Erro de Conexão", "Erro ao conectar com o banco de dados")
        except Exception as e:
            logger.error(f"Erro ao incluir aluno: {e}")
            error_msg = str(e)

            if "já existe" in error_msg:
                messagebox.showerror("Erro", "Este aluno já existe!")
            else:
                messagebox.showerror("Erro", "Erro inesperado. Entre em contato com o Suporte")

    def alterar_aluno(self):
        """Altera o aluno selecionado"""
        try:
            if not self.selected_aluno:
                raise SelectionError("Selecione um aluno na tabela!")

            nome = self.nome_entry.get().strip()
            matricula = self.matricula_entry.get().strip()

            if not nome or not matricula:
                raise ValidationError("Preencha todos os campos!")

            self.aluno_service.atualizar(
                id=int(self.selected_aluno), nome=nome, matricula=matricula
            )
            self.refresh_table()
            self.limpar_campos()
            logger.info(f"Aluno alterado ID {self.selected_aluno}: {nome} - {matricula}")
            messagebox.showinfo("Sucesso", "Aluno alterado com sucesso!")

        except SelectionError as e:
            logger.warning(f"Erro de seleção: {e}")
            messagebox.showerror("Erro de Seleção", str(e))
        except ValidationError as e:
            logger.warning(f"Erro de validação: {e}")
            messagebox.showerror("Erro de Validação", str(e))
        except DataNotFoundError as e:
            logger.warning(f"Dados não encontrados: {e}")
            messagebox.showerror("Erro", "Aluno não encontrado!")
        except DatabaseConnectionError as e:
            logger.error(f"Erro de conexão: {e}")
            messagebox.showerror("Erro de Conexão", "Erro ao conectar com o banco de dados")
        except Exception as e:
            logger.error(f"Erro ao alterar aluno: {e}")
            error_msg = str(e)

            if "já existe" in error_msg:
                messagebox.showerror("Erro", "Este aluno já existe!")
            elif "não encontrado" in error_msg:
                messagebox.showerror("Erro", "Aluno não encontrado!")
            else:
                messagebox.showerror("Erro", "Erro inesperado. Entre em contato com o Suporte")

    def excluir_aluno(self):
        """Exclui o aluno selecionado"""
        if not self.selected_aluno:
            messagebox.showerror("Erro", "Selecione um aluno na tabela!")
            return

        nome = self.nome_entry.get().strip()

        if messagebox.askyesno(
            "Confirmar Exclusão", f"Tem certeza que deseja excluir o aluno:\n{nome}?"
        ):
            try:
                self.aluno_service.deletar(int(self.selected_aluno))
                self.refresh_table()
                self.limpar_campos()
                logger.info(f"Aluno excluído ID {self.selected_aluno}: {nome}")

            except Exception as e:
                logger.error(f"Erro ao excluir aluno: {e}")
                messagebox.showerror("Erro", "Erro ao salvar, entre em contato com o Suporte")

    def limpar_campos(self):
        """Limpa os campos do formulário"""
        self.nome_entry.delete(0, tk.END)
        self.matricula_entry.delete(0, tk.END)
        self.selected_aluno = None

        # Limpar seleção da tabela
        self.tree.selection_remove(self.tree.selection())
