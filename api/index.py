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


@app.route('/investigai')
def investigai():
    return render_template('pergunta_rag.html')


@app.route('/investigai_resposta', methods=['GET', 'POST'])
def investigai_resposta():
    query = request.form['pergunta'] # Pegamos a pergunta do formulário

    uri_embeddings = os.environ.get('MONGODB_EMBEDDINGS')
    database = 'comunicacao' # Nome da base que estamos usando.
    collection = 'teste_rag' # Nome da coleção que estamos usando. Substitua pela sua.
    # Importamos as bibliotecas necessárias da Langchain -- podemos fazer isso no topo do código também para agializar 
    # Os modelos abaixo "conversam" com o banco de dados e com o modelo de linguagem da OpenAI
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import MongoDBAtlasVectorSearch
    vector_search = MongoDBAtlasVectorSearch.from_connection_string(
        uri_embeddings,
        f'{database}.{collection}', 
        OpenAIEmbeddings(disallowed_special=()),
        index_name='default'
    )
    qa_retriever = vector_search.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 200,
            "post_filter_pipeline": [{"$limit": 25}]
        }
    )

    # Agora desenhamos um template par a pergunta
    from langchain.prompts import PromptTemplate
    prompt_template = """Use o contexto a seguir para responder a pergunta no final. 
        Se você não souber da resposta, apenas diga que não sabe. 
        Não tente inventar uma resposta.
    
        
        {context}


        Pergunta: {question}
        """
    
    prompt = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
    )

    from langchain.chains import RetrievalQA # Importamos o modelo de perguntas e respostas
    from langchain_openai import OpenAI    
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), # Qual LLM vamos usar para a tarefa
                                     chain_type="stuff", # stuff = "entucha" os documentos na query
                                     retriever=qa_retriever, # O modelo de recuperação que criamos
                                     return_source_documents=True, # Queremos mais detalhes sobre as fontes das respostas
                                     chain_type_kwargs={"prompt": prompt})
    docs = qa({"query": query}) # Finalmente chamamos a pergunta e a resposta
    resposta = docs["result"]
    pagina = docs['source_documents'][0].metadata['page']
    return render_template('resposta_rag.html', resposta=resposta, pagina=pagina)
