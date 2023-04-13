from flask_login import current_user, login_required, login_user, logout_user
from app import app, db, login_manager
from flask import flash, redirect, render_template, request, url_for
from excepts.ErroDeAutenticacao import ErroDeAutenticacao
from src.orm import Carro, Usuario


@login_manager.user_loader
def carregar_usuario(id_usuario):
    return db.session.execute(db.select(Usuario).filter_by(id=int(id_usuario))).scalar_one()


@app.route("/")
def base():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return redirect(url_for('index'))


@app.route("/index")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        msg = ("Erro inesperado, tente novamente!", 'danger')
        page_return = 'login'
        try:
            f = request.form
            usuarioTentandoLogar = db.session.execute(
                db.select(Usuario).filter_by(email=f['email'])).scalar_one()
            if usuarioTentandoLogar is None:
                raise ErroDeAutenticacao
            else:
                if usuarioTentandoLogar.senha == f['pswd']:
                    login_user(usuarioTentandoLogar)
                    msg = ("Login realizado com sucesso!", 'primary')
                    page_return = 'index'
                else:
                    raise ErroDeAutenticacao
        except ErroDeAutenticacao:
            msg = ("Email ou senha errados!", 'danger')
        except:
            msg = ("Erro inesperado, tente novamente!", 'danger')
        flash(message=msg[0], category=msg[1])
        return redirect(url_for(page_return))


@app.route("/cadastro", methods=['POST', 'GET'])
def cadastro():
    if request.method == 'GET':
        return render_template("cadastro.html")
    elif request.method == 'POST':
        msg = ("Usuario cadastrado com sucesso!", 'primary')
        page_return = ''
        try:
            f = request.form
            novoUsuario = Usuario(
                email=f['email'], senha=f['pswd'], nome=f['nome'])
            db.session.add(novoUsuario)
            db.session.commit()
            page_return = 'login'
        except:
            msg = ("Email já cadastrado!", 'danger')
            page_return = 'cadastro'
        flash(message=msg[0], category=msg[1])
        return redirect(url_for(page_return))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(message='Usuario deslogado com sucesso!', category='primary')
    return redirect(url_for('login'))


@app.route("/carro", methods=['POST', 'GET'])
@login_required
def carro():
    if request.method == 'GET':
        carros = db.session.execute(db.select(Carro)).scalars()
        return render_template("carro.html", carros=carros)
    elif request.method == 'POST':
        msg = ("Carro cadastrado com sucesso!", 'primary')
        try:
            f = request.form
            novoCarro = Carro(
                modelo=f['modelo'], placa=f['placa'])
            db.session.add(novoCarro)
            db.session.commit()
        except:
            msg = ("Erro inesperado, tente novamente!", 'danger')
        flash(message=msg[0], category=msg[1])
        carros = db.session.execute(db.select(Carro)).scalars()
        return render_template("carro.html", carros=carros)


@app.errorhandler(404)
def page_not_found(e):
    flash(message='404 - Não encontramos a tela que você tentou acessar!',
          category='warning')
    return redirect(url_for('index'))


@login_manager.unauthorized_handler
def acesso_nao_autorizado():
    flash(message=f'Faça login para poder acessar esta página.',
        category='warning')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
