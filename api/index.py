from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv 
import os
load_dotenv(find_dotenv())
#Vamos criar uma nova conexão usando esta URI

uri = os.environ.get('MONGODB_URI')
db = MongoClient(uri, ssl=True, tlsAllowInvalidCertificates=True)['mjd_2024']

app = Flask(__name__)
# Rota 1
@app.route('/')
def home():
    alunos = db.pedro_alunos_2 
    turma = alunos.find()
    return render_template('index.html', turma=turma)


@app.route('/busca', methods=['GET', 'POST'])
def busca():
    numero = request.form['nome'] # request.form.get("nome")
    aluno = db.pedro_alunos_2.find_one({"id": numero})
    return render_template('estudante.html', estudante=aluno)


@app.route('/about')
def about():
    return 'Alguma coisa diferente'


@app.route('/teste/<id>')
def estudante(id):
    aluno = turma[id]
    return render_template('estudante.html', estudante=aluno)

