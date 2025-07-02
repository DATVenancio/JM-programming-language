import ply.lex as lex
import sys
import os

# Reserved words
reserved_words = {
    'int' : 'TIPO_INT',
    'real' : 'TIPO_REAL',
    'char' : 'TIPO_CHAR',
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'print' : 'PRINT',
    'read' : 'READ',
    'start' : 'INICIO',
    'end' : 'FIM',
    'write' : 'WRITE',
}

# Tokens
tokens = [
    'SEPARADOR',               # .
    'PONTO_E_VIRGULA',         # ;
    'ABRE_PARENTESES',         # (
    'FECHA_PARENTESES',        # )
    'INICIO_BLOCO',            # {
    'FINAL_BLOCO',             # }
    'SOMA',                    # +
    'SUB',                     # -
    'MULT',                    # *
    'DIV',                     # /
    'INT',                     # int
    'REAL',                    # real
    'CHAR',                    # char
    'VARIAVEL',                # nome da variavel
    'AND',                     # &
    'OR',                      # |
    'MENOR',                   # <
    'MAIOR',                   # >
    'MENOR_OU_IGUAL',          # <=
    'MAIOR_OU_IGUAL',          # >=
    'IGUAL_IGUAL',             # ==
    'DIFERENTE',               # !=
    'IGUAL',                   # =
    'COMENTARIO',              # comentario
    'QUEBRA_LINHA',            # \n
    'IGNORE',                  # Ignorar espaços
    'STRING',                  # string literals


] + list(reserved_words.values()) 

# General regular expressions
t_INICIO                = r'start'
t_FIM                   = r'end'
t_IF                    = r'if'
t_ELSE                  = r'else'
t_WHILE                 = r'while'
t_READ                  = r'read'
t_PRINT                 = r'print'
t_WRITE                 = r'write'
t_TIPO_INT              = r'int'
t_TIPO_CHAR             = r'char'
t_TIPO_REAL            = r'real'
t_SOMA = r'\+'
t_SUB = r'\-'
t_MULT = r'\*'
t_DIV = r'/'
t_AND = r'\&'
t_OR = r'\|'
t_MENOR = r'\<'
t_MAIOR = r'\>'
t_MENOR_OU_IGUAL = r'\<\='
t_MAIOR_OU_IGUAL = r'\>\='
t_IGUAL_IGUAL = r'\=\='
t_DIFERENTE = r'\!\='
t_SEPARADOR = r'\.'
t_PONTO_E_VIRGULA = r'\;'
t_ABRE_PARENTESES  = r'\('
t_FECHA_PARENTESES  = r'\)'
t_INICIO_BLOCO = r'\{'
t_FINAL_BLOCO = r'\}'
t_IGUAL = r'\='
t_IGNORE = r' \t'


# Complex regular expressions
def t_INT(t):
    r'[+-]?\d+'
    max_digits = (len(t.value))
    if (max_digits > 15):       
        t.value = 0
    else:
        t.value = int(t.value)
    return t

def t_CHAR(t):
    r'\"(\w|\+|\-|\*|/|\%)\"'
    return t

def t_REAL(t):
    r'[+-]?(\d*\.\d*)|(\d+\.\d*)'
    t.value = float(t.value)  
    return t

def t_VARIAVEL(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved_words:
        t.type = reserved_words[t.value]
    return t

def t_STRING(t):
    r'"[^"]*"'
    return t

def t_COMENTARIO(t):
     r'\#.*'
     return(t)
     
def t_QUEBRA_LINHA(t):
    r'"\n"'
    t.lexer.lineno += len(t.value)
    return t




precedence = (
    ('left','SOMA','SUB'),
    ('left','MULT','DIV'),
    ('left','ABRE_PARENTESES','FECHA_PARENTESES'),
    ('left','AND','OR'),
    ('left','MAIOR','MENOR', 'MAIOR_OU_IGUAL', 'MENOR_OU_IGUAL', 'IGUAL_IGUAL', 'DIFERENTE'),
    ('left', 'IF', 'ELSE')
)

lexical_errors = []
def t_error(t):
    lexical_errors.append((t.lineno,t.lexpos,t.type,t.value, f'Character not recognized by this language'))
    t.lexer.skip(1)

filename, file_extension = os.path.splitext(sys.argv[1])

source_file = open(sys.argv[1], 'r')

source_code = ""
for line in source_file:
    source_code += line

lexer = lex.lex()
lexer.input(source_code)


filename = filename[filename.rfind("/")+1:]
with open(f"./logs/tokens_{filename}.txt", "w") as token_file, open(f"./logs/erros_{filename}.txt", "w+") as error_file:
        token_file.write(f"( TOKEN, 'palavra/simbolo' )\n")
        for token in lexer:
            token = (f"( {token.type}, '{token.value}' )").replace("LexToken","")
            token_file.write(f"{token}\n")
        token_file.close()
        error_file.write(f"( TOKEN, 'palavra/simbolo' )\n")
        for token in lexer:
            token = (f"( {token.type}, '{token.value}' )").replace("LexToken","")
            error_file.write(f"{token}\n")
        error_file.close()