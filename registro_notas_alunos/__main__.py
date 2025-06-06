#!/usr/bin/env python3
"""
Arquivo principal para execução do Sistema de Registro de Notas
"""

from registro_notas_alunos.gui.main import MainApp


def main():
    """Função principal para entrada do script"""
    app = MainApp()
    app.run()


if __name__ == "__main__":
    main()
