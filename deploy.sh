#!/bin/bash
# Script de implantação para o Sistema de Produção SUS
# Este script configura o ambiente e inicia a aplicação

# Verifica se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python 3 não encontrado. Por favor, instale o Python 3.11 ou superior."
    exit 1
fi

# Verifica se o PostgreSQL está instalado
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL não encontrado. Por favor, instale o PostgreSQL 14 ou superior."
    exit 1
fi

# Cria e ativa o ambiente virtual
echo "Criando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate

# Instala as dependências
echo "Instalando dependências..."
pip install -r requirements.txt

# Verifica se o arquivo .env existe
if [ ! -f .env ]; then
    echo "Arquivo .env não encontrado. Criando arquivo de exemplo..."
    cat > .env << EOF
FLASK_APP=app
FLASK_ENV=production
SECRET_KEY=chave_secreta_para_producao_alterar
DATABASE_URL=postgresql://sistema_sus:senha_segura@localhost/sistema_sus_db
EOF
    echo "Por favor, edite o arquivo .env com as configurações corretas."
    exit 1
fi

# Executa as migrações do banco de dados
echo "Executando migrações do banco de dados..."
flask db upgrade

# Verifica se existe um usuário administrador
echo "Verificando usuário administrador..."
python3 -c "
from app import create_app, db
from app.models import User
app = create_app()
with app.app_context():
    admin = User.query.filter_by(perfil='admin').first()
    if not admin:
        print('Criando usuário administrador padrão...')
        admin = User(username='admin', email='admin@example.com', nome_completo='Administrador', perfil='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('Usuário admin criado com senha admin123. Por favor, altere a senha após o primeiro login.')
    else:
        print('Usuário administrador já existe.')
"

# Inicia a aplicação
echo "Iniciando a aplicação..."
if [ "$FLASK_ENV" = "production" ]; then
    echo "Ambiente de produção detectado. Iniciando com Gunicorn..."
    if ! command -v gunicorn &> /dev/null; then
        echo "Gunicorn não encontrado. Instalando..."
        pip install gunicorn
    fi
    gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
else
    echo "Ambiente de desenvolvimento detectado. Iniciando com Flask..."
    flask run --host=0.0.0.0
fi
