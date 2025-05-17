# Documentação Técnica - Sistema de Produção SUS

## Visão Geral

O Sistema de Produção SUS é uma aplicação web desenvolvida para auxiliar técnicos e digitadores de secretarias de saúde na geração de arquivos válidos de produção ambulatorial e hospitalar do SUS (BPA, FPO, RAAS e AIH), com base na tabela SIGTAP.

Esta documentação técnica destina-se a desenvolvedores e administradores de sistemas que precisam entender a arquitetura, implementação e manutenção do sistema.

## Arquitetura

O sistema foi desenvolvido seguindo uma arquitetura em camadas, utilizando o padrão MVC (Model-View-Controller), com as seguintes tecnologias:

- **Backend**: Python 3.11+ com Flask 3.1+
- **ORM**: SQLAlchemy 2.0+ com Flask-SQLAlchemy
- **Banco de Dados**: PostgreSQL 14+
- **Frontend**: HTML5, CSS3, JavaScript com Bootstrap 5
- **Autenticação**: Flask-Login
- **Migrações**: Flask-Migrate (Alembic)

### Estrutura de Diretórios

```
sistema_sus/
├── app/                    # Código principal da aplicação
│   ├── __init__.py         # Inicialização da aplicação Flask
│   ├── models.py           # Modelos de dados (SQLAlchemy)
│   ├── auth/               # Módulo de autenticação
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── main/               # Módulo principal (dashboard)
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── sigtap/             # Módulo de importação SIGTAP
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── producao/           # Módulo de produção SUS
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── exportacao/         # Módulo de exportação DATASUS
│   │   ├── __init__.py
│   │   └── routes.py
│   └── templates/          # Templates HTML (Jinja2)
│       ├── base.html
│       ├── auth/
│       ├── main/
│       ├── sigtap/
│       ├── producao/
│       └── exportacao/
├── config.py               # Configurações da aplicação
├── tests/                  # Testes automatizados
│   ├── unit/
│   └── integration/
├── migrations/             # Migrações de banco de dados
├── .env                    # Variáveis de ambiente (não versionado)
├── requirements.txt        # Dependências do projeto
└── run.py                  # Script para iniciar a aplicação
```

## Modelos de Dados

O sistema utiliza os seguintes modelos principais:

### User

Representa os usuários do sistema, com diferentes perfis de acesso.

```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    nome_completo = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    perfil = db.Column(db.String(20), nullable=False, default='digitador')
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_acesso = db.Column(db.DateTime)
```

### ProcedimentoSIGTAP

Armazena os procedimentos importados da tabela SIGTAP.

```python
class ProcedimentoSIGTAP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), index=True, unique=True, nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    grupo = db.Column(db.String(2))
    subgrupo = db.Column(db.String(2))
    forma_organizacao = db.Column(db.String(2))
    complexidade = db.Column(db.String(20))
    sexo = db.Column(db.String(1))
    idade_minima = db.Column(db.Integer)
    idade_maxima = db.Column(db.Integer)
    valor = db.Column(db.Float)
    competencia_inicio = db.Column(db.String(6))
    competencia_fim = db.Column(db.String(6))
```

### ProducaoSUS

Modelo base para registros de produção, com herança para tipos específicos.

```python
class ProducaoSUS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10), nullable=False)
    competencia = db.Column(db.String(6), nullable=False)
    cnes = db.Column(db.String(7), nullable=False)
    cns_profissional = db.Column(db.String(15), nullable=False)
    cbo = db.Column(db.String(6), nullable=False)
    cns_paciente = db.Column(db.String(15))
    data_atendimento = db.Column(db.Date, nullable=False)
    procedimento_id = db.Column(db.Integer, db.ForeignKey('procedimento_sigtap.id'), nullable=False)
    procedimento = db.relationship('ProcedimentoSIGTAP', backref='producoes')
    quantidade = db.Column(db.Integer, default=1)
    valor_calculado = db.Column(db.Float)
    status = db.Column(db.String(20), default='pendente')
    observacoes = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    usuario = db.relationship('User', backref='producoes')
```

### Exportacao

Registra as exportações de arquivos realizadas.

```python
class Exportacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10), nullable=False)
    competencia = db.Column(db.String(6), nullable=False)
    nome_arquivo = db.Column(db.String(255), nullable=False)
    caminho_arquivo = db.Column(db.String(255), nullable=False)
    quantidade_registros = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='gerado')
    data_geracao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    usuario = db.relationship('User', backref='exportacoes')
```

## Módulos Principais

### Autenticação (auth)

Gerencia o login, logout e registro de usuários, com controle de acesso baseado em perfis.

### SIGTAP (sigtap)

Responsável pela importação e consulta da tabela SIGTAP, permitindo:
- Upload do arquivo ZIP oficial
- Processamento e importação para o banco de dados
- Consulta de procedimentos com filtros avançados
- Visualização detalhada de procedimentos

