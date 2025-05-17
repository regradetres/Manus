from flask import Blueprint

bp = Blueprint('producao', __name__, url_prefix='/producao')

from app.producao import routes
