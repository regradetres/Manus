from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    """Modelo para usuários do sistema"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    nome_completo = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    perfil = db.Column(db.String(20), nullable=False, default='digitador')
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_acesso = db.Column(db.DateTime)
    
    @property
    def is_admin(self):
        return self.perfil == 'admin'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class ProcedimentoSIGTAP(db.Model):
    """Modelo para procedimentos importados da tabela SIGTAP"""
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), index=True, unique=True, nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    grupo = db.Column(db.String(2))
    subgrupo = db.Column(db.String(2))
    forma_organizacao = db.Column(db.String(2))
    complexidade = db.Column(db.String(20))
    sexo = db.Column(db.String(1))  # M, F ou N (não aplicável)
    idade_minima = db.Column(db.Integer)
    idade_maxima = db.Column(db.Integer)
    valor = db.Column(db.Float)
    competencia_inicio = db.Column(db.String(6))  # AAAAMM
    competencia_fim = db.Column(db.String(6))  # AAAAMM ou null para vigente
    
    def __repr__(self):
        return f'<Procedimento {self.codigo} - {self.nome}>'

class ProducaoSUS(db.Model):
    """Modelo base para registros de produção SUS"""
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10), nullable=False)  # BPA, FPO, RAAS, AIH
    competencia = db.Column(db.String(6), nullable=False)  # AAAAMM
    cnes = db.Column(db.String(7), nullable=False)
    cns_profissional = db.Column(db.String(15), nullable=False)
    cbo = db.Column(db.String(6), nullable=False)
    cns_paciente = db.Column(db.String(15))
    data_atendimento = db.Column(db.Date, nullable=False)
    procedimento_id = db.Column(db.Integer, db.ForeignKey('procedimento_sigtap.id'), nullable=False)
    procedimento = db.relationship('ProcedimentoSIGTAP', backref='producoes')
    quantidade = db.Column(db.Integer, default=1)
    valor_calculado = db.Column(db.Float)
    status = db.Column(db.String(20), default='pendente')  # pendente, validado, rejeitado, exportado
    observacoes = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    usuario = db.relationship('User', backref='producoes')
    
    __mapper_args__ = {
        'polymorphic_identity': 'producao',
        'polymorphic_on': tipo
    }
    
    def __repr__(self):
        return f'<Producao {self.tipo} {self.id} - {self.procedimento.codigo}>'

class BPA(ProducaoSUS):
    """Modelo para Boletim de Produção Ambulatorial"""
    __tablename__ = 'bpa'
    id = db.Column(db.Integer, db.ForeignKey('producao_sus.id'), primary_key=True)
    tipo_bpa = db.Column(db.String(1))  # C (consolidado) ou I (individualizado)
    cid = db.Column(db.String(4))
    carater_atendimento = db.Column(db.String(2))
    
    __mapper_args__ = {
        'polymorphic_identity': 'BPA',
    }

class RAAS(ProducaoSUS):
    """Modelo para Registro das Ações Ambulatoriais de Saúde"""
    __tablename__ = 'raas'
    id = db.Column(db.Integer, db.ForeignKey('producao_sus.id'), primary_key=True)
    tipo_raas = db.Column(db.String(2))  # PS (Psicossocial), AD (Atenção Domiciliar), etc.
    cid_principal = db.Column(db.String(4))
    cid_secundario = db.Column(db.String(4))
    cns_cuidador = db.Column(db.String(15))
    
    __mapper_args__ = {
        'polymorphic_identity': 'RAAS',
    }

class AIH(ProducaoSUS):
    """Modelo para Autorização de Internação Hospitalar"""
    __tablename__ = 'aih'
    id = db.Column(db.Integer, db.ForeignKey('producao_sus.id'), primary_key=True)
    numero_aih = db.Column(db.String(13), unique=True)
    data_internacao = db.Column(db.Date, nullable=False)
    data_alta = db.Column(db.Date)
    cid_principal = db.Column(db.String(4), nullable=False)
    cid_secundario = db.Column(db.String(4))
    carater_internacao = db.Column(db.String(2))
    
    __mapper_args__ = {
        'polymorphic_identity': 'AIH',
    }

class Exportacao(db.Model):
    """Modelo para registros de exportação de arquivos"""
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10), nullable=False)  # BPA, FPO, RAAS, AIH
    competencia = db.Column(db.String(6), nullable=False)  # AAAAMM
    nome_arquivo = db.Column(db.String(255), nullable=False)
    caminho_arquivo = db.Column(db.String(255), nullable=False)
    quantidade_registros = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='gerado')  # gerado, enviado, aceito, rejeitado
    data_geracao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    usuario = db.relationship('User', backref='exportacoes')
    
    def __repr__(self):
        return f'<Exportacao {self.tipo} {self.competencia} - {self.nome_arquivo}>'

class LogSistema(db.Model):
    """Modelo para logs de operações no sistema"""
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)  # login, cadastro, alteracao, exclusao, exportacao, etc.
    descricao = db.Column(db.Text, nullable=False)
    entidade = db.Column(db.String(50))  # tabela/modelo afetado
    entidade_id = db.Column(db.Integer)  # id do registro afetado
    dados_anteriores = db.Column(db.Text)  # JSON com dados antes da alteração
    dados_novos = db.Column(db.Text)  # JSON com dados após a alteração
    data = db.Column(db.DateTime, default=datetime.utcnow)
    ip = db.Column(db.String(15))
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    usuario = db.relationship('User', backref='logs')
    
    def __repr__(self):
        return f'<Log {self.tipo} {self.entidade} {self.entidade_id} - {self.data}>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
