import ply.yacc as yacc
from lexico3 import tokens

# Lista de errores sintácticos
syntax_errors = []

# Bloque principal con paréntesis verificados
def p_main_structure(p):
    '''statement : RESERVED RESERVED LEFT_PAREN RIGHT_PAREN LBRACE statements RBRACE'''
    p[0] = ('main_structure', p[2], 'correcto')

# Variación donde falta el paréntesis de cierre
def p_main_missing_close_paren(p):
    '''statement : RESERVED RESERVED LEFT_PAREN LBRACE statements RBRACE'''
    error_msg = f"Error de sintaxis: Falta un paréntesis de cierre ')' en la línea {p.lineno(3)}, posición {p.lexpos(3)}."
    syntax_errors.append(error_msg)

# Variación donde falta el paréntesis de apertura
def p_main_missing_open_paren(p):
    '''statement : RESERVED RESERVED RIGHT_PAREN LBRACE statements RBRACE'''
    error_msg = f"Error de sintaxis: Falta un paréntesis de apertura '(' en la línea {p.lineno(3)}, posición {p.lexpos(3)}."
    syntax_errors.append(error_msg)

# Varios statements
def p_statements_multiple(p):
    '''statements : statements statement'''
    pass

def p_statements_single(p):
    '''statements : statement'''
    pass

# Declaración de variables con verificación de punto y coma
def p_variable_declaration(p):
    '''statement : RESERVED IDENTIFIER SEMICOLON'''
    if p[2] != 'x':
        error_msg = f"Error de sintaxis: Se esperaba 'x', pero se encontró '{p[2]}' en la línea {p.lineno(2)}, posición {p.lexpos(2)}."
        syntax_errors.append(error_msg)

    if p[3] != ';':
        error_msg = f"Error de sintaxis: Falta el punto y coma ';' al final en la línea {p.lineno(3)}, posición {p.lexpos(3)}."
        syntax_errors.append(error_msg)

# Declaración incompleta
def p_incomplete_declaration(p):
    '''statement : RESERVED IDENTIFIER'''
    error_msg = f"Error de sintaxis: Declaración incompleta. Falta ';' en la línea {p.lineno(2)}, posición {p.lexpos(2)}."
    syntax_errors.append(error_msg)

# Manejo de bloques con llaves
def p_brace_block(p):
    '''statement : LBRACE statements RBRACE'''
    p[0] = ('brace_block', 'correcto')

# Llaves faltantes
def p_missing_braces(p):
    '''statement : LBRACE statements
                 | statements RBRACE'''
    if len(p) == 3 and p[1] == '{':
        error_msg = "Error de sintaxis: Falta '}' para cerrar el bloque."
        syntax_errors.append(error_msg)
    elif len(p) == 3 and p[2] == '}':
        error_msg = "Error de sintaxis: Falta '{' al inicio del bloque."
        syntax_errors.append(error_msg)

# Manejo de errores sintácticos en general
def p_error(p):
    if p:
        if p.type == 'RBRACE':
            error_msg = f"Error de sintaxis: Falta '}}' para cerrar el bloque en la línea {p.lineno}, posición {p.lexpos}."
        else:
            error_msg = f"Error de sintaxis: Token inesperado '{p.value}' en la línea {p.lineno}, posición {p.lexpos}."
        syntax_errors.append(error_msg)
    else:
        # Here is where you are getting the 'Final inesperado del archivo' message.
        error_msg = "Error de sintaxis: Final inesperado del archivo. ¿Falta '}'?"
        syntax_errors.append(error_msg)


# Inicializar el parser
parser = yacc.yacc()

def sintactico(text):
    global syntax_errors
    syntax_errors.clear()
    try:
        result = parser.parse(text)
        return result
    except Exception as e:
        return str(e)