
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


class Agendamento(db.Model):
    __tablename__ = "agendamentos"

    id_agendamento = db.Column(db.Integer, primary_key=True)

    id_cliente = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id_cliente"),
        nullable=False
    )

    id_servico = db.Column(
        db.Integer,
        db.ForeignKey("servicos.id_servico"),
        nullable=False
    )

    data_hora = db.Column(db.DateTime, nullable=False)

    status = db.Column(
        db.String(20),
        nullable=False,
        default="agendado"
    )

    cliente = db.relationship("Cliente", backref="agendamentos")
    servico = db.relationship("Servico", backref="agendamentos")
