
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
from models import db, Cliente, Servico, Agendamento

app = Flask(__name__)

# Configuração do banco de dados SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///salao.db"

# Conectar o banco ao Flask
db.init_app(app)

# Criar as tabelas do banco de dados
with app.app_context():
    db.create_all()


@app.route("/")
def inicio():
    return "<h1>Sistema de Gestão - Salão de Beleza</h1>"



@app.route("/agendamentos")
def listar_agendamentos():
    agendamentos = Agendamento.query.order_by(
        Agendamento.data_hora
    ).all()

    return render_template(
        "lista_agendamentos.html",
        agendamentos=agendamentos
    )

    agendamentos = Agendamento.query.order_by(
        Agendamento.data_hora
    ).all()

    html = "<h1>Agendamentos do Salão</h1>"

    if not agendamentos:
        return html + "<p>Nenhum agendamento cadastrado.</p>"

    for agendamento in agendamentos:
        html += (
            f"<p>Cliente: {agendamento.cliente.nome} | "
            f"Serviço: {agendamento.servico.nome} | "
            f"Data: {agendamento.data_hora:%d/%m/%Y %H:%M} | "
            f"Status: {agendamento.status}</p>"
        )

    return html


@app.route("/agendamentos/novo", methods=["GET", "POST"])
def novo_agendamento():
    clientes = Cliente.query.order_by(Cliente.nome).all()
    servicos = Servico.query.order_by(Servico.nome).all()

    if request.method == "POST":
        try:
            id_cliente = int(request.form["cliente"])
            id_servico = int(request.form["servico"])
            data_hora = datetime.fromisoformat(
                request.form["data_hora"]
            )
        except (ValueError, KeyError):
            return "Dados inválidos.", 400

        cliente = db.session.get(Cliente, id_cliente)
        servico = db.session.get(Servico, id_servico)

        if not cliente or not servico:
            return "Cliente ou serviço não encontrado.", 400

        if servico.duracao <= 0:
            return "Duração do serviço inválida.", 400

        inicio = data_hora
        fim = inicio + timedelta(minutes=servico.duracao)

        agendamentos = Agendamento.query.filter_by(
            status="agendado"
        ).all()

        for existente in agendamentos:
            inicio_existente = existente.data_hora
            fim_existente = inicio_existente + timedelta(
                minutes=existente.servico.duracao
            )

            if inicio < fim_existente and fim > inicio_existente:
                return "Horário indisponível.", 409

        novo = Agendamento(
            id_cliente=id_cliente,
            id_servico=id_servico,
            data_hora=data_hora,
            status="agendado"
        )

        db.session.add(novo)
        db.session.commit()

        return redirect(url_for("listar_agendamentos"))

    return render_template(
        "novo_agendamento.html",
        clientes=clientes,
        servicos=servicos
    )


@app.route("/clientes/novo", methods=["GET", "POST"])
def novo_cliente():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()

        if not nome or not telefone:
            return "Nome e telefone são obrigatórios.", 400

        cliente = Cliente(nome=nome, telefone=telefone)
        db.session.add(cliente)
        db.session.commit()

        return "Cliente cadastrado com sucesso!"

    return """
    <h1>Cadastrar Cliente</h1>
    <form method="POST">
        <label for="nome">Nome:</label>
        <input id="nome" name="nome" required>

        <br><br>

        <label for="telefone">Telefone:</label>
        <input id="telefone" name="telefone" required>

        <br><br>

        <button type="submit">Salvar Cliente</button>
    </form>
    """


@app.route("/servicos/novo", methods=["GET", "POST"])
def novo_servico():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()

        try:
            preco = float(request.form.get("preco", ""))
            duracao = int(request.form.get("duracao", ""))
        except ValueError:
            return "Preço ou duração inválidos.", 400

        if not nome or preco < 0 or duracao <= 0:
            return "Dados do serviço inválidos.", 400

        servico = Servico(
            nome=nome,
            preco=preco,
            duracao=duracao
        )

        db.session.add(servico)
        db.session.commit()

        return "Serviço cadastrado com sucesso!"

    return """
    <h1>Cadastrar Serviço</h1>

    <form method="POST">
        <label for="nome">Nome do serviço:</label>
        <input id="nome" name="nome" required>

        <br><br>

        <label for="preco">Preço (R$):</label>
        <input type="number" id="preco" name="preco"
               min="0" step="0.01" required>

        <br><br>

        <label for="duracao">Duração (minutos):</label>
        <input type="number" id="duracao" name="duracao"
               min="1" required>

        <br><br>

        <button type="submit">Salvar Serviço</button>
    </form>
    """


if __name__ == "__main__":
    app.run(debug=True)
