from app import app, db
from flask import flash, redirect, render_template, request, url_for
from orm.Usuario import Usuario
from psycopg2.errors import UniqueViolation


@app.route("/")
def index():
    return redirect(url_for('login'))


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        return render_template("login.html")


@app.route("/cadastro", methods=['POST', 'GET'])
def cadastro():
    if request.method == 'GET':
        return render_template("cadastro.html")
    elif request.method == 'POST':
        msg = "Usuario cadastrado com sucesso!"
        try:
            f = request.form
            novoUsuario = Usuario(
                email=f['email'], senha=f['pswd'], nome=f['nome'])
            db.session.add(novoUsuario)
            db.session.commit()
        except UniqueViolation:
            msg = "Email já cadastrado!"
        except:
            msg = "Algum erro inesperado aconteceu!"
        flash(msg)
        return render_template("cadastro.html")


if __name__ == '__main__':
    app.run()
