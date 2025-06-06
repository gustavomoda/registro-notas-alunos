#!/usr/bin/env python3
"""
Script para atualizar requirements.txt baseado no Poetry
"""

import subprocess
import sys
from datetime import datetime


def run_command(cmd):
    """Executa comando e retorna output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Erro ao executar: {cmd}")
            print(f"Erro: {result.stderr}")
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"Erro: {e}")
        return None


def get_main_dependencies():
    """Pega dependências principais do Poetry"""
    cmd = "poetry show --only=main"
    output = run_command(cmd)
    if not output:
        return []

    deps = []
    for line in output.split("\n"):
        if line.strip():
            parts = line.split()
            if len(parts) >= 2:
                name = parts[0]
                version = parts[1]
                deps.append(f"{name}=={version}")
    return deps


def get_dev_dependencies():
    """Pega dependências de desenvolvimento instaladas"""
    main_deps = get_main_dependencies()
    main_names = [dep.split("==")[0] for dep in main_deps]

    # Lista completa de pacotes instalados
    cmd = "pip freeze"
    output = run_command(cmd)
    if not output:
        return []

    dev_deps = []
    skip_packages = ["registro-notas-alunos"]  # Pular o próprio projeto

    for line in output.split("\n"):
        if line.strip() and "==" in line:
            package_name = line.split("==")[0]
            # Incluir apenas dependências relevantes para desenvolvimento
            if (
                package_name not in main_names
                and package_name not in skip_packages
                and any(
                    keyword in package_name.lower()
                    for keyword in [
                        "test",
                        "pytest",
                        "black",
                        "flake",
                        "mypy",
                        "click",
                        "pathspec",
                        "platform",
                        "packaging",
                        "mccabe",
                        "pycode",
                        "pyflakes",
                        "pluggy",
                        "iniconfig",
                        "colorama",
                    ]
                )
            ):
                dev_deps.append(line.strip())

    return sorted(dev_deps)


def update_requirements_txt():
    """Atualiza o arquivo requirements.txt"""
    print("🔄 Atualizando requirements.txt...")

    # Pegar dependências
    main_deps = get_main_dependencies()
    dev_deps = get_dev_dependencies()

    if not main_deps:
        print("❌ Erro ao obter dependências principais")
        return False

    # Gerar conteúdo
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"""# ===========================================
# REQUIREMENTS.TXT - Gerado via Poetry
# Atualizado em: {timestamp}
# ===========================================

# Dependências principais
"""

    for dep in sorted(main_deps):
        content += f"{dep}\n"

    if dev_deps:
        content += f"\n# Dependências de desenvolvimento\n"
        for dep in dev_deps:
            content += f"{dep}\n"

    content += """
# Nota: Para desenvolvimento use 'poetry install'
# Para produção use apenas as dependências principais
"""

    # Escrever arquivo
    try:
        with open("requirements.txt", "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ requirements.txt atualizado com sucesso!")

        # Mostrar resumo
        print(f"\n📋 RESUMO:")
        print(f"   • Dependências principais: {len(main_deps)}")
        print(f"   • Dependências de desenvolvimento: {len(dev_deps)}")
        print(f"   • Total: {len(main_deps) + len(dev_deps)} pacotes")

        return True

    except Exception as e:
        print(f"❌ Erro ao escrever arquivo: {e}")
        return False


def main():
    """Função principal"""
    print("=" * 60)
    print("🔧 ATUALIZADOR DE REQUIREMENTS.TXT")
    print("=" * 60)

    # Verificar se está em ambiente Poetry
    if not run_command("poetry --version"):
        print("❌ Poetry não encontrado. Instale Poetry primeiro.")
        sys.exit(1)

    # Atualizar requirements.txt
    success = update_requirements_txt()

    print("\n" + "=" * 60)
    if success:
        print("🎉 Atualização concluída!")
        print("💡 Dica: Execute 'pip install -r requirements.txt' para instalar")
    else:
        print("❌ Falha na atualização")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()
