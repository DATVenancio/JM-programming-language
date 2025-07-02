from ply import yacc
from declarations import *
from lexer import *

# Auxiliary variables
indentation = '''
    '''

# Syntax Analysis
def p_empty(p): 
    '''empty :
    '''
    p[0] = ""

def p_statement_terminator(p): 
    '''end : PONTO_E_VIRGULA
    '''

def p_main_program(p): 
    '''main : INICIO INICIO_BLOCO lista_codigo FINAL_BLOCO FIM
    '''
    with open(f"{filename}.py", "w") as output_file, open(f"./logs/erros_{filename}.txt", "w") as error_log:
        output_file.write(f"{p[3]}")
    output_file.close()
    error_log.close()

def p_code_statement(p): 
    '''codigo   : condicional
                | atribuicao end
                | entrada end
                | saida_string end
                | declaracao
                | while
                | comentario
    '''
    p[0] = p[1]

def p_code_list(p): 
    '''lista_codigo : codigo lista_codigo
                    | empty
    '''
    if(len(p) == 2):
        p[0] = f''
    else:
        if p[2] == "":
            p[0] = f'{p[1]}'
        else:
            p[0] = f'{p[1]}'+f'\n'+f'{p[2]}'

def p_comment(p):
    '''comentario : COMENTARIO
    '''
    comment_text = p[1].replace("#", '')
    p[0] = f"#{comment_text}"

def p_data_types(p):
    '''type : TIPO_INT
            | TIPO_REAL
            | TIPO_CHAR
    '''
    p[0] = p[1]

def p_literal_values(p): 
    '''valTipo : INT
               | REAL
               | CHAR
    ''' 
    p[0] = p[1]

def p_variable_declaration(p): 
    '''declaracao : type VARIAVEL end
                  | type VARIAVEL IGUAL expression end
                  | type VARIAVEL IGUAL READ ABRE_PARENTESES string_expression FECHA_PARENTESES end
    '''
    register_variable(p[2])
    if len(p) == 4:
        default_value = declare_value_type[p[1]]
        p[0] = f"{p[2]}: {default_value}"
    elif str(p[4]) == "read":
        p[0] = f"{p[2]} = {p[1]}(input({p[6]}))"
    else:
        p[0] = f"{p[2]} = {p[4]}"

def p_variable_assignment(p): 
    '''atribuicao : VARIAVEL IGUAL expression
                  | VARIAVEL IGUAL valTipo
                  | VARIAVEL IGUAL READ ABRE_PARENTESES string_expression FECHA_PARENTESES
    '''
    if(str(p[3]) == "read"):
        p[0] = f"{p[1]} {p[2]} type({p[1]}) (input({p[5]}))"
    else:
        p[0] = f"{p[1]} {p[2]} {p[3]}"

def p_input_statement(p): 
    '''entrada  : VARIAVEL IGUAL READ ABRE_PARENTESES string_expression FECHA_PARENTESES
    '''
    p[0] = f"{p[1]} = input({p[5]})"

def p_string_output(p): 
    '''saida_string : WRITE ABRE_PARENTESES string_expression FECHA_PARENTESES 
                    | WRITE ABRE_PARENTESES expression FECHA_PARENTESES 
    '''
    if len(p) == 4:
        # Handle string_expression case
        p[0] = f'print({p[3]}, end="")'
    else:
        # Handle expression case (for arithmetic operations, variables, etc.)
        p[0] = f'print({format_string_concatenation(p[3].split("+"))}, end="")'

def p_string_expression(p):
    '''string_expression : STRING
                        | VARIAVEL
                        | string_expression SOMA string_expression
                        | string_expression SOMA VARIAVEL
                        | VARIAVEL SOMA string_expression
    '''
    if len(p) == 2:
        if p[1].startswith('"') and p[1].endswith('"'):
            # It's a string literal
            p[0] = p[1]
        else:
            # It's a variable, convert to string
            p[0] = f"str({p[1]})"
    else:
        # Handle concatenation cases
        left_operand = p[1]
        right_operand = p[3]
        
        # Convert variables to strings if they're not already strings
        if not left_operand.startswith('"') and not left_operand.startswith('str('):
            left_operand = f"str({left_operand})"
        if not right_operand.startswith('"') and not right_operand.startswith('str('):
            right_operand = f"str({right_operand})"
            
        p[0] = f"{left_operand} + {right_operand}"

def p_relational_operators(p):
    '''opRel : IGUAL_IGUAL 
             | MAIOR_OU_IGUAL
             | MENOR_OU_IGUAL
             | MAIOR
             | MENOR
             | DIFERENTE
    '''      
    p[0] = p[1]

def p_arithmetic_operators(p):
    '''opArit : SOMA 
              | SUB
              | MULT
              | DIV
    '''
    p[0] = p[1]

def p_comparison_with_parentheses(p): 
    '''comparacao : ABRE_PARENTESES comparacao FECHA_PARENTESES
    '''
    p[0] = f"({p[2]})"

def p_simple_comparison(t):
    '''comparacao : relacional
    '''
    t[0] = t[1]

def p_logical_operators(p): 
    '''comparacao : comparacao AND comparacao
                  | comparacao OR comparacao
    '''
    if(p[2] == "&&"):
        p[0] = f"{p[1]} and {p[3]}"
    elif(p[2] == "||"):
        p[0] = f"{p[1]} or {p[2]}"
    else:
        with open(f"erros_{filename}.txt", "w") as error_log:
            error_log.write(f"(!) Invalid operation\n")
        raise Exception("(!) Invalid operation")

