import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-padrao-mudar-em-producao'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    
    # Configurações de email para notificações
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['admin@example.com']
    
    # Configurações específicas da aplicação
    SIGTAP_UPLOAD_FOLDER = os.path.join(basedir, 'uploads', 'sigtap')
    EXPORT_FOLDER = os.path.join(basedir, 'exports')
    
    @staticmethod
    def init_app(app):
        # Inicializações específicas da aplicação
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)
        if not os.path.exists(Config.SIGTAP_UPLOAD_FOLDER):
            os.makedirs(Config.SIGTAP_UPLOAD_FOLDER)
        if not os.path.exists(Config.EXPORT_FOLDER):
            os.makedirs(Config.EXPORT_FOLDER)

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'dev-app.db')

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'  # Usa banco de dados em memória
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://sistema_sus:senha_segura@localhost/sistema_sus_db'
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Configurações específicas de produção
        import logging
        from logging.handlers import RotatingFileHandler
        
        # Configura log para stdout se estiver em ambiente de container
        if os.environ.get('LOG_TO_STDOUT'):
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            # Configura log para arquivo
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/sistema_sus.log', 
                                              maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Sistema de Produção SUS inicializado')

# Configuração para Railway.app
class RailwayConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)
        
        # Configura proxy para Railway
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
    'railway': RailwayConfig,
    'default': DevelopmentConfig
}
