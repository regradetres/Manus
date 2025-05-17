from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

# Inicialização das extensões
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config=None):
    """Função factory para criar a aplicação Flask"""
    app = Flask(__name__, instance_relative_config=True)
    
    # Configuração padrão
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev_key_insegura'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///app.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    
    # Carrega configuração específica se fornecida
    if config:
        app.config.from_mapping(config)
    
    # Inicializa extensões com a aplicação
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Garante que o diretório de instância existe
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
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
    
    # Rota de teste
    @app.route('/teste')
    def teste():
        return 'Sistema de Produção SUS funcionando!'
    
    return app
