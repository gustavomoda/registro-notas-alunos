import tkinter as tk
from tkinter import messagebox, ttk

from ...backend import DisciplinaService, MatriculaService, NotasService
from ...backend.lib.database import DatabaseConnection


class RelatorioDisciplinaScreen:
    def __init__(self, parent):
        self.parent = parent
        self.db = DatabaseConnection()
        self.disciplina_service = DisciplinaService(self.db)
        self.matricula_service = MatriculaService(self.db)
        self.notas_service = NotasService(self.db)
        self.create_window()

    def create_window(self):
        """Cria a janela de relatório por disciplina"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Relatório de Notas por Disciplina")
        self.window.geometry("800x600")
        self.window.resizable(True, True)

        # Centralizar janela
        self.center_window()

        # Criar widgets
        self.create_widgets()

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
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Título
        title_label = ttk.Label(
            main_frame,
            text="Relatório de Notas por Disciplina",
            font=("Arial", 14, "bold"),
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))

        # Informação da arquitetura
        info_label = ttk.Label(
            main_frame,
            text="Usando Services Integrados (Package-as-Services)",
            font=("Arial", 9, "italic"),
            foreground="#cc5500",
        )
        info_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))

        # Seleção de Disciplina
        ttk.Label(main_frame, text="Selecione a Disciplina:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.disciplina_combo = ttk.Combobox(main_frame, width=40, state="readonly")
        self.disciplina_combo.grid(row=2, column=1, pady=5, padx=(10, 0))

        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=2, pady=5, padx=10)

        ttk.Button(
            button_frame, text="Carregar Disciplinas", command=self.carregar_disciplinas
        ).grid(row=0, column=0, padx=2)

        ttk.Button(button_frame, text="Gerar Relatório", command=self.gerar_relatorio).grid(
            row=0, column=1, padx=2
        )

        # Frame para desenvolvimento
        dev_frame = ttk.LabelFrame(main_frame, text="Status de Desenvolvimento", padding="10")
        dev_frame.grid(row=3, column=0, columnspan=3, pady=20, sticky="ew")

        dev_label = ttk.Label(
            dev_frame,
            text="Relatório por disciplina em desenvolvimento",
            font=("Arial", 12),
            foreground="orange",
        )
        dev_label.grid(row=0, column=0, pady=5)

        # Descrição da funcionalidade
        desc_label = ttk.Label(
            dev_frame,
            text="Esta funcionalidade será implementada utilizando a nova arquitetura Package-as-Services.",
            font=("Arial", 10),
            justify="center",
            foreground="gray",
        )
        desc_label.grid(row=1, column=0, pady=10)

        # Botão fechar
        ttk.Button(main_frame, text="Fechar", command=self.window.destroy).grid(
            row=4, column=0, columnspan=3, pady=20
        )

        # Configurar redimensionamento da janela
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Carregar disciplinas automaticamente
        self.carregar_disciplinas()

    def carregar_disciplinas(self):
        """Carrega as disciplinas no combobox"""
        try:
            disciplinas = self.disciplina_service.listar_todas()
            self.disciplinas_dict = {
                f"{disc.nome} ({disc.ano}/{disc.semestre})": disc.id for disc in disciplinas
            }
            self.disciplina_combo["values"] = list(self.disciplinas_dict.keys())
            messagebox.showinfo("Sucesso", "Disciplinas carregadas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar disciplinas:\n{str(e)}")

    def gerar_relatorio(self):
        """Gera o relatório da disciplina selecionada"""
        disciplina_selecionada = self.disciplina_combo.get()

        if not disciplina_selecionada:
            messagebox.showerror("Erro de Validação", "Selecione uma disciplina!")
            return

        try:
            id_disciplina = self.disciplinas_dict[disciplina_selecionada]

            # Por enquanto, apenas mostra uma mensagem
            messagebox.showinfo(
                "Relatório em Desenvolvimento",
                f"Relatório para disciplina ID {id_disciplina} será gerado em breve!\n\n"
                f"Disciplina: {disciplina_selecionada}\n\n"
                f"Funcionalidade em implementação usando:\n"
                f"- DisciplinaService\n"
                f"- MatriculaService  \n"
                f"- NotasService",
            )

        except Exception as e:
            messagebox.showerror("Erro do Sistema", f"Erro ao gerar relatório:\n{str(e)}")
