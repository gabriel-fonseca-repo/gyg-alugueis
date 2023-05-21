from flask_security import current_user, login_user, logout_user
from app import app
from src.extensions import db, login_manager, security
from flask import flash, redirect, render_template, request, url_for
from excepts.ErroDeAutenticacao import ErroDeAutenticacao
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def carregar_usuario(id_usuario):
    return security.datastore.find_user(fs_uniquifier=id_usuario)


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        msg = ("Erro inesperado, tente novamente!", 'danger')
        page_return = 'login'
        try:
            f = request.form
            usuarioTentandoLogar = security.datastore.find_user(
                email=f['email'])
            if usuarioTentandoLogar is None:
                raise ErroDeAutenticacao('Email não cadastrado ou com erro!')
            else:
                if check_password_hash(usuarioTentandoLogar.password, f['pswd']):
                    login_user(usuarioTentandoLogar)
                    msg = ("Login realizado com sucesso!", 'primary')
                    page_return = 'index'
                else:
                    raise ErroDeAutenticacao('Senha errada!')
        except ErroDeAutenticacao as error:
            msg = (error.args[0], 'danger')
        flash(message=msg[0], category=msg[1])
        return redirect(url_for(page_return))


@app.route("/cadastro", methods=['POST', 'GET'])
def cadastro():
    if request.method == 'GET':
        if current_user is not None and current_user.is_authenticated:
            flash(message='Dê logout antes de criar uma nova conta!',
                  category='primary')
            return redirect(url_for('index'))
        return render_template("cadastro.html")
    elif request.method == 'POST':
        msg = ("Usuario cadastrado com sucesso!", 'primary')
        page_return = ''
        try:
            f = request.form
            std_role = security.datastore.find_or_create_role(
                name='Aluguel', page_url='aluguel', description='Cargo que habilita o aluguel de carros.', permissions=['USER_ALUGUEL_CRUD'])
            security.datastore.create_user(email=f['email'], password=generate_password_hash(
                f['pswd']), username=f['nome'], roles=[std_role])
            page_return = 'login'
            db.session.commit()
        except:
            msg = ("Email já cadastrado!", 'danger')
            page_return = 'cadastro'
        flash(message=msg[0], category=msg[1])
        return redirect(url_for(page_return))


@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    flash(message='Usuario deslogado com sucesso!', category='primary')
    return redirect(url_for('login'))
