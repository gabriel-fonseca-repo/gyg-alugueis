from src.extensions import db
from datetime import datetime
from flask_security.models.fsqla_v3 import FsUserMixin, FsRoleMixin


class Carro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(8), unique=True, nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    descricao_imagem = db.Column(db.String(255), nullable=False)
    url_imagem = db.Column(db.String(255), nullable=False)


class Aluguel(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    inicio_aluguel = db.Column(
        db.DateTime(), nullable=False, default=datetime.utcnow)
    final_aluguel = db.Column(db.DateTime(), nullable=False)
    carro_id = db.Column(db.Integer(), db.ForeignKey(
        'carro.id'), nullable=False)
    carro = db.relationship(
        'Carro', backref=db.backref('carro_alugueis', lazy=True))
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref(
        'user_alugueis', lazy=True))


class User(db.Model, FsUserMixin):
    pass


class Role(db.Model, FsRoleMixin):
    page_url = db.Column(db.String(80))
    pass
