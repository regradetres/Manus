from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Por favor, faça login para acessar esta página.'
login.login_message_category = 'info'

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    
    # Registra blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.sigtap import bp as sigtap_bp
    app.register_blueprint(sigtap_bp)
    
    from app.producao import bp as producao_bp
    app.register_blueprint(producao_bp)
    
    from app.exportacao import bp as exportacao_bp
    app.register_blueprint(exportacao_bp)
    
    # Configura manipuladores de erro
    from app.errors import register_error_handlers
    register_error_handlers(app)
    
    # Configura comandos CLI
    from app.cli import register_commands
    register_commands(app)
    
    # Configura contexto de shell
    @app.shell_context_processor
    def make_shell_context():
        from app.models import User, ProcedimentoSIGTAP, ProducaoSUS, BPA, RAAS, AIH, Exportacao
        return {
            'db': db, 
            'User': User, 
            'ProcedimentoSIGTAP': ProcedimentoSIGTAP,
            'ProducaoSUS': ProducaoSUS,
            'BPA': BPA,
            'RAAS': RAAS,
            'AIH': AIH,
            'Exportacao': Exportacao
        }
    
    return app

from app import models
