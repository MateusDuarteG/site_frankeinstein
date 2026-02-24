from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configurações de e-mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

# Endpoint para enviar e-mail
@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    if not data or "to" not in data or "subject" not in data or "body" not in data:
        return jsonify({"error": "Campos obrigatórios: to, subject, body"}), 400
    
    try:
        msg = Message(
            subject=data["subject"],
            recipients=[data["to"]],
            body=data["body"]
        )
        mail.send(msg)
        return jsonify({"message": f"E-mail enviado para {data['to']} com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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

if __name__ == '__main__':
    app.run(debug=True)