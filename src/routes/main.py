from flask_security import current_user, login_required
from app import app
from flask import redirect, render_template, url_for


@app.route("/")
def base():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return redirect(url_for('index'))


@app.route("/index")
@login_required
def index():
    return render_template("index.html")


@app.route("/map")
def rotas():
    print(app.url_map)
    return redirect(url_for('index'))
