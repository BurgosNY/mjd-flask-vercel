from flask import Flask, render_template

app = Flask(__name__)
# Rota 1
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return 'About'


@app.route('/teste/<nome>')
def muda_nome(nome):
    return transforma_nome(nome)


def transforma_nome(nome):
    return nome.upper()