import logging
import tkinter as tk
from tkinter import messagebox, ttk

from ...backend import MatriculaService, NotasService
from ...backend.lib.database import DatabaseConnection
from ...backend.notas.model import Notas

logger = logging.getLogger(__name__)


class GerenciarNotasScreen:
    def __init__(self, parent):
        self.parent = parent
        self.db = DatabaseConnection()
        self.notas_service = NotasService(self.db)
        self.matricula_service = MatriculaService(self.db)
        self.selected_nota = None
        self.create_window()

    def create_window(self):
        """Cria a janela de gerenciamento de notas"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Gerenciar Notas")
        self.window.geometry("1100x700")
        self.window.resizable(True, True)

        self.center_window()
        self.create_widgets()
        self.load_matriculas()
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
            main_frame, text="Gerenciar Notas", font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))

        # Frame formulário
        form_frame = ttk.LabelFrame(main_frame, text="Dados das Notas", padding="10")
        form_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 15))

        # Matrícula
        ttk.Label(form_frame, text="Matrícula:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.matricula_combo = ttk.Combobox(form_frame, width=45, state="readonly")
        self.matricula_combo.grid(row=0, column=1, columnspan=3, pady=5, padx=(10, 0))

        # Notas - Linha 1
        ttk.Label(form_frame, text="SM1:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.sm1_entry = ttk.Entry(form_frame, width=10)
        self.sm1_entry.grid(row=1, column=1, pady=5, padx=(10, 20))

        ttk.Label(form_frame, text="SM2:").grid(row=1, column=2, sticky=tk.W, pady=5)
        self.sm2_entry = ttk.Entry(form_frame, width=10)
        self.sm2_entry.grid(row=1, column=3, pady=5, padx=(10, 0))

        # Notas - Linha 2
        ttk.Label(form_frame, text="AV:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.av_entry = ttk.Entry(form_frame, width=10)
        self.av_entry.grid(row=2, column=1, pady=5, padx=(10, 20))

        ttk.Label(form_frame, text="AVS:").grid(row=2, column=2, sticky=tk.W, pady=5)
        self.avs_entry = ttk.Entry(form_frame, width=10)
        self.avs_entry.grid(row=2, column=3, pady=5, padx=(10, 0))

        # Nota Final (calculada)
        ttk.Label(form_frame, text="NF (calculado):").grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        self.nf_label = ttk.Label(
            form_frame, text="--", font=("Arial", 10, "bold"), foreground="blue"
        )
        self.nf_label.grid(row=3, column=1, pady=5, padx=(10, 0), sticky=tk.W)

        # Situação
        ttk.Label(form_frame, text="Situação:").grid(
            row=3, column=2, sticky=tk.W, pady=5
        )
        self.situacao_label = ttk.Label(
            form_frame, text="--", font=("Arial", 10, "bold")
        )
        self.situacao_label.grid(row=3, column=3, pady=5, padx=(10, 0), sticky=tk.W)

        # Botões
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=4, pady=15)

        buttons = [
            ("Incluir", self.incluir_nota),
            ("Alterar", self.alterar_nota),
            ("Excluir", self.excluir_nota),
            ("Calcular", self.calcular_preview),
            ("Atualizar", self.refresh_table),
            ("Limpar", self.limpar_campos),
        ]

        for i, (text, command) in enumerate(buttons):
            ttk.Button(button_frame, text=text, command=command).grid(
                row=0, column=i, padx=5
            )

        # Tabela
        table_frame = ttk.LabelFrame(main_frame, text="Lista de Notas", padding="10")
        table_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=(0, 15))

        columns = (
            "ID",
            "Aluno",
            "Disciplina",
            "Ano/Sem",
            "SM1",
            "SM2",
            "AV",
            "AVS",
            "NF",
            "Situação",
        )
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=12
        )

        # Configurar colunas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Aluno", text="Aluno")
        self.tree.heading("Disciplina", text="Disciplina")
        self.tree.heading("Ano/Sem", text="Ano/Sem")
        self.tree.heading("SM1", text="SM1")
        self.tree.heading("SM2", text="SM2")
        self.tree.heading("AV", text="AV")
        self.tree.heading("AVS", text="AVS")
        self.tree.heading("NF", text="NF")
        self.tree.heading("Situação", text="Situação")

        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Aluno", width=140, anchor=tk.W)
        self.tree.column("Disciplina", width=140, anchor=tk.W)
        self.tree.column("Ano/Sem", width=70, anchor=tk.CENTER)
        self.tree.column("SM1", width=60, anchor=tk.CENTER)
        self.tree.column("SM2", width=60, anchor=tk.CENTER)
        self.tree.column("AV", width=60, anchor=tk.CENTER)
        self.tree.column("AVS", width=60, anchor=tk.CENTER)
        self.tree.column("NF", width=60, anchor=tk.CENTER)
        self.tree.column("Situação", width=100, anchor=tk.CENTER)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Bind para cálculo automático
        for entry in [self.sm1_entry, self.sm2_entry, self.av_entry, self.avs_entry]:
            entry.bind("<KeyRelease>", self.calcular_preview)

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

    def load_matriculas(self):
        """Carrega matrículas no combobox"""
        try:
            matriculas = self.matricula_service.listar_todas()
            self.matriculas_dict = {
                f"{mat[1]} - {mat[3]} (Matrícula: {mat[2]})": mat[0]
                for mat in matriculas
            }
            self.matricula_combo["values"] = list(self.matriculas_dict.keys())

        except Exception as e:
            logger.error(f"Erro ao carregar matrículas: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar matrículas:\n{str(e)}")

    def refresh_table(self):
        """Atualiza a tabela"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            notas_apuradas = self.notas_service.listar_com_detalhes()

            for nota_vo in notas_apuradas:
                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        nota_vo.id_nota,  # ID da nota para operações
                        nota_vo.nome_aluno,
                        nota_vo.disciplina.nome,
                        f"{nota_vo.disciplina.ano}/{nota_vo.disciplina.semestre}",
                        nota_vo.get_sm1_display(),
                        nota_vo.get_sm2_display(),
                        nota_vo.get_av_display(),
                        nota_vo.get_avs_display(),
                        nota_vo.get_nota_final_display(),
                        nota_vo.situacao,
                    ),
                )

            logger.info(f"Tabela notas atualizada - {len(notas_apuradas)} registros")

            # Aplicar cores nas linhas
            for child in self.tree.get_children():
                values = self.tree.item(child)["values"]
                situacao = values[9]  # Índice da situação

                if situacao == "APROVADO":
                    self.tree.tag_configure("aprovado", foreground="green")
                    self.tree.item(child, tags=("aprovado",))
                elif situacao == "REPROVADO":
                    self.tree.tag_configure("reprovado", foreground="red")
                    self.tree.item(child, tags=("reprovado",))
                elif situacao == "PENDENTE":
                    self.tree.tag_configure("pendente", foreground="orange")
                    self.tree.item(child, tags=("pendente",))

        except Exception as e:
            logger.error(f"Erro ao atualizar tabela notas: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar notas:\n{str(e)}")

    def calcular_preview(self, event=None):
        """Calcula preview da nota final usando o service"""
        try:
            sm1_str = self.sm1_entry.get().strip()
            sm2_str = self.sm2_entry.get().strip()
            av_str = self.av_entry.get().strip()
            avs_str = self.avs_entry.get().strip()

            # Usa conversão brasileira (aceita vírgula)
            sm1 = self.convert_decimal_input(sm1_str) if sm1_str else None
            sm2 = self.convert_decimal_input(sm2_str) if sm2_str else None
            av = self.convert_decimal_input(av_str) if av_str else None
            avs = self.convert_decimal_input(avs_str) if avs_str else None

            # Usa o service para calcular
            nf, situacao = self.notas_service.calcular_nota_final_e_situacao(
                sm1, sm2, av, avs
            )

            if situacao == "PENDENTE":
                self.nf_label.config(text="--", foreground="gray")
                self.situacao_label.config(text="PENDENTE", foreground="orange")
            else:
                # NF em CYAN escuro com formatação brasileira
                self.nf_label.config(
                    text=self.format_decimal_display(nf), foreground="#008B8B"
                )

                if situacao == "APROVADO":
                    self.situacao_label.config(text=situacao, foreground="green")
                else:
                    self.situacao_label.config(text=situacao, foreground="red")

        except Exception as e:
            logger.error(f"Erro ao calcular preview: {e}")
            self.nf_label.config(text="--", foreground="gray")
            self.situacao_label.config(text="--", foreground="gray")

    def on_select(self, event):
        """Evento seleção"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item["values"]

            # Nova estrutura: (id_nota, nome_aluno, nome_disciplina, ano_semestre,
            #                 sm1, sm2, av, avs, nf, situacao)
            nome_aluno = values[1]
            nome_disciplina = values[2]

            # Encontrar matrícula correspondente
            aluno_disciplina = f"{nome_aluno} - {nome_disciplina}"
            for key, value in self.matriculas_dict.items():
                if aluno_disciplina in key:
                    self.matricula_combo.set(key)
                    break

            # Preencher notas - usar os valores originais com formatação brasileira
            # Ajustar índices devido à nova coluna Ano/Sem
            self.sm1_entry.delete(0, tk.END)
            if values[4]:  # SM1 (era índice 3, agora é 4)
                self.sm1_entry.insert(0, str(values[4]).replace(".", ","))

            self.sm2_entry.delete(0, tk.END)
            if values[5]:  # SM2 (era índice 4, agora é 5)
                self.sm2_entry.insert(0, str(values[5]).replace(".", ","))

            self.av_entry.delete(0, tk.END)
            if values[6]:  # AV (era índice 5, agora é 6)
                self.av_entry.insert(0, str(values[6]).replace(".", ","))

            self.avs_entry.delete(0, tk.END)
            if values[7]:  # AVS (era índice 6, agora é 7)
                self.avs_entry.insert(0, str(values[7]).replace(".", ","))

            # Usar o ID da nota corretamente
            self.selected_nota = values[0]  # id_nota
            self.calcular_preview()

    def incluir_nota(self):
        """Inclui nova nota"""
        matricula_sel = self.matricula_combo.get()

        if not matricula_sel:
            messagebox.showerror("Erro", "Selecione uma matrícula!")
            return

        try:
            id_matricula = self.matriculas_dict[matricula_sel]
            sm1 = self.convert_decimal_input(self.sm1_entry.get() or "0")
            sm2 = self.convert_decimal_input(self.sm2_entry.get() or "0")
            av = self.convert_decimal_input(self.av_entry.get() or "0")
            avs = self.convert_decimal_input(self.avs_entry.get() or "0")

            notas = Notas(
                id=None, id_matricula=id_matricula, sm1=sm1, sm2=sm2, av=av, avs=avs
            )
            self.notas_service.criar(notas)
            self.refresh_table()
            self.limpar_campos()
            logger.info(f"Nota incluída para matrícula {id_matricula}")

        except Exception as e:
            logger.error(f"Erro ao incluir nota: {e}")
            error_msg = str(e)

            if "já existe" in error_msg:
                messagebox.showerror("Erro", "Nota já existe para esta matrícula!")
            else:
                messagebox.showerror(
                    "Erro", "Erro ao salvar, entre em contato com o Suporte"
                )

    def alterar_nota(self):
        """Altera nota selecionada"""
        if not self.selected_nota:
            messagebox.showerror("Erro", "Selecione uma nota na tabela!")
            return

        try:
            sm1 = self.convert_decimal_input(self.sm1_entry.get() or "0")
            sm2 = self.convert_decimal_input(self.sm2_entry.get() or "0")
            av = self.convert_decimal_input(self.av_entry.get() or "0")
            avs = self.convert_decimal_input(self.avs_entry.get() or "0")

            notas = Notas(
                id=int(self.selected_nota),
                id_matricula=0,
                sm1=sm1,
                sm2=sm2,
                av=av,
                avs=avs,
            )
            self.notas_service.atualizar(notas)
            self.refresh_table()
            self.limpar_campos()
            logger.info(f"Nota alterada ID {self.selected_nota}")

        except Exception as e:
            logger.error(f"Erro ao alterar nota: {e}")
            error_msg = str(e)

            if "não encontrada" in error_msg:
                messagebox.showerror("Erro", "Nota não encontrada!")
            else:
                messagebox.showerror(
                    "Erro", "Erro ao salvar, entre em contato com o Suporte"
                )

    def excluir_nota(self):
        """Exclui nota selecionada"""
        if not self.selected_nota:
            messagebox.showerror("Erro", "Selecione uma nota na tabela!")
            return

        if messagebox.askyesno("Confirmar", "Excluir nota selecionada?"):
            try:
                self.notas_service.deletar(int(self.selected_nota))
                self.refresh_table()
                self.limpar_campos()
                logger.info(f"Nota excluída ID {self.selected_nota}")

            except Exception as e:
                logger.error(f"Erro ao excluir nota: {e}")
                messagebox.showerror(
                    "Erro", "Erro ao salvar, entre em contato com o Suporte"
                )

    def limpar_campos(self):
        """Limpa campos"""
        self.matricula_combo.set("")
        self.sm1_entry.delete(0, tk.END)
        self.sm2_entry.delete(0, tk.END)
        self.av_entry.delete(0, tk.END)
        self.avs_entry.delete(0, tk.END)
        self.nf_label.config(text="--")
        self.situacao_label.config(text="--", foreground="black")
        self.selected_nota = None
        self.tree.selection_remove(self.tree.selection())

    def convert_decimal_input(self, value_str: str) -> float:
        """
        Converte entrada decimal brasileira (vírgula) para float

        Args:
            value_str: String com número (pode usar , ou .)

        Returns:
            float: Valor convertido
        """
        if not value_str.strip():
            return 0.0
        # Substitui vírgula por ponto para conversão
        return float(value_str.replace(",", "."))

    def format_decimal_display(self, value: float) -> str:
        """
        Formata número para exibição brasileira (com vírgula)

        Args:
            value: Valor numérico

        Returns:
            str: Valor formatado com vírgula
        """
        return f"{value:.2f}".replace(".", ",")
