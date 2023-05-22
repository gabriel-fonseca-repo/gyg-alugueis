from decimal import Decimal
from src.extensions import db, security
from datetime import datetime
from flask_security.models.fsqla_v3 import FsUserMixin, FsRoleMixin


class Carro(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    placa = db.Column(db.String(8), unique=True, nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    descricao_imagem = db.Column(db.Text(), nullable=False)
    url_imagem = db.Column(db.String(255), nullable=False)
    alugueis = db.relationship("Aluguel", back_populates="carro")
    custo_diario = db.Column(db.Numeric(
        19, 2), default=Decimal('0.00'), nullable=False)
    capacidade_pessoas = db.Column(db.Integer(), default=0, nullable=False)
    quantidade_alugueis = db.Column(db.Integer(), default=0)
    data_de_insercao = db.Column(db.DateTime(), default=datetime.utcnow)

    def isDisponivel(self):
        def comparar_datas(aluguel):
            return (aluguel.inicio_aluguel.date() <= datetime.today().date()) and (aluguel.final_aluguel.date() >= datetime.today().date())
        if self.alugueis and len(self.alugueis) > 0:
            alugueisf = filter(comparar_datas, self.alugueis)
            isDisponivelVar = not (len(list(alugueisf)) > 0)
            return isDisponivelVar
        return True

    def getProxDataDisponivel(self):
        alugueisByDataFinal = sorted(
            self.alugueis, key=lambda x: x.final_aluguel, reverse=True)
        if alugueisByDataFinal and len(alugueisByDataFinal) > 0:
            return alugueisByDataFinal[0].final_aluguel
        return None

    def detectar_overlap(self, data_inicio_1, data_fim_1):
        for aluguel in self.alugueis:
            if data_inicio_1 <= aluguel.final_aluguel.date() and aluguel.inicio_aluguel.date() <= data_fim_1:
                return True
        return False


class Aluguel(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    inicio_aluguel = db.Column(
        db.DateTime(), nullable=False, default=datetime.utcnow)
    final_aluguel = db.Column(db.DateTime(), nullable=False)
    total_pagar = db.Column(db.Numeric(
        19, 2), default=Decimal('0.00'), nullable=False)
    forma_pagamento = db.Column(db.String(3))
    carro = db.relationship('Carro', back_populates="alugueis")
    user = db.relationship('User', back_populates="alugueis")
    carro_id = db.Column(db.Integer(), db.ForeignKey('carro.id'), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)


class User(db.Model, FsUserMixin):
    cpf = db.Column(db.String(14), unique=True)
    celular = db.Column(db.String(15), unique=True)
    data_cadastro = db.Column(
        db.DateTime(), default=datetime.utcnow)
    alugueis = db.relationship("Aluguel", back_populates="user")

    @staticmethod
    def checar_celular_ja_cadastrados(celular):
        celularDb = db.session.query(User).filter(
            User.celular == celular).first()
        return (celularDb is not None)

    @staticmethod
    def checar_cpf_ja_cadastrados(cpf):
        cpfDb = db.session.query(User).filter(User.cpf == cpf).first()
        return (cpfDb is not None)

    def adicionar_permissao_seus_alugueis(self):
        seus_alugueis_role = security.datastore.find_or_create_role(
            name='Seus alugueis', page_url='seusalugueis', description='Cargo que habilita a consulta de seus alugueis realizados', permissions=['USER_SEUS_ALUGUEIS'])
        if seus_alugueis_role not in self.roles:
            self.roles.append(seus_alugueis_role)
            db.session.merge(self)


class Role(db.Model, FsRoleMixin):
    page_url = db.Column(db.String(80))
    pass