### Produção (producao)

Gerencia o cadastro e validação de produção ambulatorial e hospitalar:
- Cadastro de BPA, RAAS e AIH
- Validação de dados contra regras do DATASUS
- Listagem e edição de registros
- Controle de status (pendente, validado, rejeitado, exportado)

### Exportação (exportacao)

Responsável pela geração de arquivos no formato exigido pelo DATASUS:
- Configuração de parâmetros de exportação
- Geração de arquivos TXT com layout fixo
- Histórico de exportações
- Download de arquivos gerados

## Configuração e Implantação

### Requisitos

- Python 3.11+
- PostgreSQL 14+
- Bibliotecas Python listadas em requirements.txt

### Variáveis de Ambiente

O sistema utiliza as seguintes variáveis de ambiente, que devem ser definidas no arquivo `.env`:

```
FLASK_APP=app
FLASK_ENV=development|production
SECRET_KEY=chave_secreta_para_sessoes
DATABASE_URL=postgresql://usuario:senha@host/banco
```

### Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/regradetres/Manus.git
   cd Manus
   ```

2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configure o banco de dados PostgreSQL:
   ```
   sudo -u postgres psql
   CREATE USER sistema_sus WITH PASSWORD 'senha_segura';
   CREATE DATABASE sistema_sus_db OWNER sistema_sus;
   GRANT ALL PRIVILEGES ON DATABASE sistema_sus_db TO sistema_sus;
   ```

5. Configure as variáveis de ambiente no arquivo `.env`

6. Execute as migrações:
   ```
   flask db upgrade
   ```

7. Crie um usuário administrador:
   ```
   flask shell
   >>> from app import db
   >>> from app.models import User
   >>> u = User(username='admin', email='admin@example.com', nome_completo='Administrador', perfil='admin')
   >>> u.set_password('senha_admin')
   >>> db.session.add(u)
   >>> db.session.commit()
   >>> exit()
   ```

8. Inicie a aplicação:
   ```
   flask run
   ```

### Implantação em Produção

Para implantação em ambiente de produção, recomenda-se:

1. Utilizar um servidor WSGI como Gunicorn ou uWSGI
2. Configurar um proxy reverso como Nginx ou Apache
3. Utilizar HTTPS com certificado SSL
4. Configurar backups regulares do banco de dados
5. Definir uma política de rotação de logs

Exemplo de configuração com Gunicorn e Nginx:

```bash
# Instalação do Gunicorn
pip install gunicorn

# Execução com Gunicorn
gunicorn -w 4 -b 127.0.0.1:8000 "app:create_app()"
```

Configuração Nginx:

```nginx
server {
    listen 80;
    server_name seu_dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Testes

O sistema inclui testes unitários e de integração, organizados nos diretórios `tests/unit` e `tests/integration`.

Para executar os testes:

```bash
# Todos os testes
python -m unittest discover

# Testes unitários
python -m unittest discover tests/unit

# Testes de integração
python -m unittest discover tests/integration
```

## Manutenção e Suporte

### Logs

O sistema gera logs detalhados que podem ser utilizados para diagnóstico de problemas:

- Logs de aplicação: registram erros, avisos e informações sobre o funcionamento do sistema
- Logs de auditoria: registram ações dos usuários, como login, cadastro, alteração e exclusão de registros

### Backup

Recomenda-se realizar backups regulares do banco de dados:

```bash
pg_dump -U sistema_sus sistema_sus_db > backup_$(date +%Y%m%d).sql
```

### Atualização da Tabela SIGTAP

A tabela SIGTAP deve ser atualizada mensalmente, seguindo o calendário de publicação do Ministério da Saúde:

1. Baixe o arquivo ZIP da tabela SIGTAP do site oficial do DATASUS
2. Acesse o sistema com perfil de administrador
3. Navegue até o módulo SIGTAP > Importar
4. Faça upload do arquivo ZIP
5. Aguarde o processamento e verifique os resultados

## Considerações de Segurança

- Todas as senhas são armazenadas com hash seguro (Werkzeug)
- Autenticação e autorização são implementadas em todas as rotas
- Validação de entrada em todos os formulários
- Proteção contra CSRF em todos os formulários
- Sanitização de dados antes da geração de arquivos
- Logs de auditoria para rastreabilidade

## Extensões e Melhorias Futuras

- Integração com APIs do CADSUS para validação de CNS
- Implementação de autenticação de dois fatores
- Geração de relatórios estatísticos avançados
- Integração com sistemas de prontuário eletrônico
- Envio automático de arquivos para o DATASUS
- Aplicativo móvel para consulta e validação

## Suporte Técnico

Para suporte técnico, entre em contato com:

- Email: suporte@exemplo.com
- Telefone: (00) 1234-5678
- Horário de atendimento: Segunda a sexta, das 8h às 18h
