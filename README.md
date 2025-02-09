# Grid Graph - Instruções de Uso

Este documento fornece instruções detalhadas para configurar e executar o Grid Analyzer.

## Pré-requisitos

Antes de começar, você precisa ter instalado:

1. Python 3.6 ou superior
2. Graphviz (biblioteca do sistema)
3. Python package graphviz

## Instalação

### 1. Instalando o Graphviz

#### No Windows:
```bash
# Usando chocolatey
choco install graphviz

# Ou baixe o instalador em:
# https://graphviz.org/download/
```

#### No Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install graphviz
```

#### No macOS:
```bash
brew install graphviz
```

### 2. Instalando a biblioteca Python
```bash
pip install graphviz
```

## Estrutura do Código

O código está organizado em um único arquivo que contém:

- Classe `GridAnalyzer`: responsável pela análise da grade
- Funções auxiliares para criar grades de exemplo
- Função de visualização no terminal
- Função principal para execução

## Como Usar

1. Salve o código em um arquivo chamado `grid_analyzer.py`

2. Execute o script:
```bash
python grid_analyzer.py
```

3. O script irá:
   - Gerar uma grade de exemplo
   - Mostrar a visualização da grade no terminal
   - Criar dois arquivos de visualização:
     - `grid_graph.pdf`
     - `grid_graph.png`

## Personalizando a Grade

Você pode personalizar a grade de duas maneiras:

### 1. Usando a grade de exemplo simples

Modifique a função `create_example_grid()`:

```python
def create_example_grid():
    grid = [
        ['R', 'R', '1', '1', 'R'],
        ['R', 'R', '1', '1', 'R'],
        ['R', 'R', 'R', 'R', 'R'],
        ['2', '2', 'R', '3', '3'],
        ['2', '2', 'R', '3', '3']
    ]
    warehouse_ids = {'1', '3'}
    return grid, warehouse_ids
```

### 2. Usando a grade maior

Modifique os parâmetros na função `create_larger_grid(width=20, height=20)`:

```python
grid = create_larger_grid(width=30, height=30)  # Para uma grade 30x30
```

## Elementos da Grade

- `'R'`: Representa uma estrada
- `'1'`, `'2'`, `'3'`, etc.: Representam edifícios
- `'.'`: Representa espaço vazio
- O conjunto `warehouse_ids` define quais números representam armazéns

## Saída

O programa gera três tipos de visualização:

1. **Terminal**: Representação ASCII da grade
2. **PDF**: Grafo detalhado em formato PDF
3. **PNG**: Grafo detalhado em formato PNG

Nos grafos gerados:
- Os nós mostram as coordenadas (x, y)
- As arestas mostram:
  - W: Largura da estrada
  - D: Distância entre os nós

## Resolução de Problemas

### Erro: "graphviz.backend.ExecutableNotFound"
Significa que o Graphviz não está instalado no sistema ou não está no PATH. Certifique-se de:
1. Instalar o Graphviz usando as instruções acima
2. Reiniciar o terminal após a instalação
3. Verificar se o comando `dot -V` funciona no terminal

### Erro: "ModuleNotFoundError: No module named 'graphviz'"
Execute:
```bash
pip install graphviz
```

## Exemplo de Uso em Código

```python
from grid_analyzer import GridAnalyzer

# Criar uma grade personalizada
my_grid = [
    ['R', 'R', '1'],
    ['R', 'R', '1'],
    ['2', 'R', 'R']
]
warehouse_ids = {'1'}

# Inicializar o analisador
analyzer = GridAnalyzer(my_grid, warehouse_ids)

# Gerar e salvar o grafo
graphviz_code = analyzer.analyze()
dot = graphviz.Source(graphviz_code)
dot.render("my_graph", format="png", cleanup=True)
```

## Contribuindo

Para contribuir com melhorias:

1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Faça suas alterações
4. Envie um pull request

## Suporte

Em caso de dúvidas ou problemas:
1. Verifique a seção de resolução de problemas acima
2. Abra uma issue no repositório
3. Entre em contato com o mantenedor
