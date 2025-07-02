symbol_table = []

declare_value_type =    { 
                        "int" : "int = 0", 
                        "real" : "float = 0.0",
                        "char" :  "chr = 0",
                        }

def register_variable(variable):
    """Register a new variable in the symbol table"""
    if(len(symbol_table) > 0):
        if variable not in symbol_table:
            symbol_table.append(variable)
        else:
            raise Exception("(!) Variable " + str(variable) + " already exists")
    else:
            symbol_table.append(variable)
            
def is_variable_declared(variable):
    """Check if a variable is declared in the symbol table"""
    if(len(symbol_table) > 0):
        if variable not in symbol_table:
            return False
        else:
            return True
    else:
        return False
    
def format_string_concatenation(string_list):
    """Format string concatenation for print statements"""
    result_list = []
    inside_quotes = False

    for item in string_list:
        if isinstance(item, str) and item.strip().startswith('"') and item.strip().endswith('"'):
            result_list.append(item)
        elif not inside_quotes and item == '+':
            result_list.append(item)
        else:
            result_list.append('str('+item+')')

    return " + ".join(result_list)

def apply_indentation(lines, indent):
    """Apply indentation to code lines"""
    return ' '.join(indent + line for line in lines.splitlines())