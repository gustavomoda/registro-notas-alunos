import logging
import tkinter as tk
from tkinter import messagebox, ttk

from ...backend import AlunoService, MatriculaService, NotasService
from ...backend.lib.database import DatabaseConnection
from ...backend.notas.model import Notas
from ...backend.notas.service import NotasJaExistemException

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
        self.load_alunos()
        self.refresh_table()

        # Configurar estado inicial dos botões após criar toda a interface
        self.update_button_states()

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
        title_label = ttk.Label(main_frame, text="Gerenciar Notas", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))

        # Frame formulário
        form_frame = ttk.LabelFrame(main_frame, text="Dados das Notas", padding="10")
        form_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 15))

        # Linha 1 - Seleção de Aluno, Semestre e Disciplina
        ttk.Label(form_frame, text="Aluno:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.aluno_combo = ttk.Combobox(form_frame, width=25, state="readonly")
        self.aluno_combo.grid(row=0, column=1, pady=5, padx=(10, 20))
        self.aluno_combo.bind("<<ComboboxSelected>>", self.on_aluno_selected)

        ttk.Label(form_frame, text="Semestre:").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.semestre_combo = ttk.Combobox(form_frame, width=15, state="disabled")
        self.semestre_combo.grid(row=0, column=3, pady=5, padx=(10, 20))
        self.semestre_combo.bind("<<ComboboxSelected>>", self.on_semestre_selected)

        ttk.Label(form_frame, text="Disciplina:").grid(row=0, column=4, sticky=tk.W, pady=5)
        self.disciplina_combo = ttk.Combobox(form_frame, width=25, state="disabled")
        self.disciplina_combo.grid(row=0, column=5, pady=5, padx=(10, 0))
        self.disciplina_combo.bind("<<ComboboxSelected>>", self.on_disciplina_selected)

        # Notas - Linha 2
        ttk.Label(form_frame, text="SM1:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.sm1_entry = ttk.Entry(form_frame, width=10, state="disabled")
        self.sm1_entry.grid(row=1, column=1, pady=5, padx=(10, 20))

        ttk.Label(form_frame, text="SM2:").grid(row=1, column=2, sticky=tk.W, pady=5)
        self.sm2_entry = ttk.Entry(form_frame, width=10, state="disabled")
        self.sm2_entry.grid(row=1, column=3, pady=5, padx=(10, 20))

        ttk.Label(form_frame, text="AV:").grid(row=1, column=4, sticky=tk.W, pady=5)
        self.av_entry = ttk.Entry(form_frame, width=10, state="disabled")
        self.av_entry.grid(row=1, column=5, pady=5, padx=(10, 0))

        # Notas - Linha 3
        ttk.Label(form_frame, text="AVS:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.avs_entry = ttk.Entry(form_frame, width=10, state="disabled")
        self.avs_entry.grid(row=2, column=1, pady=5, padx=(10, 20))

        # Nota Final (calculada)
        ttk.Label(form_frame, text="NF (calculado):").grid(row=2, column=2, sticky=tk.W, pady=5)
        self.nf_label = ttk.Label(
            form_frame, text="--", font=("Arial", 10, "bold"), foreground="blue"
        )
        self.nf_label.grid(row=2, column=3, pady=5, padx=(10, 0), sticky=tk.W)

        # Situação
        ttk.Label(form_frame, text="Situação:").grid(row=2, column=4, sticky=tk.W, pady=5)
        self.situacao_label = ttk.Label(form_frame, text="--", font=("Arial", 10, "bold"))
        self.situacao_label.grid(row=2, column=5, pady=5, padx=(10, 0), sticky=tk.W)

        # Botões
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=6, pady=15)

        # Criar botões e armazenar referências
        self.btn_incluir = ttk.Button(button_frame, text="Incluir", command=self.incluir_nota)
        self.btn_incluir.grid(row=0, column=0, padx=5)

        self.btn_alterar = ttk.Button(button_frame, text="Alterar", command=self.alterar_nota)
        self.btn_alterar.grid(row=0, column=1, padx=5)

        self.btn_excluir = ttk.Button(button_frame, text="Excluir", command=self.excluir_nota)
        self.btn_excluir.grid(row=0, column=2, padx=5)

        ttk.Button(button_frame, text="Calcular", command=self.calcular_preview).grid(
            row=0, column=3, padx=5
        )
        ttk.Button(button_frame, text="Atualizar", command=self.refresh_table).grid(
            row=0, column=4, padx=5
        )
        ttk.Button(button_frame, text="Limpar", command=self.limpar_campos).grid(
            row=0, column=5, padx=5
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
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

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
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
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

    def load_alunos(self):
        """Carrega apenas os alunos no primeiro combo"""
        try:
            aluno_service = AlunoService(self.db)

            alunos = aluno_service.listar_todos()
            self.alunos_dict = {aluno.nome: aluno.id for aluno in alunos}
            self.aluno_combo["values"] = list(self.alunos_dict.keys())

        except Exception as e:
            logger.error(f"Erro ao carregar alunos: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar alunos:\n{str(e)}")

    def on_aluno_selected(self, event):
        """Carrega semestres disponíveis para o aluno selecionado"""
        try:
            aluno_nome = self.aluno_combo.get()
            if not aluno_nome:
                return

            id_aluno = self.alunos_dict.get(aluno_nome)
            if not id_aluno:
                return

            # Limpar campos dependentes primeiro
            self.semestre_combo.set("")
            self.semestre_combo["state"] = "disabled"
            self.disciplina_combo.set("")
            self.disciplina_combo["state"] = "disabled"
            self.disable_note_fields()

            # Limpar matrícula atual se existir
            if hasattr(self, "current_id_matricula"):
                delattr(self, "current_id_matricula")

            # Buscar semestres onde o aluno tem matrícula
            matriculas_aluno = self.matricula_service.listar_por_aluno(id_aluno)

            # Extrair semestres únicos (ano/semestre)
            semestres = set()
            self.semestres_matriculas = {}  # Para mapear semestre -> lista de matrículas

            for matricula in matriculas_aluno:
                id_matricula, nome_disciplina, ano, semestre = matricula
                semestre_key = f"{ano}/{semestre}"
                semestres.add(semestre_key)

                if semestre_key not in self.semestres_matriculas:
                    self.semestres_matriculas[semestre_key] = []
                self.semestres_matriculas[semestre_key].append(matricula)

            # Habilitar e carregar combo de semestre
            if semestres:
                semestres_list = sorted(list(semestres))
                self.semestre_combo["values"] = semestres_list
                self.semestre_combo["state"] = "readonly"

            # Atualizar estado dos botões
            self.update_button_states()

        except Exception as e:
            logger.error(f"Erro ao carregar semestres: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar semestres:\n{str(e)}")

    def on_semestre_selected(self, event):
        """Carrega disciplinas disponíveis para o semestre selecionado"""
        try:
            semestre_sel = self.semestre_combo.get()
            if not semestre_sel:
                return

            # Limpar campos dependentes primeiro
            self.disciplina_combo.set("")
            self.disciplina_combo["state"] = "disabled"
            self.disable_note_fields()

            # Limpar matrícula atual se existir
            if hasattr(self, "current_id_matricula"):
                delattr(self, "current_id_matricula")

            # Buscar matrículas do semestre selecionado
            matriculas_semestre = self.semestres_matriculas.get(semestre_sel, [])

            # Extrair disciplinas
            self.disciplinas_dict = {}
            disciplinas_nomes = []

            for matricula in matriculas_semestre:
                id_matricula, nome_disciplina, ano, semestre = matricula
                self.disciplinas_dict[nome_disciplina] = id_matricula
                disciplinas_nomes.append(nome_disciplina)

            # Habilitar e carregar combo de disciplina
            if disciplinas_nomes:
                self.disciplina_combo["values"] = sorted(disciplinas_nomes)
                self.disciplina_combo["state"] = "readonly"

            # Atualizar estado dos botões
            self.update_button_states()

        except Exception as e:
            logger.error(f"Erro ao carregar disciplinas: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar disciplinas:\n{str(e)}")

    def on_disciplina_selected(self, event):
        """Habilita campos de notas e carrega dados existentes se houver"""
        try:
            disciplina_sel = self.disciplina_combo.get()
            if not disciplina_sel:
                return

            # Obter ID da matrícula
            self.current_id_matricula = self.disciplinas_dict[disciplina_sel]

            # Habilitar campos de notas
            self.enable_note_fields()

            # Verificar se já existem notas para esta matrícula
            notas_existentes = self.notas_service.buscar_por_matricula(self.current_id_matricula)

            if notas_existentes:
                # Preencher campos com notas existentes
                self.sm1_entry.delete(0, tk.END)
                self.sm1_entry.insert(0, self.format_decimal_display(notas_existentes.sm1))

                self.sm2_entry.delete(0, tk.END)
                self.sm2_entry.insert(0, self.format_decimal_display(notas_existentes.sm2))

                self.av_entry.delete(0, tk.END)
                self.av_entry.insert(0, self.format_decimal_display(notas_existentes.av))

                self.avs_entry.delete(0, tk.END)
                self.avs_entry.insert(0, self.format_decimal_display(notas_existentes.avs))

                self.selected_nota = notas_existentes.id
            else:
                # Limpar campos para nova entrada
                self.limpar_campos_notas()
                self.selected_nota = None

            # Calcular preview
            self.calcular_preview()

            # Atualizar estado dos botões
            self.update_button_states()

        except Exception as e:
            logger.error(f"Erro ao carregar dados da disciplina: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar dados da disciplina:\n{str(e)}")

    def enable_note_fields(self):
        """Habilita campos de entrada de notas"""
        self.sm1_entry["state"] = "normal"
        self.sm2_entry["state"] = "normal"
        self.av_entry["state"] = "normal"
        self.avs_entry["state"] = "normal"

    def disable_note_fields(self):
        """Desabilita campos de entrada de notas"""
        self.sm1_entry["state"] = "disabled"
        self.sm2_entry["state"] = "disabled"
        self.av_entry["state"] = "disabled"
        self.avs_entry["state"] = "disabled"
        self.limpar_campos_notas()

    def limpar_campos_notas(self):
        """Limpa apenas os campos de notas"""
        self.sm1_entry.delete(0, tk.END)
        self.sm2_entry.delete(0, tk.END)
        self.av_entry.delete(0, tk.END)
        self.avs_entry.delete(0, tk.END)
        self.nf_label.config(text="--")
        self.situacao_label.config(text="--", foreground="black")

    def refresh_table(self):
        """Atualiza a tabela"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            notas_apuradas = self.notas_service.listar_com_detalhes()

            for nota_vo in notas_apuradas:
                # Formatear a situação com símbolos para destacar visualmente
                situacao_display = nota_vo.situacao
                if nota_vo.situacao == "APROVADO":
                    situacao_display = "✓ APROVADO"
                elif nota_vo.situacao == "REPROVADO":
                    situacao_display = "✗ REPROVADO"
                elif nota_vo.situacao == "PENDENTE":
                    situacao_display = "⏳ PENDENTE"

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
                        situacao_display,
                    ),
                )

            logger.info(f"Tabela notas atualizada - {len(notas_apuradas)} registros")

        except Exception as e:
            logger.error(f"Erro ao atualizar tabela notas: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar notas:\n{str(e)}")

    def validar_notas(self, sm1, sm2, av, avs, mostrar_mensagem=True):
        """
        Valida os valores das notas conforme regras de negócio

        Args:
            sm1: Nota SM1
            sm2: Nota SM2
            av: Nota AV
            avs: Nota AVS
            mostrar_mensagem: Se deve mostrar messagebox em caso de erro

        Returns:
            bool: True se válido, False caso contrário
        """
        try:
            # Verificar se valores são números válidos
            if sm1 is not None and (sm1 < 0 or sm1 > 1):
                if mostrar_mensagem:
                    valor_formatado = self.format_decimal_display(sm1)
                    messagebox.showerror("Erro", f"SM1 = {valor_formatado} deve ser ≤ 1,00!")
                return False

            if sm2 is not None and (sm2 < 0 or sm2 > 1):
                if mostrar_mensagem:
                    valor_formatado = self.format_decimal_display(sm2)
                    messagebox.showerror("Erro", f"SM2 = {valor_formatado} deve ser ≤ 1,00!")
                return False

            if av is not None and (av < 0 or av > 10):
                if mostrar_mensagem:
                    valor_formatado = self.format_decimal_display(av)
                    messagebox.showerror("Erro", f"AV = {valor_formatado} deve ser ≤ 10,00!")
                return False

            if avs is not None and (avs < 0 or avs > 10):
                if mostrar_mensagem:
                    valor_formatado = self.format_decimal_display(avs)
                    messagebox.showerror("Erro", f"AVS = {valor_formatado} deve ser ≤ 10,00!")
                return False

            return True

        except Exception as e:
            if mostrar_mensagem:
                messagebox.showerror("Erro", f"Valores inválidos digitados! {str(e)}")
            return False

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

            # Validar valores - sem mostrar mensagem no preview para não incomodar
            if not self.validar_notas(sm1, sm2, av, avs, mostrar_mensagem=False):
                self.nf_label.config(text="--", foreground="red")
                self.situacao_label.config(text="INVÁLIDO", foreground="red")
                return

            # Usa o service para calcular
            nf, situacao = self.notas_service.calcular_nota_final_e_situacao(sm1, sm2, av, avs)

            if situacao == "PENDENTE":
                self.nf_label.config(text="--", foreground="gray")
                self.situacao_label.config(text="PENDENTE", foreground="orange")
            else:
                # NF em CYAN escuro com formatação brasileira
                self.nf_label.config(text=self.format_decimal_display(nf), foreground="#008B8B")

                if situacao == "APROVADO":
                    self.situacao_label.config(text=situacao, foreground="green")
                else:
                    self.situacao_label.config(text=situacao, foreground="red")

        except Exception as e:
            logger.error(f"Erro ao calcular preview: {e}")
            self.nf_label.config(text="--", foreground="gray")
            self.situacao_label.config(text="--", foreground="gray")

    def on_select(self, event):
        """Evento seleção da tabela - carrega dados nos combos"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item["values"]

            # Nova estrutura: (id_nota, nome_aluno, nome_disciplina, ano_semestre,
            #                 sm1, sm2, av, avs, nf, situacao)
            nome_aluno = values[1]
            nome_disciplina = values[2]
            ano_semestre = values[3]  # formato "2024/1"

            # Selecionar aluno
            self.aluno_combo.set(nome_aluno)
            self.on_aluno_selected(None)  # Carregar semestres

            # Selecionar semestre
            self.semestre_combo.set(ano_semestre)
            self.on_semestre_selected(None)  # Carregar disciplinas

            # Selecionar disciplina
            self.disciplina_combo.set(nome_disciplina)
            self.on_disciplina_selected(None)  # Carregar notas

            # O ID da nota já foi definido no on_disciplina_selected
            self.selected_nota = values[0]  # id_nota

            # Atualizar estado dos botões
            self.update_button_states()

    def incluir_nota(self):
        """Inclui nova nota"""
        if not hasattr(self, "current_id_matricula") or not self.current_id_matricula:
            messagebox.showerror("Erro", "Selecione aluno, semestre e disciplina!")
            return

        try:
            # Limpar seleção para garantir que é uma inclusão nova
            self.selected_nota = None
            self.tree.selection_remove(self.tree.selection())

            sm1 = self.convert_decimal_input(self.sm1_entry.get() or "0")
            sm2 = self.convert_decimal_input(self.sm2_entry.get() or "0")
            av = self.convert_decimal_input(self.av_entry.get() or "0")
            avs = self.convert_decimal_input(self.avs_entry.get() or "0")

            # Validar notas antes de salvar
            if not self.validar_notas(sm1, sm2, av, avs):
                return

            notas = Notas(
                id=None, id_matricula=self.current_id_matricula, sm1=sm1, sm2=sm2, av=av, avs=avs
            )
            self.notas_service.criar(notas)
            self.refresh_table()
            self.limpar_campos_notas()

            # Atualizar estado dos botões
            self.update_button_states()

            logger.info(f"Nota incluída para matrícula {self.current_id_matricula}")

        except NotasJaExistemException as e:
            logger.info(f"Tentativa de incluir nota duplicada: {e}")
            messagebox.showinfo("Informação", "Nota já existe para esta matrícula!")
        except Exception as e:
            logger.error(f"Erro ao incluir nota: {e}")
            messagebox.showerror("Erro", "Erro ao salvar, entre em contato com o Suporte")

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

            # Validar notas antes de salvar
            if not self.validar_notas(sm1, sm2, av, avs):
                return

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
            self.limpar_campos_notas()

            # Atualizar estado dos botões
            self.update_button_states()

            logger.info(f"Nota alterada ID {self.selected_nota}")

        except Exception as e:
            logger.error(f"Erro ao alterar nota: {e}")
            error_msg = str(e)

            if "não encontrada" in error_msg:
                messagebox.showerror("Erro", "Nota não encontrada!")
            else:
                messagebox.showerror("Erro", "Erro ao salvar, entre em contato com o Suporte")

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

                # Atualizar estado dos botões
                self.update_button_states()

                logger.info(f"Nota excluída ID {self.selected_nota}")

            except Exception as e:
                logger.error(f"Erro ao excluir nota: {e}")
                messagebox.showerror("Erro", "Erro ao salvar, entre em contato com o Suporte")

    def limpar_campos(self):
        """Limpa todos os campos"""
        self.aluno_combo.set("")
        self.semestre_combo.set("")
        self.semestre_combo["state"] = "disabled"
        self.disciplina_combo.set("")
        self.disciplina_combo["state"] = "disabled"
        self.disable_note_fields()
        self.selected_nota = None
        if hasattr(self, "current_id_matricula"):
            delattr(self, "current_id_matricula")
        self.tree.selection_remove(self.tree.selection())

        # Atualizar estado dos botões
        self.update_button_states()

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

    def format_decimal_display(self, value) -> str:
        """
        Formata número para exibição brasileira (com vírgula)

        Args:
            value: Valor numérico (pode ser None)

        Returns:
            str: Valor formatado com vírgula ou string vazia se None
        """
        if value is None:
            return ""
        return f"{value:.2f}".replace(".", ",")

    def update_button_states(self):
        """Atualiza o estado dos botões com base na seleção"""
        # Verificar se a interface foi completamente criada
        if not hasattr(self, "tree") or not hasattr(self, "btn_incluir"):
            return

        has_selection = bool(self.tree.selection())
        has_complete_selection = hasattr(self, "current_id_matricula") and self.current_id_matricula

        if has_selection:
            # Modo edição - linha selecionada na tabela
            self.btn_incluir.config(state=tk.DISABLED)
            self.btn_alterar.config(state=tk.NORMAL if has_complete_selection else tk.DISABLED)
            self.btn_excluir.config(state=tk.NORMAL)
        else:
            # Modo inclusão - nenhuma linha selecionada
            self.btn_incluir.config(state=tk.NORMAL if has_complete_selection else tk.DISABLED)
            self.btn_alterar.config(state=tk.DISABLED)
            self.btn_excluir.config(state=tk.DISABLED)
