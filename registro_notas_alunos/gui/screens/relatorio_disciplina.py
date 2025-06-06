import logging
import tkinter as tk
from tkinter import messagebox, ttk

from registro_notas_alunos.backend import (
    AlunoService,
    DisciplinaService,
    MatriculaService,
    NotasService,
)
from registro_notas_alunos.backend.lib.database import DatabaseConnection

logger = logging.getLogger(__name__)


class RelatorioDisciplinaScreen:
    def __init__(self, parent):
        self.parent = parent
        self.db = DatabaseConnection()
        self.disciplina_service = DisciplinaService(self.db)
        self.matricula_service = MatriculaService(self.db)
        self.notas_service = NotasService(self.db)
        self.aluno_service = AlunoService(self.db)
        self.create_window()

    def create_window(self):
        """Cria a janela de relatório por disciplina"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Relatório de Disciplinas")
        self.window.geometry("1200x700")
        self.window.resizable(True, True)

        self.center_window()
        self.create_widgets()
        self.carregar_filtros()
        self.gerar_relatorio()

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
            main_frame, text="Relatório de Disciplinas", font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))

        # Frame de filtros
        filter_frame = ttk.LabelFrame(main_frame, text="Filtros", padding="10")
        filter_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 15))

        # Ano
        ttk.Label(filter_frame, text="Ano:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ano_combo = ttk.Combobox(filter_frame, width=10, state="readonly")
        self.ano_combo.grid(row=0, column=1, pady=5, padx=(10, 20))

        # Semestre
        ttk.Label(filter_frame, text="Semestre:").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.semestre_combo = ttk.Combobox(filter_frame, width=10, state="readonly")
        self.semestre_combo.grid(row=0, column=3, pady=5, padx=(10, 20))

        # Disciplina específica
        ttk.Label(filter_frame, text="Disciplina:").grid(row=0, column=4, sticky=tk.W, pady=5)
        self.disciplina_combo = ttk.Combobox(filter_frame, width=25, state="readonly")
        self.disciplina_combo.grid(row=0, column=5, pady=5, padx=(10, 20))

        # Aluno
        ttk.Label(filter_frame, text="Aluno:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.aluno_combo = ttk.Combobox(filter_frame, width=25, state="readonly")
        self.aluno_combo.grid(row=1, column=1, columnspan=2, pady=5, padx=(10, 0))

        # Botões
        button_frame = ttk.Frame(filter_frame)
        button_frame.grid(row=2, column=0, columnspan=6, pady=15)

        buttons = [
            ("Gerar Relatório", self.gerar_relatorio),
            ("Limpar Filtros", self.limpar_filtros),
            ("Exportar", self.exportar_dados),
            ("Atualizar", self.carregar_filtros),
        ]

        for i, (text, command) in enumerate(buttons):
            ttk.Button(button_frame, text=text, command=command).grid(row=0, column=i, padx=5)

        # Resumo estatístico
        stats_frame = ttk.LabelFrame(main_frame, text="Resumo Estatístico", padding="10")
        stats_frame.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(0, 15))

        # Labels para estatísticas
        self.total_registros_label = ttk.Label(
            stats_frame, text="Total de Registros: --", font=("Arial", 10, "bold")
        )
        self.total_registros_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 20))

        self.total_disciplinas_label = ttk.Label(
            stats_frame, text="Disciplinas: --", font=("Arial", 10, "bold")
        )
        self.total_disciplinas_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))

        self.total_alunos_label = ttk.Label(
            stats_frame, text="Alunos: --", font=("Arial", 10, "bold")
        )
        self.total_alunos_label.grid(row=0, column=2, sticky=tk.W, padx=(0, 20))

        self.aprovacao_geral_label = ttk.Label(
            stats_frame, text="% Aprovação Geral: --", font=("Arial", 10, "bold")
        )
        self.aprovacao_geral_label.grid(row=0, column=3, sticky=tk.W)

        # Tabela
        table_frame = ttk.LabelFrame(
            main_frame, text="Detalhes por Aluno e Disciplina", padding="10"
        )
        table_frame.grid(row=3, column=0, columnspan=4, sticky="nsew", pady=(0, 15))

        columns = (
            "Aluno",
            "Matrícula",
            "Disciplina",
            "Ano/Sem",
            "SM1",
            "SM2",
            "AV",
            "AVS",
            "NF",
            "Situação",
        )
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        # Configurar colunas
        self.tree.heading("Aluno", text="Aluno")
        self.tree.heading("Matrícula", text="Matrícula")
        self.tree.heading("Disciplina", text="Disciplina")
        self.tree.heading("Ano/Sem", text="Ano/Sem")
        self.tree.heading("SM1", text="SM1")
        self.tree.heading("SM2", text="SM2")
        self.tree.heading("AV", text="AV")
        self.tree.heading("AVS", text="AVS")
        self.tree.heading("NF", text="NF")
        self.tree.heading("Situação", text="Situação")

        self.tree.column("Aluno", width=150, anchor=tk.W)
        self.tree.column("Matrícula", width=100, anchor=tk.CENTER)
        self.tree.column("Disciplina", width=140, anchor=tk.W)
        self.tree.column("Ano/Sem", width=80, anchor=tk.CENTER)
        self.tree.column("SM1", width=60, anchor=tk.CENTER)
        self.tree.column("SM2", width=60, anchor=tk.CENTER)
        self.tree.column("AV", width=60, anchor=tk.CENTER)
        self.tree.column("AVS", width=60, anchor=tk.CENTER)
        self.tree.column("NF", width=70, anchor=tk.CENTER)
        self.tree.column("Situação", width=100, anchor=tk.CENTER)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Botão fechar
        ttk.Button(main_frame, text="Fechar", command=self.window.destroy).grid(
            row=4, column=0, columnspan=4, pady=15
        )

        # Configurar redimensionamento
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

    def carregar_filtros(self):
        """Carrega os dados dos filtros"""
        try:
            # Carregar disciplinas
            disciplinas = self.disciplina_service.listar_todas()

            # Carregar alunos
            alunos = self.aluno_service.listar_todos()

            # Extrair anos e semestres únicos
            anos = sorted(set(disc.ano for disc in disciplinas))
            semestres = sorted(set(disc.semestre for disc in disciplinas))

            # Configurar combos
            self.ano_combo["values"] = ["Todos"] + [str(ano) for ano in anos]
            self.semestre_combo["values"] = ["Todos"] + [str(sem) for sem in semestres]

            # Disciplinas
            self.disciplinas_dict = {f"{disc.nome}": disc.id for disc in disciplinas}
            self.disciplina_combo["values"] = ["Todas"] + list(self.disciplinas_dict.keys())

            # Alunos
            self.alunos_dict = {aluno.nome: aluno.id for aluno in alunos}
            self.aluno_combo["values"] = ["Todos"] + list(self.alunos_dict.keys())

            # Valores padrão
            self.ano_combo.set("Todos")
            self.semestre_combo.set("Todos")
            self.disciplina_combo.set("Todas")
            self.aluno_combo.set("Todos")

        except Exception as e:
            logger.error(f"Erro ao carregar filtros: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar filtros:\n{str(e)}")

    def gerar_relatorio(self):
        """Gera o relatório com base nos filtros"""
        try:
            # Limpar tabela
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Obter filtros
            ano_filtro = self.ano_combo.get()
            semestre_filtro = self.semestre_combo.get()
            disciplina_filtro = self.disciplina_combo.get()
            aluno_filtro = self.aluno_combo.get()

            # Buscar todas as notas com detalhes
            notas_apuradas = self.notas_service.listar_com_detalhes()

            # Aplicar filtros
            registros_filtrados = []
            for nota_vo in notas_apuradas:
                # Filtro de ano
                if ano_filtro != "Todos" and nota_vo.disciplina.ano != int(ano_filtro):
                    continue

                # Filtro de semestre
                if semestre_filtro != "Todos" and nota_vo.disciplina.semestre != int(
                    semestre_filtro
                ):
                    continue

                # Filtro de disciplina
                if disciplina_filtro != "Todas" and nota_vo.disciplina.nome != disciplina_filtro:
                    continue

                # Filtro de aluno
                if aluno_filtro != "Todos" and nota_vo.nome_aluno != aluno_filtro:
                    continue

                registros_filtrados.append(nota_vo)

            # Estatísticas gerais
            total_registros = len(registros_filtrados)
            disciplinas_unicas = set()
            alunos_unicos = set()
            aprovados = 0
            reprovados = 0

            # Processar registros e adicionar à tabela
            for nota_vo in registros_filtrados:
                disciplinas_unicas.add(nota_vo.disciplina.nome)
                alunos_unicos.add(nota_vo.nome_aluno)

                if nota_vo.situacao == "APROVADO":
                    aprovados += 1
                elif nota_vo.situacao == "REPROVADO":
                    reprovados += 1

                # Formatear situação com símbolo
                situacao_display = nota_vo.situacao
                if nota_vo.situacao == "APROVADO":
                    situacao_display = "✓ APROVADO"
                elif nota_vo.situacao == "REPROVADO":
                    situacao_display = "✗ REPROVADO"
                elif nota_vo.situacao == "PENDENTE":
                    situacao_display = "⏳ PENDENTE"

                # Adicionar linha na tabela
                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        nota_vo.nome_aluno,
                        nota_vo.id_nota,  # Usando id_nota como proxy para matrícula
                        nota_vo.disciplina.nome,
                        f"{nota_vo.disciplina.ano}/{nota_vo.disciplina.semestre}",
                        nota_vo.get_sm1_display(),
                        nota_vo.get_sm2_display(),
                        nota_vo.get_av_display(),
                        nota_vo.get_avs_display(),
                        nota_vo.get_nota_final_display(),
                        situacao_display,
                    ),
                )

            # Calcular estatísticas
            total_disciplinas = len(disciplinas_unicas)
            total_alunos = len(alunos_unicos)
            perc_aprovacao = (aprovados / total_registros * 100) if total_registros > 0 else 0

            # Atualizar estatísticas
            self.total_registros_label.config(text=f"Total de Registros: {total_registros}")
            self.total_disciplinas_label.config(text=f"Disciplinas: {total_disciplinas}")
            self.total_alunos_label.config(text=f"Alunos: {total_alunos}")
            self.aprovacao_geral_label.config(text=f"% Aprovação Geral: {perc_aprovacao:.1f}%")

            logger.info(
                f"Relatório gerado - {total_registros} registros, {total_disciplinas} disciplinas, {total_alunos} alunos"
            )

        except Exception as e:
            logger.error(f"Erro ao gerar relatório: {e}")
            messagebox.showerror("Erro", f"Erro ao gerar relatório:\n{str(e)}")

    def limpar_filtros(self):
        """Limpa todos os filtros"""
        self.ano_combo.set("Todos")
        self.semestre_combo.set("Todos")
        self.disciplina_combo.set("Todas")
        self.aluno_combo.set("Todos")
        self.gerar_relatorio()

    def exportar_dados(self):
        """Exporta os dados para um formato legível"""
        try:
            dados = []
            for child in self.tree.get_children():
                values = self.tree.item(child)["values"]
                dados.append(values)

            if not dados:
                messagebox.showwarning("Aviso", "Nenhum dado para exportar!")
                return

            # Por enquanto, apenas mostra resumo
            resumo = "RELATÓRIO DE DISCIPLINAS\n"
            resumo += "=" * 50 + "\n\n"
            resumo += "Filtros aplicados:\n"
            resumo += f"Ano: {self.ano_combo.get()}\n"
            resumo += f"Semestre: {self.semestre_combo.get()}\n"
            resumo += f"Disciplina: {self.disciplina_combo.get()}\n"
            resumo += f"Aluno: {self.aluno_combo.get()}\n\n"

            resumo += "Estatísticas:\n"
            resumo += f"{self.total_registros_label.cget('text')}\n"
            resumo += f"{self.total_disciplinas_label.cget('text')}\n"
            resumo += f"{self.total_alunos_label.cget('text')}\n"
            resumo += f"{self.aprovacao_geral_label.cget('text')}\n\n"

            resumo += f"Total de registros no relatório: {len(dados)}\n"

            messagebox.showinfo("Exportação", resumo)

        except Exception as e:
            logger.error(f"Erro ao exportar dados: {e}")
            messagebox.showerror("Erro", f"Erro ao exportar dados:\n{str(e)}")
