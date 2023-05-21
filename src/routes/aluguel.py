import re
from datetime import datetime
from flask_security import login_required, current_user, permissions_required
from sqlalchemy import and_, func
from app import app
from src.extensions import db
from flask import flash, redirect, render_template, request, session, url_for
from src.orm import Aluguel, Carro, User


@app.route("/aluguel")
@login_required
def aluguel():
    return render_template("aluguel.html", carros=filtrar_consulta())


@app.route("/seusalugueis")
@login_required
@permissions_required('USER_SEUS_ALUGUEIS')
def seusalugueis():
    return render_template("seusalugueis.html", alugueis=filtrar_consulta_alugueis())


@app.route("/aluguel/<int:id_carro>", methods=['POST', 'GET'])
@login_required
def aluguel_especifico(id_carro):
    carro = db.session.execute(
        db.select(Carro).filter_by(id=int(id_carro))).scalar()
    if carro is None:
        flash(message=f'Não encontramos o carro com o código {id_carro}!',
              category='warning')
        return redirect(url_for('aluguel'))
    if not carro.isDisponivel():
        flash(message=f'Esse carro já está alugado!', category='warning')
        return redirect(url_for('aluguel'))
    if request.method == 'GET':
        return render_template("aluguel_especifico.html", carro=carro)
    elif request.method == 'POST':
        return render_template("aluguel_especifico.html", carro=carro)


@app.route("/alugar", methods=['POST'])
@login_required
def alugar():
    page_return = 'aluguel'
    form_data = request.form.to_dict()
    try:
        carro_id = form_data.get('carro_id')
        cpf = form_data.get('cpf')
        celular = form_data.get('celular')
        inicio_aluguel = form_data.get('inicio_aluguel')
        final_aluguel = form_data.get('final_aluguel')
        dt_ini = datetime.strptime(inicio_aluguel, '%Y-%m-%d').date()
        dt_fim = datetime.strptime(final_aluguel, '%Y-%m-%d').date()
        inicio_maior_que_fim = dt_fim - dt_ini
        inicio_antes_de_hoje = dt_ini < datetime.today().date()

        carro = db.session.execute(
            db.select(Carro).filter_by(id=int(carro_id))).scalar()

        if cpf and not validate(cpf):
            flash("CPF inserido é inválido!", 'danger')
        if inicio_antes_de_hoje:
            flash("Você não pode alugar o carro no passado, bobinho!", 'warning')
        if cpf and User.checar_cpf_ja_cadastrados(cpf):
            flash("Este CPF já está cadastrado.", 'warning')
        if celular and User.checar_celular_ja_cadastrados(celular):
            flash("Este Celular já está cadastrado.", 'warning')
        if not carro:
            flash(f"Carro de código {carro_id} não encontrado!", 'danger')
        if carro and carro.detectar_overlap(dt_ini, dt_fim):
            flash("Esse carro estará alugado neste intervalo de tempo!", 'warning')
        if inicio_maior_que_fim.days < 1:
            flash(
                "A data de finalização não pode ser menor que a data de início do aluguel!", 'danger')

        mensagens = session['_flashes'] if '_flashes' in session else []
        if mensagens and len(mensagens) > 0:
            return redirect(f'/aluguel/{carro_id}')

        current_user.cpf = cpf if cpf else current_user.cpf
        current_user.celular = celular if celular else current_user.celular

        db.session.merge(current_user)
        aluguel = Aluguel(user=current_user, user_id=current_user.id,
                          carro=carro, carro_id=carro_id, inicio_aluguel=dt_ini, final_aluguel=dt_fim, forma_pagamento=form_data.get(
                              'forma_pagamento'), total_pagar=carro.custo_diario*inicio_maior_que_fim.days)
        db.session.add(aluguel)
        current_user.adicionar_permissao_seus_alugueis()
        db.session.commit()
        page_return = 'aluguel'
        flash(
            "Carro alugado com sucesso!", 'primary')
    except:
        flash("Erro inesperado. Contate o administrador do sistema.", 'danger')
    return redirect(url_for(page_return))


def filtrar_consulta_alugueis():
    query_params = request.args.to_dict()
    valores_igualdade = ('capacidade_pessoas', 'total_pagar')
    filters = []
    for key, value in query_params.items():
        if hasattr(Carro, key) and (value):
            if key in valores_igualdade:
                filters.append(getattr(Carro, key) == value)
            else:
                filters.append(getattr(Carro, key).ilike(f'%{value}%'))
        if hasattr(Aluguel, key) and (value):
            if key in valores_igualdade:
                filters.append(getattr(Aluguel, key) == value)
            elif key == 'inicio_aluguel':
                date = datetime.strptime(value, '%Y-%m-%d').date()
                filters.append(func.DATE(Aluguel.inicio_aluguel) >= date)
            elif key == 'final_aluguel':
                date = datetime.strptime(value, '%Y-%m-%d').date()
                filters.append(func.DATE(Aluguel.final_aluguel) <= date)
            else:
                filters.append(getattr(Aluguel, key).ilike(f'%{value}%'))
    return Aluguel.query.join(Carro).filter(and_(*filters)).all()


@app.route("/aluguel/del/<int:id_aluguel>", methods=['GET'])
@login_required
@permissions_required('USER_SEUS_ALUGUEIS')
def aluguel_delete(id_aluguel):
    if (id_aluguel is not None and id_aluguel) and (isinstance(id_aluguel, int)):
        carro_a_deletar = Aluguel.query.get(id_aluguel)
        if carro_a_deletar is not None:
            db.session.delete(carro_a_deletar)
            db.session.commit()
    return redirect(url_for('seusalugueis'))


def filtrar_consulta():
    query_params = request.args.to_dict()
    valores_igualdade = ('capacidade_pessoas')
    filters = []
    for key, value in query_params.items():
        if hasattr(Carro, key) and (value is not None and value):
            if key in valores_igualdade:
                filters.append(getattr(Carro, key) == value)
            else:
                filters.append(getattr(Carro, key).ilike(f'%{value}%'))
    return Carro.query.filter(and_(*filters)).all()


def validate(cpf: str) -> bool:
    if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
        return False
    numbers = [int(digit) for digit in cpf if digit.isdigit()]
    if len(numbers) != 11 or len(set(numbers)) == 1:
        return False
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return False
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False
    return True
