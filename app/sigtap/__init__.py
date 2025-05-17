from flask import Blueprint

bp = Blueprint('sigtap', __name__, url_prefix='/sigtap')

from app.sigtap import routes
