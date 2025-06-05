# 🧪 Testes Unitários - Sistema de Registro de Notas

## 📋 Visão Geral

Este diretório contém uma suíte completa de testes unitários para o Sistema de Registro de Notas, com foco em **cobertura superior a 90%** dos componentes críticos do backend.

## 🏗️ Arquitetura de Testes

### 📁 Estrutura de Arquivos

```
test/backup/
├── __init__.py                 # Inicialização do pacote de testes
├── conftest.py                 # Configurações globais e fixtures
├── test_models.py              # Testes para todos os models (28 testes)
├── test_aluno_service.py       # Testes para AlunoService (20 testes)
├── test_disciplina_service.py  # Testes para DisciplinaService (18 testes)
├── test_matricula_service.py   # Testes para MatriculaService (20 testes)
├── test_coverage.py            # Script para executar testes
└── README.md                   # Esta documentação
```

## 🎯 Cobertura de Testes

### ✅ Componentes 100% Testados

- **Models (28 testes)**:
  - `Aluno`: 7 testes - validações, criação, normalização
  - `Disciplina`: 7 testes - validações de ano/semestre, nome
  - `Matricula`: 4 testes - validações de IDs
  - `Notas`: 10 testes - validações, cálculos, situação

- **Services (58 testes)**:
  - `AlunoService`: 20 testes - CRUD, validações, erros
  - `DisciplinaService`: 18 testes - CRUD, período, validações
  - `MatriculaService`: 20 testes - CRUD, aluno-disciplina, validações

### 📊 Métricas Atualizadas

- **Total de Testes**: 86 testes
- **Taxa de Sucesso**: 100% (86/86 passando)
- **Tempo de Execução**: ~0.23s
- **Cobertura Backend**:
  - Models: 100% (todos os models)
  - AlunoService: 100% (54 linhas)
  - DisciplinaService: 100% (49 linhas)
  - MatriculaService: 93% (61 linhas, 4 não cobertas)
  - NotasService: 18% (pendente implementação)

## 🛠️ Tecnologias e Ferramentas

- **Framework**: `pytest` 7.4.4
- **Cobertura**: `pytest-cov` 6.1.1
- **Mocking**: `unittest.mock`
- **Validações**: `pytest.raises` para testes de exceções

## 🚀 Como Executar

### 1. Instalação de Dependências

```bash
pip install pytest pytest-cov
```

### 2. Executar Todos os Testes

```bash
# Na raiz do projeto:
python -m pytest test/backup/ -v
```

### 3. Executar com Cobertura

```bash
python -m pytest test/backup/ --cov=registro_notas_alunos --cov-report=term-missing -v
```

### 4. Executar Script Automático

```bash
python test/backup/test_coverage.py
```

### 5. Gerar Relatório HTML

```bash
python -m pytest test/backup/ --cov=registro_notas_alunos --cov-report=html:test/backup/coverage_html -v
```

## 🎯 Tipos de Testes Implementados

### 🔍 Testes de Models

**Objetivo**: Validar integridade dos dados e regras de negócio

```python
def test_aluno_criacao_valida(self):
    """Testa criação válida de aluno"""
    aluno = Aluno(id=1, nome="João Silva", matricula="2024001")

    assert aluno.id == 1
    assert aluno.nome == "João Silva"
    assert aluno.matricula == "2024001"
```

**Cenários Cobertos**:
- ✅ Criação válida com e sem ID
- ✅ Validações de campos obrigatórios
- ✅ Normalização de dados (remoção de espaços)
- ✅ Validações de range (notas 0.0-1.0, anos 2020-2030)
- ✅ Cálculos automáticos (nota final, situação)

### 🔧 Testes de Services

**Objetivo**: Validar lógica de negócio e operações CRUD

```python
def test_criar_sucesso(self):
    """Testa criação de aluno com sucesso"""
    mock_db = Mock()
    mock_db.execute_query.return_value = [(1,)]

    service = AlunoService(mock_db)
    id_criado = service.criar(nome="João Silva", matricula="2024001")

    assert id_criado == 1
```

**Cenários Cobertos**:
- ✅ Operações CRUD (Create, Read, Update, Delete)
- ✅ Validações de entrada (IDs inválidos, campos vazios)
- ✅ Tratamento de erros (registros não encontrados)
- ✅ Casos de sucesso e falha
- ✅ Integração com banco (mockado)

## 🏆 Boas Práticas Implementadas

### 🧩 Fixtures Reutilizáveis

```python
@pytest.fixture
def sample_aluno():
    """Aluno de exemplo para testes"""
    return Aluno(id=1, nome="João Silva", matricula="2024001")
```

### 🎭 Mocking Eficiente

```python
mock_db = Mock()
mock_db.execute_query.return_value = [(1,)]
service = AlunoService(mock_db)
```

### 🎯 Testes Específicos

- **Casos Felizes**: Operações que devem funcionar
- **Casos de Erro**: Validações e tratamento de exceções
- **Casos Limite**: Valores extremos e edge cases

## 📈 Resultados Detalhados

### ✅ Componentes Totalmente Cobertos (100%)

| Componente | Linhas | Cobertura | Status |
|------------|--------|-----------|--------|
| Aluno Model | 14 | 100% | ✅ |
| Disciplina Model | 16 | 100% | ✅ |
| Matricula Model | 12 | 100% | ✅ |
| Notas Model | 31 | 100% | ✅ |
| AlunoService | 54 | 100% | ✅ |
| DisciplinaService | 49 | 100% | ✅ |

### 🔄 Em Desenvolvimento

| Componente | Linhas | Cobertura | Status |
|------------|--------|-----------|--------|
| MatriculaService | 61 | 93% | 🟡 4 linhas não testadas |
| NotasService | 83 | 18% | ⚠️ Pendente implementação |
| Database | 46 | 48% | ⚠️ Conexão real não testada |

## 📚 Guia de Execução

### Execução Local

1. **Certifique-se de estar na raiz do projeto**:
   ```bash
   pwd
   # Deve mostrar: .../registro-notas-alunos
   ```

2. **Execute os testes**:
   ```bash
   python -m pytest test/backup/ -v
   ```

3. **Para ver cobertura**:
   ```bash
   python -m pytest test/backup/ --cov=registro_notas_alunos --cov-report=term-missing
   ```

### Depuração de Problemas

- **ImportError**: Verifique se está na raiz do projeto
- **ModuleNotFoundError**: Execute `pip install pytest pytest-cov`
- **Falhas específicas**: Execute teste individual com `-s` para ver prints

### Relatórios de Cobertura

- **Terminal**: `--cov-report=term-missing`
- **HTML**: `--cov-report=html:test/backup/coverage_html`
- **XML**: `--cov-report=xml`

## 🔄 Próximos Passos

### 🎯 Metas Pendentes

- [ ] Completar testes do NotasService (15 testes planejados)
- [ ] Melhorar cobertura do MatriculaService (4 linhas restantes)
- [ ] Testes de integração com banco real
- [ ] Testes de performance

### 📈 Meta de Cobertura

- [x] **Models**: 100% ✅
- [x] **Services Críticos**: 95%+ ✅
- [ ] **Total Backend**: >90%
- [ ] **Sistema Completo**: >80%

---

**🎉 Sistema desenvolvido com arquitetura Package-as-Services e princípios SOLID**
