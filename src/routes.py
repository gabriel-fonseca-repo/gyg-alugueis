from app import app, db
from flask import flash, redirect, render_template, request, session, url_for
from excepts.ErroDeAutenticacao import ErroDeAutenticacao
from orm.Usuario import Usuario


@app.route("/")
def base():
    if session.get('usuario') is None:
        return redirect(url_for('login'))
    return redirect(url_for('index'))


@app.route("/index")
def index():
    if session.get('usuario') is None:
        return redirect(url_for('login'))
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
                    session['usuario'] = usuarioTentandoLogar
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


@app.errorhandler(404)
def page_not_found(e):
    flash(message='404 - Não encontramos a tela que você tentou acessar!',
          category='warning')
    return redirect(url_for('index'))


@app.route("/logout")
def logout():
    if session.get('usuario') is not None:
        session.clear()
    flash(message='Usuario deslogado com sucesso!', category='primary')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()