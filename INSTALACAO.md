# Instruções de Instalação - Sistema de Registro de Notas

## 📦 Pacotes Gerados

Foram gerados dois tipos de pacote para instalação:

1. **Wheel (Recomendado)**: `registro_notas_alunos-0.1.0-py3-none-any.whl`
2. **Source Distribution**: `registro_notas_alunos-0.1.0.tar.gz`

## 🔧 Pré-requisitos

- Python 3.12 ou superior
- Docker e Docker Compose (para PostgreSQL)
- Pip atualizado

## 📋 Instalação em Outro Computador

### Opção 1: Instalação via Wheel (Recomendado)

```bash
# 1. Copiar o arquivo .whl para o computador destino
# 2. Instalar o pacote
pip install registro_notas_alunos-0.1.0-py3-none-any.whl

# 3. Executar o sistema
registro-notas
```

### Opção 2: Instalação via Source

```bash
# 1. Copiar o arquivo .tar.gz para o computador destino
# 2. Instalar o pacote
pip install registro_notas_alunos-0.1.0.tar.gz

# 3. Executar o sistema
registro-notas
```

### Opção 3: Instalação em Ambiente Virtual (Recomendado)

```bash
# 1. Criar ambiente virtual
python -m venv venv-registro-notas

# 2. Ativar ambiente virtual
# Linux/Mac:
source venv-registro-notas/bin/activate
# Windows:
venv-registro-notas\Scripts\activate

# 3. Atualizar pip
pip install --upgrade pip

# 4. Instalar o pacote
pip install registro_notas_alunos-0.1.0-py3-none-any.whl

# 5. Executar o sistema
registro-notas
```

## 🐳 Configuração do Banco de Dados

### 1. Copiar arquivo Docker Compose

Copie o arquivo `docker-compose.yml` para o computador destino:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    container_name: registro_notas_db
    environment:
      POSTGRES_DB: registro_notas
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./registro_notas_alunos/sql:/docker-entrypoint-initdb.d

volumes:
  postgres_data:
```

### 2. Inicializar PostgreSQL

```bash
# Subir container PostgreSQL
docker-compose up -d

# Verificar se está rodando
docker-compose ps
```

## 🚀 Execução

### Via Script de Entrada
```bash
registro-notas
```

### Via Módulo Python
```bash
python -m registro_notas_alunos
```

## 🔍 Verificação da Instalação

```bash
# Verificar se o pacote foi instalado
pip list | grep registro-notas

# Verificar se o comando está disponível
registro-notas --help
```

## ❌ Desinstalação

```bash
# Desinstalar o pacote
pip uninstall registro-notas-alunos

# Remover banco de dados (opcional)
docker-compose down -v
```

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError"
- Verifique se todas as dependências foram instaladas
- Reinstale o pacote: `pip install --force-reinstall registro_notas_alunos-0.1.0-py3-none-any.whl`

### Erro: "Connection refused" (Banco)
- Verifique se Docker está rodando: `docker ps`
- Reinicie o container: `docker-compose restart`

### Erro: "Command not found"
- Verifique se o PATH inclui os scripts do Python
- Use: `python -m registro_notas_alunos`

## 📝 Logs e Configuração

O sistema criará automaticamente:
- Arquivo de log: `sistema_notas.log`
- Conexão padrão: `localhost:5432`

## 🔄 Atualizações

Para instalar uma nova versão:

```bash
# Desinstalar versão antiga
pip uninstall registro-notas-alunos

# Instalar nova versão
pip install nova_versao.whl
```

## 📞 Suporte

Em caso de problemas, verifique:
1. Versão do Python compatível (3.12+)
2. Dependências instaladas corretamente
3. PostgreSQL rodando e acessível
4. Logs do sistema para detalhes de erro
