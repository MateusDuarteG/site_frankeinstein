from flask import Flask, jsonify, request, render_template
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
print(os.getenv("MAIL_USERNAME"))
print(os.getenv("MAIL_PASSWORD"))

# Configurações de e-mail usando variáveis de ambiente
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# Configuração do servidor de e-mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True


mail = Mail(app)

# --- Rotas de agentes (mantém igual) ---
agent = [
    {'id': 1, 'Nome': 'Mateus Duarte', 'Matricula': '147884'},
    {'id': 2, 'Nome': 'Pricila Brito', 'Matricula': '1456788'},
    {'id': 3, 'Nome': 'Romeu Zelito', 'Matricula': '1456458'}
]


@app.route('/agent', methods=['GET'])
def obter_agent():
    return jsonify(agent)


@app.route('/agent/<int:id>', methods=['GET'])
def obter_agent_id(id):
    for agents in agent:
        if agents.get('id') == id:
            return jsonify(agents)


@app.route('/agent/<int:id>', methods=['PUT'])
def editar_agent_id(id):
    agent_alterado = request.get_json()
    for indice, agents in enumerate(agent):
        if agents.get('id') == id:
            agent[indice].update(agent_alterado)
            return jsonify(agent[indice])


@app.route('/agent', methods=['POST'])
def incluir_novo_agent():
    novo_agents = request.get_json()
    agent.append(novo_agents)
    return jsonify(agent)


@app.route('/agent/<int:id>', methods=['DELETE'])
def excluir_agnt(id):
    for indice, agents in enumerate(agent):
        if agents.get('id') == id:
            del agent[indice]
    return jsonify(agent)

# --- Nova rota de contato ---
# Rota para página inicial


@app.route('/')
def index():
    return render_template('index.html')

# Rota para projetos


@app.route("/projetos")
def projetos():
    projects = [
        {
            "title": "Portfólio Pessoal",
            "description": "Site feito em Flask com Bootstrap",
            "link": "https://github.com/MateusDuarteG/site_portfolio"
        },
        {
            "title": "API Flask",
            "description": "API simples para autenticação",
            "link": "https://github.com/MateusDuarteG/api_flask"
        },
        {
            "title": "Automação de Tarefas",
            "description": "Scripts para automatizar processos",
            "link": "https://github.com/MateusDuarteG/automacoes"
        }
    ]
    return render_template("projetos.html", projects=projects)


# Rota para contato (formulário)


@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']

        # Enviar e-mails (já configurado)
        msg = Message('Novo contato do site',
                      sender=email,
                      recipients=['mateuscp1708@gmail.com'])
        msg.body = f"Nome: {nome}\nEmail: {email}\nMensagem: {mensagem}"
        mail.send(msg)

        resposta = Message('Obrigado pelo contato!',
                           sender='mateuscp1708@gmail.com',
                           recipients=[email])
        resposta.body = "Olá, recebemos sua mensagem e entraremos em contato em breve."
        mail.send(resposta)

        return jsonify({"status": "sucesso", "mensagem": "Contato enviado!"})

    # Se for GET, renderiza a página de contato
    return render_template('contato.html')


if __name__ == "__main__":
    app.run(debug=True)
