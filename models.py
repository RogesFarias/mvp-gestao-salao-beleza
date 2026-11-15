
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Cliente(db.Model):
    __tablename__ = "clientes"

    id_cliente = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)


class Servico(db.Model):
    __tablename__ = "servicos"

    id_servico = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    duracao = db.Column(db.Integer, nullable=False)
