from flask_security import current_user, login_required, login_user, logout_user, permissions_required
from app import app
from src.extensions import login_manager, db, security
from flask import flash, redirect, render_template, request, url_for
from excepts.ErroDeAutenticacao import ErroDeAutenticacao
from src.orm import Carro
from werkzeug.security import generate_password_hash, check_password_hash


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


@app.route("/carro", methods=['POST', 'GET'])
@login_required
@permissions_required('ADMIN_CARRO_CRUD')
def carro():
    if request.method == 'GET':
        carros = db.session.execute(db.select(Carro)).scalars()
        return render_template("carro.html", carros=carros)
    elif request.method == 'POST':
        msg = ("Carro cadastrado com sucesso!", 'primary')
        try:
            f = request.form
            novoCarro = Carro(
                modelo=f['modelo'],
                placa=f['placa'],
                descricao=f['descricao'],
                url_imagem=f['url_imagem'],
                descricao_imagem=f['descricao_imagem'])
            db.session.add(novoCarro)
            db.session.commit()
        except:
            msg = ("Erro inesperado, tente novamente!", 'danger')
        flash(message=msg[0], category=msg[1])
        carros = db.session.execute(db.select(Carro)).scalars()
    return render_template("carro.html", carros=carros)


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
        flash(message=f'404 - Não encontramos o carro com o código {id_carro}!',
              category='warning')
        return redirect(url_for('aluguel'))
    if request.method == 'GET':
        return render_template("aluguel_especifico.html", carro=carro)
    elif request.method == 'POST':
        return render_template("aluguel_especifico.html", carro=carro)


@app.errorhandler(404)
def page_not_found(e):
    flash(message='404 - Não encontramos a tela que você tentou acessar!',
          category='warning')
    return redirect(url_for('index'))


@app.errorhandler(403)
def page_not_found(e):
    flash(message='Você não tem acesso a esta funcionalidade!',
          category='danger')
    return redirect(url_for('index'))


@login_manager.unauthorized_handler
def acesso_nao_autorizado():
    flash(message=f'Faça login para poder acessar esta página.',
          category='warning')
    return redirect(url_for('login'))


@app.route("/map")
def rotas():
    print(app.url_map)
    return redirect(url_for('index'))
