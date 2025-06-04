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


## Próximos Passos

### Melhorias Planejadas
- [ ] Implementar relatórios por disciplina
- [ ] Adicionar backup/restore do banco
- [ ] Criar API REST para integração
- [ ] Implementar autenticação de usuários
- [ ] Adicionar logs de auditoria
- [ ] Criar dashboards com estatísticas

### Refatorações Técnicas
- [ ] Adicionar mais testes unitários
- [ ] Implementar CI/CD pipeline
- [ ] Adicionar documentação API (Swagger)
- [ ] Otimizar queries do banco de dados


## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request


## Licença

Este projeto é desenvolvido para fins educacionais como parte do curso de **Análise e Desenvolvimento de Sistemas**.


**Desenvolvido com arquitetura Package-as-Services seguindo princípios SOLID**
