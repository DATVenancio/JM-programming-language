# JM Programming Language

## Descrição

JM é uma linguagem de programação educacional desenvolvida como projeto acadêmico na disciplina ECOM06 - Compiladores no curso de Engenharia da Computação na Universidade Federal de Itajubá. Ela implementa um compilador que traduz código fonte escrito em sintaxe JM para código Python executável.

## Setup

### Pré-requisitos
- Python 3.x 
- pip (gerenciador de pacotes Python)

### Clone o repositório
```bash
git clone https://github.com/DATVenancio/JM-programming-language
```

### Criação de um ambiente virtual (opcional)
Crie um ambiente virtual utilizando o comando:
```bash
python -m venv <nome_do_seu_venv>
```
Ative o ambiente virtual com o comando:
```bash
source <nome_do_seu_venv>/bin/activate
```

### Instalação das Dependências
```bash
pip install -r requirements.txt
```

## Como Usar

Os códigos na linguagem JM são arquivos com a extensão `.jm`. É **extremamente necessário** para a execução dos arquivos JM que uma pasta com o nome `logs` seja criada na raiz do projeto, no mesmo diretório do arquivo `main.py`.

### Executando um Arquivo .jm

```bash
python main.py arquivo.jm
```

O projeto contém 3 códigos JM previamente criados:
- `helloworld.jm`: um código básico que exibe a mensagem "Hello World" na tela.
- `loop.jm`: um código básico que utiliza a estrutura `while` para exibir os números de 1 a 10 na tela.
- `expression.jm`: um código que lê 4 inputs do usuário (A, B, C e D) e calcula a expressão `result = (A + B) * (C / D)`. Além disso, o programa informa se o resultado é maior ou menor que 10.

### Exemplo de Uso
```bash
# Executar o exemplo Hello World
python main.py helloworld.jm

# Executar exemplo com expressões
python main.py expression.jm

# Executar exemplo com loop
python main.py loop.jm
```

## Estrutura do Projeto

```
JM-programming-language/
├── main.py              # Ponto de entrada do compilador
├── lexer.py             # Analisador léxico (PLY)
├── sintax.py            # Analisador sintático (PLY)
├── declarations.py      # Tabela de símbolos e utilitários
├── requirements.txt     # Dependências Python
├── logs/                # Diretório para logs de tokens e erros
├── helloworld.jm        # Exemplo básico
├── expression.jm        # Exemplo com expressões e condicionais
└── loop.jm             # Exemplo com loop while
```

## Características da Linguagem

### Tipos de Dados Suportados
- `int` - Números inteiros
- `real` - Números de ponto flutuante  
- `char` - Caracteres

### Estruturas de Controle
- **Condicionais**: `if` / `else`
- **Loops**: `while`
- **Entrada/Saída**: `read()`, `write()`, `print()`

### Operadores
- **Aritméticos**: `+`, `-`, `*`, `/`
- **Relacionais**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Lógicos**: `&` (AND), `|` (OR)

## Sintaxe da Linguagem JM

### Estrutura Básica
```jm
start {
    # Seu código aqui
} end
```

### Declaração de Variáveis
```jm
int variavel;
int variavel = 10;
int variavel = read("Digite um valor: ");
```

### Entrada e Saída
```jm
# Leitura de dados
int valor = read("Digite um número: ");

# Saída de texto
write("Olá, mundo!" + "\n");

# Saída de variáveis
write(valor);
```

### Estruturas Condicionais
```jm
if (condicao) {
    # código se verdadeiro
} else {
    # código se falso
}
```

### Loops
```jm
while (condicao) {
    # código do loop
}
```

### Comentários
```jm
# Este é um comentário
```

## Exemplos

### Hello World (helloworld.jm)
```jm
start { 
    # Hello World
    write("Hello World!" + "\n");
} end
```

### Expressões e Condicionais (expression.jm)
```jm
start { 
    # Calculate (A+B)*(C/D) and check if result is greater or lower than 10

    int A = read("Enter value for A: ");
    int B = read("Enter value for B: ");
    int C = read("Enter value for C: ");
    int D = read("Enter value for D: ");
    
    int result;
    result = (A + B) * (C / D);

    if (result > 10){
        write("The result " + result + " is greater than 10" + "\n");
    } else {
        write("The result " + result + " is lower than or equal to 10" + "\n");
    }

} end
```

### Loop While (loop.jm)
```jm
start { 
    # Print numbers from 1 to 10 using a while loop

    int i = 1;
    
    while (i <= 10) {
        write("Number: " + i + "\n");
        i = i + 1;
    }

} end 
```

## Como Funciona o Compilador

1. **Análise Léxica** (`lexer.py`): Converte o código fonte em tokens
2. **Análise Sintática** (`sintax.py`): Verifica a estrutura gramatical e gera código Python
3. **Tabela de Símbolos** (`declarations.py`): Gerencia variáveis e tipos
4. **Execução**: O código Python gerado é executado automaticamente

### Logs e Debugging

O compilador gera logs na pasta `logs/`:
- `tokens_arquivo.txt`: Lista de tokens identificados
- `erros_arquivo.txt`: Erros de sintaxe encontrados
