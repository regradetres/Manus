from flask import render_template, redirect, url_for, flash, request
from app.main import bp
from flask_login import login_required, current_user

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    """Rota principal que exibe o dashboard do sistema"""
    return render_template('main/index.html', title='Dashboard')

@bp.route('/sobre')
def sobre():
    """Página sobre o sistema"""
    return render_template('main/sobre.html', title='Sobre o Sistema')
