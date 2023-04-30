from flask_security import current_user, login_required, login_user, logout_user, permissions_required
from app import app
from src.extensions import login_manager, db, security
from flask import flash, redirect, render_template, request, url_for
from excepts.ErroDeAutenticacao import ErroDeAutenticacao
from src.orm import Carro
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/aluguel", methods=['POST', 'GET'])
@login_required
def aluguel():
    if request.method == 'GET':
        carros = db.session.execute(db.select(Carro)).scalars()
        return render_template("aluguel.html", carros=carros)
    elif request.method == 'POST':
        return render_template("aluguel.html")


@app.route("/aluguel/<int:id_carro>", methods=['POST', 'GET'])
@login_required
def aluguel_especifico(id_carro):
    carro = db.session.execute(
        db.select(Carro).filter_by(id=int(id_carro))).scalar()
    if carro is None:
        flash(message=f'Não encontramos o carro com o código {id_carro}!',
              category='warning')
        return redirect(url_for('aluguel'))
    if request.method == 'GET':
        return render_template("aluguel_especifico.html", carro=carro)
    elif request.method == 'POST':
        return render_template("aluguel_especifico.html", carro=carro)