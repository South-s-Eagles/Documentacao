# Constantes
TESTE = False

# caracteres usados em operadores
OPERADORES = "%*/+-!^="

# caracteres usados em números inteiros
DIGITOS = "0123456789"

# ponto decimal
PONTO = "."

# todos os caracteres usados em um números float
FLOATS = DIGITOS + PONTO

# caracteres usados em nomes de variáveis
LETRAS = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# abre e fecha parenteses
ABRE_FECHA_PARENTESES = "()"

# categorias
OPERADOR = 1  # para operadores aritméticos e atribuição
NUMERO = 2  # para números: todos são considerados float
VARIAVEL = 3  # para variáveis
PARENTESES = 4  # para '(' e ')

# Whitespace characters: space, newline, horizontal tab,
# vertical tab, form feed, carriage return
BRANCOS = [" ", "\n", "\t", "\v", "\f", "\r"]

# caractere que indica comentário
COMENTARIO = "#"


# ------------------------------------------------------------
def tokeniza(exp):
    tokens = []
    current_token = ""

    def add_token(token, tipo):
        tokens.append([token, tipo])

    for char in exp:
        if char.isdigit() or char == PONTO:
            current_token += char
        elif char.isalpha() or char == "_":
            current_token += char
        elif char in OPERADORES:
            if current_token:
                add_token(
                    current_token, VARIAVEL if current_token.isalpha() else NUMERO
                )
                current_token = ""
            add_token(char, OPERADOR)
        elif char in ABRE_FECHA_PARENTESES:
            if current_token:
                add_token(
                    current_token, VARIAVEL if current_token.isalpha() else NUMERO
                )
                current_token = ""
            add_token(char, PARENTESES)
        elif char == "#":
            break
        elif char.isspace():
            if current_token:
                add_token(
                    current_token, VARIAVEL if current_token.isalpha() else NUMERO
                )
                current_token = ""
        else:
            current_token += char

    if current_token:
        add_token(current_token, VARIAVEL if current_token.isalpha() else NUMERO)

    return tokens
