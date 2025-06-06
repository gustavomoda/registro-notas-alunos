# Sistema de Registro de Notas - Alunos

Sistema completo para registro e controle de notas acadêmicas, implementado com arquitetura **Package-as-Services** seguindo os princípios **SOLID**.

## Índice de Navegação

### Estrutura do Projeto
- [1. Visão Geral da Arquitetura](#visao-geral-da-arquitetura)
- [2. Estrutura de Diretórios](#estrutura-de-diretorios)

### Desenvolvimento
- [4. Configuração do Ambiente](#configuracao-do-ambiente)
- [5. Setup do Banco de Dados](#setup-do-banco-de-dados)
- [6. Executando a Aplicação](#executando-a-aplicacao)

### Funcionalidades
- [7. Sistema de Notas](#sistema-de-notas)
- [8. Interface Gráfica](#interface-grafica)
- [9. Funcionalidades Implementadas](#funcionalidades-implementadas)

### Documentação Técnica
- [10. Tecnologias Utilizadas](#tecnologias-utilizadas)
- [11. Arquitetura e Padrões](#arquitetura-e-padroes)
- [12. Testes](#testes)


## Visão Geral da Arquitetura

Sistema desenvolvido com **arquitetura Package-as-Services**, onde cada domínio é encapsulado em seu próprio pacote com responsabilidades bem definidas:

```
backend/
├── lib/          # Utilitários e configurações compartilhadas
├── aluno/        # Serviços relacionados ao domínio Aluno
├── disciplina/   # Serviços relacionados ao domínio Disciplina
├── matricula/    # Serviços relacionados ao domínio Matrícula
└── notas/        # Serviços relacionados ao domínio Notas
```

**Princípios SOLID Aplicados:**
- **S**ingle Responsibility: Cada service tem uma responsabilidade específica
- **O**pen/Closed: Extensível via interfaces, fechado para modificação
- **L**iskov Substitution: Services implementam contratos bem definidos
- **I**nterface Segregation: Interfaces específicas para cada domínio
- **D**ependency Inversion: Injeção de dependências via DatabaseConnection


## Estrutura de Diretórios

```
registro-notas-alunos/
├── backend/
│   ├── lib/
│   │   ├── __init__.py
│   │   └── database.py          # Configuração do banco
│   ├── aluno/
│   │   ├── __init__.py
│   │   ├── model.py             # Modelo Aluno
│   │   └── service.py           # AlunoService
│   ├── disciplina/
│   │   ├── __init__.py
│   │   ├── model.py             # Modelo Disciplina
│   │   └── service.py           # DisciplinaService
│   ├── matricula/
│   │   ├── __init__.py
│   │   ├── model.py             # Modelo Matricula
│   │   └── service.py           # MatriculaService
│   └── notas/
│       ├── __init__.py
│       ├── model.py             # Modelo Notas
│       └── service.py           # NotasService
├── registro_notas_alunos/
│   └── gui/                     # Interface Gráfica (tkinter)
│       ├── main.py              # Tela principal
│       └── screens/             # Telas específicas
├── docker-compose.yml           # PostgreSQL containerizado
├── pyproject.toml              # Poetry - gerenciamento de dependências
└── app.py                      # Ponto de entrada da aplicação
```


## Configuração do Ambiente

### Pré-requisitos
- Python 3.8+
- Docker e Docker Compose
- Poetry (opcional, mas recomendado)

### Setup com Poetry
```bash
# Instalar dependências
poetry install

# Ativar ambiente virtual
poetry shell
```

### Setup com pip
```bash
# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
```


## Setup do Banco de Dados

### Inicializar PostgreSQL
```bash
# Subir container PostgreSQL
docker-compose up -d

# Verificar se está rodando
docker-compose ps
```

### Configuração da Conexão
O sistema conecta automaticamente em:
- **Host:** localhost
- **Porta:** 5432
- **Database:** registro_notas
- **Usuário:** postgres
- **Senha:** postgres123

### Dados de Exemplo
O banco é inicializado automaticamente com dados de exemplo incluindo:

#### **10 Alunos com Perfis Variados:**
- **Tony Stark** (2025001) - Engenheiro brilhante mas inconsistente
- **Steve Rogers** (2025002) - Líder disciplinado, consistentemente bom
- **Natasha Romanoff** (2025003) - Estratégica, boa em tudo
- **Bruce Banner** (2025004) - Cientista instável, altos e baixos
- **Thor Odinson** (2025005) - Guerreiro nobre, esforçado mas não acadêmico
- **Clint Barton** (2025006) - Precisão sob pressão, irregular
- **Wanda Maximoff** (2025007) - Poder instável, excelente ou regular
- **Peter Parker** (2025008) - Jovem prodígio, bom mas aprendendo
- **Carol Danvers** (2025009) - Líder exemplar, consistentemente excelente
- **Stephen Strange** (2025010) - Perfeccionista, excelente mas crítico

#### **Disciplinas por Período:**
**2025/1 (Atual):**
- RAD em Python
- Álgebra Linear
- POO em Java
- Estrutura Dados em C
- Banco de Dados
- Engenharia de Software

**2025/2:**
- Mesmas disciplinas do semestre anterior

**2024/2 (Histórico):**
- Fundamentos de Programação
- Matemática Discreta
- Lógica de Programação

#### **Notas Randomizadas:**
- **Notas realistas** com variação natural por perfil de aluno
- **Diferentes desempenhos** por disciplina baseados na personalidade
- **Histórico acadêmico** com dados do semestre anterior
- **AVS (Prova Substitutiva)** aplicada estrategicamente
- **Situações variadas:** Aprovado, Reprovado, Pendente

### Reinicializar Dados
```bash
# Parar e remover containers
docker-compose down -v

# Reiniciar com dados limpos
docker-compose up -d
```


## Executando a Aplicação

### Interface Gráfica (tkinter)
```bash
python app.py
```

### Desenvolvimento no VS Code
O projeto inclui configurações otimizadas para VS Code:

#### Settings (.vscode/settings.json)
- Interpreter: `.venv/bin/python`
- Formatação: Black
- Linting: flake8, mypy, bandit
- Testes: pytest

#### Extensões Recomendadas (.vscode/extensions.json)
#### **Python Development:**
  - Python Language Support
  - Python Language Server
  - Black Python Formatter
  - Import Sorter
  - Linter
  - Type Checker
  - Python Debugger

#### **Container & Version Control:**
  - Docker Support
  - Git Supercharged
  - GitHub Pull Requests
  - Git History Viewer

#### **Productivity Tools:**
  - TODO Highlighter
  - TODO Tree View

#### **Visual Enhancements:**
  - Material Icons
  - One Dark Pro Theme
  - Indent Colors
  - CSV Viewer

#### **File Support:**
  - JSON Tools
  - YAML Support


## Sistema de Notas

### Tipos de Avaliação
- **SM1/SM2:** Seminários (0.0 a 1.0)
- **AV:** Avaliação (0.0 a 10.0)
- **AVS:** Avaliação Substitutiva (0.0 a 10.0)

### Cálculo da Nota Final (NF)
```
NF = max(AV, AVS) + SM1 + SM2
```

### Critério de Aprovação
- **Aprovado:** NF >= 6.0
- **Reprovado:** NF < 6.0


## Interface Gráfica

O sistema possui interface completa desenvolvida em **tkinter**:

### Tela Principal
- Menu com todas as funcionalidades
- Informações sobre a arquitetura utilizada

### Telas Específicas
- **Cadastrar Aluno:** Formulário com validação
- **Cadastrar Disciplina:** Campos ano/semestre
- **Matricular Aluno:** Seleção de aluno e disciplina
- **Inserir Notas:** Campos SM1, SM2, AV, AVS
- **Consultar Notas:** Visualização completa com situação
- **Calcular NF:** Recálculo automático (em desenvolvimento)


## Funcionalidades Implementadas

### Core System
- [x] Cadastro de Alunos
- [x] Cadastro de Disciplinas
- [x] Matrícula de Alunos em Disciplinas
- [x] Inserção de Notas (SM1, SM2, AV, AVS)
- [x] Cálculo Automático da Nota Final (NF)
- [x] Consulta de Notas por Aluno
- [x] Verificação de Situação (Aprovado/Reprovado)

### Interface Gráfica
- [x] Tela Principal com Menu
- [x] Formulários de Cadastro
- [x] Telas de Consulta
- [x] Validação de Dados
- [x] Tratamento de Erros

### Arquitetura
- [x] Package-as-Services implementado
- [x] Princípios SOLID aplicados
- [x] Injeção de Dependências
- [x] Separação de Responsabilidades
- [x] Models com Validação (dataclass)


## Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **PostgreSQL** (via Docker)
- **psycopg2-binary** (driver PostgreSQL)

### Frontend
- **tkinter** (interface gráfica nativa)

### Ferramentas de Desenvolvimento
- **Poetry** (gerenciamento de dependências)
- **Docker Compose** (PostgreSQL)
- **Black** (formatação de código)
- **flake8** (linting)
- **mypy** (type checking)
- **pytest** (testes)


## Arquitetura e Padrões

### Package-as-Services
Cada domínio encapsulado em pacote independente:
- **Modelo:** Definição de dados com validação
- **Service:** Regras de negócio e operações CRUD
- **Isolamento:** Baixo acoplamento entre domínios

### Padrões Implementados
- **Repository Pattern:** Acesso a dados via services
- **Dependency Injection:** DatabaseConnection injetada
- **Single Responsibility:** Cada classe com propósito específico
- **Data Validation:** Validação nos models via dataclass

### Vantagens da Arquitetura
- **Manutenibilidade:** Código organizado e fácil de manter
- **Testabilidade:** Services isolados, fáceis de testar
- **Escalabilidade:** Novos domínios facilmente adicionáveis
- **Flexibilidade:** Modificações sem impacto em outros módulos


## Testes

### Estrutura de Testes
Os testes cobrem:
- **Imports:** Verificação de importações
- **Models:** Validação de dados
- **Services:** Instantação e funcionamento
- **Integration:** Fluxo completo de operações

### Executar Testes
```bash
# Com pytest
pytest

# Com coverage
pytest --cov=backend

# Testes específicos
pytest test_new_architecture.py -v
```

# Telas

#### Menu
![image](https://github.com/user-attachments/assets/b2ce1294-8f14-455a-a3eb-01a2cd681f77)

![image](https://github.com/user-attachments/assets/fe326039-629e-4702-aba1-61bbb4bd8ffb)

![image](https://github.com/user-attachments/assets/ab1ae47d-bfd0-4498-84ac-1b028f06a947)

![image](https://github.com/user-attachments/assets/ea00099b-98fe-49f2-89f3-07df7834806f)

![image](https://github.com/user-attachments/assets/820ff765-05b9-4478-a730-188a04bfb7dd)

![image](https://github.com/user-attachments/assets/9224262c-5b80-4192-9b3f-0b52758d3171)









