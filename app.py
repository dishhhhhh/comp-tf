import os
import re
from flask import Flask, request, render_template

app = Flask(__name__)

def analizar_codigo(texto):

    reglas = [
        ('RESERVADA', r'\b(SVD|matriz|diagonalizar|transpuesta|inversa|autovalor|autovector)\b'),
        ('VARIABLE', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
        ('NUMERO', r'\b\d+(\.\d+)?\b'),
        ('OPERADOR', r'[+\-*/=]'),
        ('DELIMITADOR', r'[\[\]\(\)\{\},;]'),
        ('ESPACIO', r'\s+')
    ]

    patron_regex = '|'.join(f'(?P<{nombre}>{patron})' for nombre, patron in reglas)
    tokens_encontrados = []

    for coincidencia in re.finditer(patron_regex, texto):
        tipo = coincidencia.lastgroup
        valor = coincidencia.group(tipo)
        if tipo != 'ESPACIO':  # omitir espacios
            tokens_encontrados.append(f"[{tipo}: '{valor}']")

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