#!/bin/bash
# Script para preparar e iniciar a aplicação em ambiente de produção

# Configurações
export FLASK_APP=app
export FLASK_ENV=production
export LOG_TO_STDOUT=1

# Instala dependências
pip install -r requirements.txt

# Executa migrações do banco de dados
flask db upgrade

# Inicia a aplicação com Gunicorn
gunicorn "app:create_app('railway')" --bind 0.0.0.0:$PORT --workers 4 --log-file=-
