from flask import Flask, render_template, request

app = Flask(__name__)
# Rota 1
@app.route('/')
def home():
    return render_template('index.html', turma=turma)


@app.route('/busca', methods=['GET', 'POST'])
def busca():
    numero = request.form['nome'] # request.form.get("nome")
    for aluno in turma:
        if aluno["id"] == numero:
            resposta = aluno
            break
    return render_template('estudante.html', estudante=resposta)


@app.route('/about')
def about():
    return 'Alguma coisa diferente'


@app.route('/teste/<id>')
def estudante(id):
    aluno = turma[id]
    return render_template('estudante.html', estudante=aluno)

    
turma = [{"id": "1", "nome": "João", "idade": 20, "curso": "Engenharia"},
         {"id": "2", "nome": "Maria", "idade": 22, "curso": "Medicina"},
         {"id": "3", "nome": "José", "idade": 21, "curso": "Direito"},
         {"id": "4", "nome": "Ana", "idade": 23, "curso": "Administração"},
         {"id": "5", "nome": "Pedro", "idade": 24, "curso": "Contabilidade"}]