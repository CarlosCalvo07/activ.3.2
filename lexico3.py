import ply.lex as lex

# Definir los tokens
tokens = ['RESERVED', 'IDENTIFIER', 'LEFT_PAREN', 'RIGHT_PAREN', 'LBRACE', 'RBRACE', 'SEMICOLON']

# Palabras reservadas
reserved_keywords = {
    'for': 'RESERVED',
    'For': 'RESERVED',
    'Main': 'RESERVED',
    'main': 'RESERVED',
    'int': 'RESERVED',
    'Int': 'RESERVED'
}

# Corrección de palabras mal escritas
word_corrections = {
    'mai': 'main',
    'fo': 'for',
    'In': 'int',
    'Ma': 'Main',
    'in': 'int'
}

# Lista de errores léxicos
lexical_errors = []

# Función para identificadores o palabras reservadas
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved_keywords:
        t.type = reserved_keywords[t.value]
    else:
        suggestion = word_corrections.get(t.value[:3], None)
        if suggestion:
            error_msg = f"Error léxico: '{t.value}' no es válido. Quizás quisiste decir '{suggestion}' en la línea {t.lineno}, posición {t.lexpos}."
            lexical_errors.append(error_msg)
        else:
            t.type = 'IDENTIFIER'
    return t

# Paréntesis y llaves
t_LEFT_PAREN = r'\('
t_RIGHT_PAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'

# Ignorar espacios y tabs
t_ignore = ' \t'

# Contador de líneas nuevas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
    global lexical_errors
    if t.value[0].isspace():
        t.lexer.skip(1)
        return
    suggestion = word_corrections.get(t.value[:3], None)
    if suggestion:
        error_msg = f"Error léxico: '{t.value}' no es válido. Quizás quisiste decir '{suggestion}' en la línea {t.lineno}, posición {t.lexpos}."
    else:
        error_msg = f"Carácter ilegal '{t.value[0]}' en la línea {t.lineno}, posición {t.lexpos}."
    lexical_errors.append(error_msg)
    t.lexer.skip(1)

# Inicialización del lexer
lexer = lex.lex()

def lexico(text):
    global lexical_errors
    lexical_errors.clear()
    lexer.input(text)
    tokens_list = []

    while True:
        token = lexer.token()
        if not token:
            break
        tokens_list.append((token.type, token.value, token.lineno, token.lexpos))

    return tokens_list