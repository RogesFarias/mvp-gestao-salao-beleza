
from flask import Flask
from models import db, Cliente, Servico

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


if __name__ == "__main__":
    app.run(debug=True)
