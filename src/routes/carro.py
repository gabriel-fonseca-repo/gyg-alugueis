from datetime import datetime
from flask_security import login_required, permissions_required
from sqlalchemy import and_, cast, func
from app import app
from src.extensions import db
from flask import flash, redirect, render_template, request, url_for
from src.orm import Carro


@app.route("/carro", methods=['GET', 'POST'])
@login_required
@permissions_required('ADMIN_CARRO_CRUD')
def carro():
    if request.method == 'POST':
        msg = None
        try:
            form_data = request.form.to_dict()
            if form_data.get('id'):
                db.session.merge(Carro(**form_data))
                msg = ("Carro editado com sucesso!", 'primary')
            else:
                if 'id' in form_data:
                    form_data.pop('id')
                db.session.add(Carro(**form_data))
                msg = ("Carro cadastrado com sucesso!", 'primary')
            db.session.commit()
        except:
            msg = ("Erro inesperado, tente novamente!", 'danger')
        flash(message=msg[0], category=msg[1])
    return render_template("carro.html", carros=filtrar_consulta())


@app.route("/carro/del/<int:id_carro>", methods=['GET'])
@login_required
@permissions_required('ADMIN_CARRO_CRUD')
def carro_delete(id_carro):
    if (id_carro is not None and id_carro) and (isinstance(id_carro, int)):
        carro_a_deletar = Carro.query.get(id_carro)
        if carro_a_deletar is not None:
            db.session.delete(carro_a_deletar)
            db.session.commit()
    return redirect(url_for('carro'))


def filtrar_consulta():
    query_params = request.args.to_dict()
    valores_igualdade = ('id', 'custo_diario', 'capacidade_pessoas',
                         'quantidade_alugueis')
    filters = []
    for key, value in query_params.items():
        if hasattr(Carro, key) and (value is not None and value):
            if key in valores_igualdade:
                filters.append(getattr(Carro, key) == value)
            elif key == 'data_de_insercao':
                date = datetime.strptime(value, '%Y-%m-%d').date()
                filters.append(func.DATE(Carro.data_de_insercao) == date)
            else:
                filters.append(getattr(Carro, key).ilike(f'%{value}%'))
    return Carro.query.filter(and_(*filters)).all()
