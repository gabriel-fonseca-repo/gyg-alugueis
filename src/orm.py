from datetime import datetime

from flask_login import UserMixin
from app import db


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)


class Carro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(8), unique=True, nullable=False)
    modelo = db.Column(db.String(100), nullable=False)


class Aluguel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inicio_aluguel = db.Column(db.DateTime, nullable=False,
                               default=datetime.utcnow)
    final_aluguel = db.Column(db.DateTime, nullable=False)

    carro_id = db.Column(db.Integer, db.ForeignKey('carro.id'),
                         nullable=False)
    carro = db.relationship('Carro',
                            backref=db.backref('carro_alugueis', lazy=True))

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'),
                           nullable=False)
    usuario = db.relationship('Usuario',
                              backref=db.backref('usuario_alugueis', lazy=True))
