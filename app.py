from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def index():
    return render_template("index.html")


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


@app.route("/contato", methods=["GET", "POST"])
def contato():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        mensagem = request.form.get("mensagem")
        # Aqui você pode só retornar JSON por enquanto
        return jsonify({"status": "sucesso", "mensagem": "Contato enviado!"})
    return render_template("contato.html")
