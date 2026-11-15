
from datetime import datetime

from app import app
from models import db, Cliente, Servico, Agendamento


def test_conflito_de_horarios():
    app.config["TESTING"] = True

    with app.app_context():
        cliente = Cliente(
            nome="Cliente Teste",
            telefone="11999999999"
        )

        servico = Servico(
            nome="Corte Teste",
            preco=50,
            duracao=60
        )

        db.session.add(cliente)
        db.session.add(servico)
        db.session.commit()

        agendamento = Agendamento(
            id_cliente=cliente.id_cliente,
            id_servico=servico.id_servico,
            data_hora=datetime(2026, 11, 20, 14, 0),
            status="agendado"
        )

        db.session.add(agendamento)
        db.session.commit()

        with app.test_client() as client:
            resposta = client.post(
                "/agendamentos/novo",
                data={
                    "cliente": cliente.id_cliente,
                    "servico": servico.id_servico,
                    "data_hora": "2026-11-20T14:30"
                }
            )

        assert resposta.status_code == 409
        assert b"Hor\xc3\xa1rio indispon\xc3\xadvel" in resposta.data

        db.session.delete(agendamento)
        db.session.delete(servico)
        db.session.delete(cliente)
        db.session.commit()
