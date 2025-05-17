from flask import Blueprint

bp = Blueprint('exportacao', __name__, url_prefix='/exportacao')

from app.exportacao import routes