def p_relational_operands(p): 
    '''relacional : VARIAVEL
                  | valTipo
    '''
    p[0] = f"{p[1]}"

def p_relational_expression(p): 
    '''relacional : relacional opRel relacional
    '''
    try: 
        try:
            left_type_check = is_variable_declared(p[1])
            left_value = symbol_table[p[1]][1]
        except:
            left_type_check = type(p[1])
            left_value = p[1]
        try:
            right_type_check = is_variable_declared(p[3])
            right_value = symbol_table[p[3]][1]
        except:
            right_type_check = type(p[3])
            right_value = p[3]
        if(left_type_check != right_type_check):
            with open(f"erros_{filename}.txt", "w") as error_log:
                error_log.write(f"(!) Operation with different types\n")
            raise Exception ("(!) Operation with different types")
        else:
            if(type(p[1]) == str and type(p[3]) == str):
                if(p[2] == '=='):
                    p[0] = f"{p[1]} == {p[3]}"
                elif(p[2] == '>='):
                    p[0] = f"{p[1]} >= {p[3]}"
                elif(p[2] == '<='):
                    p[0] = f"{p[1]} <= {p[3]}"
                elif(p[2] == '>'):
                    p[0] = f"{p[1]} > {p[3]}"
                elif(p[2] == '<'):
                    p[0] = f"{p[1]} < {p[3]}"
                elif(p[2] == '!='):
                    p[0] = f"{p[1]} != {p[3]}"
                else:
                    with open(f"erros_{filename}.txt", "w") as error_log:
                        error_log.write(f"(!) Invalid operator\n")
                    raise Exception("(!) Invalid operator")
            else:
                if(p[2] == '=='):
                    p[0] = f"{left_value} == {right_value}"
                elif(p[2] == '>='):
                    p[0] = f"{left_value} >= {right_value}"
                elif(p[2] == '<='):
                    p[0] = f"{left_value} <= {right_value}"
                elif(p[2] == '>'):
                    p[0] = f"{left_value} > {right_value}"
                elif(p[2] == '<'):
                    p[0] = f"{left_value} < {right_value}"
                elif(p[2] == '!='):
                    p[0] = f"{left_value} != {right_value}"
                else:
                    with open(f"erros_{filename}.txt", "w") as error_log:
                        error_log.write(f"(!) Invalid operator\n")
                    raise Exception("(!) Invalid operator")
    except:
        if(type(p[1]) != type(p[3])):
            with open(f"erros_{filename}.txt", "w") as error_log:
                error_log.write(f"(!) Operation with different types\n")
            raise Exception ("(!) Operation with different types")
        else:
            if(p[2] == '=='):
                p[0] = f"{p[1]} == {p[3]}"
            elif(p[2] == '>='):
                p[0] = f"{p[1]} >= {p[3]}"
            elif(p[2] == '<='):
                p[0] = f"{p[1]} <= {p[3]}"
            elif(p[2] == '>'):
                p[0] = f"{p[1]} > {p[3]}"
            elif(p[2] == '<'):
                p[0] = f"{p[1]} < {p[3]}"
            elif(p[2] == '!='):
                p[0] = f"{p[1]} != {p[3]}"
            else:
                with open(f"erros_{filename}.txt", "w") as error_log:
                    error_log.write(f"(!) Invalid operator\n")
                raise Exception("(!) Invalid operator")

def p_expression_with_parentheses(p):
    '''expression : ABRE_PARENTESES expression FECHA_PARENTESES
    '''
    p[0] = f"({p[2]})"

def p_expression_value(p):
    '''expression : valTipo
                  | VARIAVEL
    '''
    p[0] = f"{p[1]}"

def p_binary_arithmetic_expression(p):
    '''expression : expression opArit expression
    '''
    if p[2] == '+':
        p[0] = f"{p[1]} + {p[3]}"
    elif p[2] == '-':
        p[0] = f"{p[1]} - {p[3]}"
    elif p[2] == '*':
        p[0] = f"{p[1]} * {p[3]}"
    elif p[2] == '/':
        p[0] = f"{p[1]} / {p[3]}"
    else:
        with open(f"erros_{filename}.txt", "w") as error_log:
            error_log.write(f"(!) Invalid sign\n")
        raise Exception("(!) Invalid sign")

def p_conditional_statement(p): 
    '''condicional : IF ABRE_PARENTESES comparacao FECHA_PARENTESES INICIO_BLOCO lista_codigo FINAL_BLOCO
                   | IF ABRE_PARENTESES comparacao FECHA_PARENTESES INICIO_BLOCO lista_codigo FINAL_BLOCO ELSE INICIO_BLOCO lista_codigo FINAL_BLOCO
    '''

    if_block_code = p[6].replace("\n", indentation)
    else_block_code = p[10].replace("\n", indentation)

    if(len(p) == 8):
        p[0] = f'''if {p[3]}:{indentation}{if_block_code}'''
    else:
        p[0] = f'''if {p[3]}:{indentation}{if_block_code}\nelse:{indentation}{else_block_code}''' 

def p_while_loop(p): 
    '''while : WHILE ABRE_PARENTESES comparacao FECHA_PARENTESES INICIO_BLOCO lista_codigo FINAL_BLOCO
    '''
    
    loop_body_code = p[6].replace("\n", indentation)

    p[0] = f'''while {p[3]}:{indentation}{loop_body_code}'''

# Error handling
syntax_errors = []
def p_error(p):
    if(p):
        syntax_errors.append(p)
        print("PARSING ERROR - Token not recognized:", p)

parser = yacc.yacc(start = 'main')
result = parser.parse(source_code)