#!/usr/bin/env python3
"""
Sistema de Registro de Notas de Alunos - Versão Windows
Aplicação principal com correções para Windows
"""

import sys
from pathlib import Path


def setup_imports():
    """Configura os imports para funcionar no Windows"""
    # Adiciona o diretório raiz do projeto ao sys.path
    project_root = Path(__file__).parent.absolute()
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))


def main():
    """Função principal da aplicação"""
    print("🚀 Iniciando Sistema de Registro de Notas (Windows)...")

    # Configura imports
    setup_imports()

    try:
        # Testa importações críticas
        print("📦 Verificando módulos...")

        from registro_notas_alunos.backend.lib.database import DatabaseConnection

        print("✅ DatabaseConnection importado")

        from registro_notas_alunos.gui.main import MainApp

        print("✅ MainApp importado")

        # Inicializa aplicação
        print("🎯 Inicializando aplicação...")
        app = MainApp()
        print("✅ Aplicação inicializada com sucesso!")

        # Executa
        app.run()

    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("\n🔧 SOLUÇÕES:")
        print("1. Execute: python instalar_windows.bat")
        print("2. Ou execute: pip install -r requirements.txt")
        print("3. Verifique se está no diretório correto do projeto")
        input("\nPressione Enter para sair...")
    except Exception as e:
        print(f"❌ Erro ao iniciar aplicação: {e}")
        print("\n🔍 Para diagnóstico completo, execute:")
        print("python windows_fix.py")
        input("\nPressione Enter para sair...")


if __name__ == "__main__":
    main()
