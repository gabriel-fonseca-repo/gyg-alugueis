from app import app
from src.extensions import login_manager
from flask import flash, redirect, url_for

@app.errorhandler(404)
def page_not_found(e):
    flash(message='Não encontramos a tela que você tentou acessar!',
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