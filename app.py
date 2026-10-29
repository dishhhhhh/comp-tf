import os
import ply.lex as lex
from flask import Flask, request, render_template

app = Flask(__name__)

# 1. Declaración de los tokens que reconocerá el metacompilador (PLY)
tokens = (
    'RESERVADA',
    'VARIABLE',
    'NUMERO',
    'OPERADOR',
    'DELIMITADOR'
)

# 2. Reglas léxicas simples
t_OPERADOR = r'[+\-*/=]'
t_DELIMITADOR = r'[\[\]\(\)\{\},;]'

# 3. Reglas léxicas complejas (Funciones PLY)
def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Diccionario de palabras reservadas para SVD y matrices
    reservadas = ['SVD', 'matriz', 'diagonalizar', 'transpuesta', 'inversa', 'autovalor', 'autovector']
    if t.value in reservadas:
        t.type = 'RESERVADA'
    return t

def t_NUMERO(t):
    r'\d+(\.\d+)?'
    return t

# 4. Caracteres ignorados (espacios, saltos de línea, tabulaciones)
t_ignore = ' \t\n\r'

# 5. Regla de manejo de errores léxicos
def t_error(t):
    print(f"Error léxico: Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construcción del analizador léxico mediante el metacompilador PLY
lexer = lex.lex()

def analizar_codigo(texto):
    lexer.input(texto)
    tokens_encontrados = []
    
    # Extraer tokens uno por uno usando el motor de PLY
    while True:
        tok = lexer.token()
        if not tok:
            break  # Fin del archivo
        tokens_encontrados.append(f"[{tok.type}: '{tok.value}']")
        
    return tokens_encontrados

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        archivo = request.files.get('file')

        if not archivo or archivo.filename == '':
            return render_template('index.html', error="No se seleccionó ningún archivo.")

        if not archivo.filename.endswith('.txt'):
            return render_template('index.html', error="El sistema solo acepta archivos .txt para el análisis.")

        try:
            contenido = archivo.read().decode('utf-8')
            tokens = analizar_codigo(contenido)
            return render_template('index.html', tokens=tokens)
        except Exception as e:
            return render_template('index.html', error=f"Error al procesar el archivo: {str(e)}")

    return render_template('index.html')

if __name__ == '__main__':
    puerto = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=puerto)
