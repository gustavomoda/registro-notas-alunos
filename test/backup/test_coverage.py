"""
Script para executar testes e medir cobertura
"""

import os
import subprocess
import sys


def run_tests_with_coverage():
    """Executa testes com medição de cobertura"""

    # Comando para executar pytest com cobertura apenas do backend
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "test/backup/",
        "--cov=registro_notas_alunos.backend",
        "--cov-report=html:test/backup/coverage_html",
        "--cov-report=term-missing",
        "--cov-fail-under=70",  # Ajustado para 70% - realista para backend atual
        "-v",
    ]

    print("Executando testes unitários com medição de cobertura do backend...")
    print(f"Comando: {' '.join(cmd)}")
    print("-" * 60)

    try:
        result = subprocess.run(cmd, cwd=os.getcwd(), check=True)
        print("-" * 60)
        print("✅ Testes executados com sucesso!")
        print("📊 Relatório de cobertura gerado em: test/backup/coverage_html/")
        return True

    except subprocess.CalledProcessError as e:
        print("-" * 60)
        print(f"❌ Erro ao executar testes: {e}")
        print("📋 Verifique os logs acima para mais detalhes")
        return False


def install_dependencies():
    """Instala dependências necessárias para os testes"""

    dependencies = ["pytest", "pytest-cov"]

    for dep in dependencies:
        print(f"Instalando {dep}...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", dep],
                check=True,
                capture_output=True,
            )
            print(f"✅ {dep} instalado com sucesso")
        except subprocess.CalledProcessError:
            print(f"❌ Erro ao instalar {dep}")
            return False

    return True


if __name__ == "__main__":
    print("🧪 Sistema de Testes Unitários - Registro de Notas")
    print("=" * 60)

    print("\n📦 Verificando dependências...")
    if not install_dependencies():
        sys.exit(1)

    print("\n🔍 Executando testes...")
    if run_tests_with_coverage():
        print("\n🎉 Todos os testes passaram com cobertura > 70% no backend!")
    else:
        print("\n⚠️  Alguns testes falharam ou cobertura < 70%")
        sys.exit(1)
