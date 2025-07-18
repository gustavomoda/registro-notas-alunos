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

### Telas do Sistema
- [10. Menu Principal](#menu-principal)
- [11. Cadastro de Alunos](#cadastro-de-alunos)
- [12. Cadastro de Disciplinas](#cadastro-de-disciplinas)
- [13. Matricular Alunos](#matricular-alunos)
- [14. Sistema de Notas Avançado](#sistema-de-notas-avancado)
- [15. Consulta de Notas Inteligente](#consulta-de-notas-inteligente)

### Documentação Técnica
- [16. Tecnologias Utilizadas](#tecnologias-utilizadas)
- [17. Arquitetura e Padrões](#arquitetura-e-padroes)
- [18. Testes](#testes)


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
# Via arquivo principal
python app.py

# Via Poetry (recomendado)
poetry run start
# ou se ambiente virtual ativo:
start

# Via módulo
python -m registro_notas_alunos

# Via script instalado
registro-notas
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
  - Python DebuggerX-

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

# Telas do Sistema

## Menu Principal

- Interface limpa e intuitiva com botões organizados
- Menu principal com acesso a todas as funcionalidades do sistema
- Design moderno seguindo padrões de UX brasileiros

![image](https://github.com/user-attachments/assets/b2ce1294-8f14-455a-a3eb-01a2cd681f77)


## Cadastro de Alunos
- Validação completa de dados de entrada
- Tratamento de erros padronizado ("Erro ao salvar, entre em contato com o Suporte")
- Prevenção contra duplicatas com mensagem informativa
- Interface responsiva com campos obrigatórios claramente identificados

![image](https://github.com/user-attachments/assets/fe326039-629e-4702-aba1-61bbb4bd8ffb)


## Cadastro de Disciplinas
- Formulário com validação de ano/semestre no formato brasileiro (2024/1, 2024/2)
- Controle de duplicatas por período acadêmico
- Mensagens de erro consistentes em todo o sistema
- Integração completa com a arquitetura Package-as-Services
![image](https://github.com/user-attachments/assets/ab1ae47d-bfd0-4498-84ac-1b028f06a947)


### Matricular Alunos
- Seleção dinâmica de alunos e disciplinas disponíveis
- Validação contra matrículas duplicadas com `MatriculaJaExisteException`
- Mensagem informativa em azul para duplicatas (não erro crítico)
- Atualização automática das listas após operações
![image](https://github.com/user-attachments/assets/ea00099b-98fe-49f2-89f3-07df7834806f)


### Sistema de Notas Avançado
- **Nova fórmula brasileira:** `NF = SM1 + SM2 + max(AV, AVS)`
- **Validação de limites:** SM1/SM2 ≤ 1,0 | AV/AVS ≤ 10,0
- **Localização brasileira:** Entrada e exibição com vírgula (3,20)
- **Cores inteligentes:** Verde (aprovado), vermelho (reprovado), laranja (pendente)
- Value Object `AlunoNotaApuradoVO` com lógica de negócio encapsulada
![image](https://github.com/user-attachments/assets/820ff765-05b9-4478-a730-188a04bfb7dd)


### Consulta de Notas Inteligente
- **Tabela completa** com informações da disciplina (ano/semestre)
- **Situação colorida:** Aprovado, Reprovado, Pendente (visual imediato)
- **Formatação brasileira:** Todas as notas exibidas com vírgula
- **Cálculo inteligente:** NF calculada automaticamente com nova fórmula
- **Detalhamento completo:** SM1, SM2, AV, AVS, NF e situação em uma única view
![image](https://github.com/user-attachments/assets/9224262c-5b80-4192-9b3f-0b52758d3171)


### Autores
- Luis Gustavo Moda <gustavo.moda@gmail.com>
- Ganriel Baptista <gabrielbaptistams@gmail.com>
- João Pedro Borges
