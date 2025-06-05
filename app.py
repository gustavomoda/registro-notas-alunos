#!/usr/bin/env python3
"""
Sistema de Registro de Notas de Alunos
Aplicação principal para execução do sistema
"""

from registro_notas_alunos.gui.main import MainApp


def main():
    """Função principal da aplicação"""
    print("Iniciando Sistema de Registro de Notas...")

    try:
        app = MainApp()
        app.run()
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        input("Pressione Enter para sair...")


if __name__ == "__main__":
    main()
