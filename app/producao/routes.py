from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.producao import bp
from app import db
from app.models import ProducaoSUS, BPA, RAAS, AIH, ProcedimentoSIGTAP

@bp.route('/')
@login_required
def index():
    """Página principal do módulo de Produção"""
    # Contagem de registros por tipo e status
    bpa_count = BPA.query.filter_by(usuario_id=current_user.id).count()
    raas_count = RAAS.query.filter_by(usuario_id=current_user.id).count()
    aih_count = AIH.query.filter_by(usuario_id=current_user.id).count()
    
    # Registros recentes
    registros_recentes = ProducaoSUS.query.filter_by(
        usuario_id=current_user.id
    ).order_by(ProducaoSUS.data_criacao.desc()).limit(5).all()
    
    return render_template(
        'producao/index.html',
        title='Produção SUS',
        bpa_count=bpa_count,
        raas_count=raas_count,
        aih_count=aih_count,
        registros_recentes=registros_recentes
    )

@bp.route('/selecionar-tipo')
@login_required
def selecionar_tipo():
    """Página para seleção do tipo de produção a ser cadastrada"""
    return render_template('producao/selecionar_tipo.html', title='Selecionar Tipo de Produção')

@bp.route('/bpa/novo', methods=['GET', 'POST'])
@login_required
def novo_bpa():
    """Cadastro de novo BPA"""
    # Implementação completa seria feita em uma fase posterior
    return render_template('producao/bpa_form.html', title='Novo BPA')

@bp.route('/raas/novo', methods=['GET', 'POST'])
@login_required
def novo_raas():
    """Cadastro de nova RAAS"""
    # Implementação completa seria feita em uma fase posterior
    return render_template('producao/raas_form.html', title='Nova RAAS')

@bp.route('/aih/novo', methods=['GET', 'POST'])
@login_required
def novo_aih():
    """Cadastro de nova AIH"""
    # Implementação completa seria feita em uma fase posterior
    return render_template('producao/aih_form.html', title='Nova AIH')

@bp.route('/listar/<tipo>')
@login_required
def listar(tipo):
    """Lista registros de produção por tipo"""
    page = request.args.get('page', 1, type=int)
    
    if tipo.upper() == 'BPA':
        registros = BPA.query.filter_by(
            usuario_id=current_user.id
        ).order_by(BPA.data_atendimento.desc()).paginate(page=page, per_page=20)
        template = 'producao/bpa_lista.html'
    elif tipo.upper() == 'RAAS':
        registros = RAAS.query.filter_by(
            usuario_id=current_user.id
        ).order_by(RAAS.data_atendimento.desc()).paginate(page=page, per_page=20)
        template = 'producao/raas_lista.html'
    elif tipo.upper() == 'AIH':
        registros = AIH.query.filter_by(
            usuario_id=current_user.id
        ).order_by(AIH.data_internacao.desc()).paginate(page=page, per_page=20)
        template = 'producao/aih_lista.html'
    else:
        flash(f'Tipo de produção inválido: {tipo}', 'danger')
        return redirect(url_for('producao.index'))
    
    return render_template(
        template,
        title=f'Lista de {tipo.upper()}',
        registros=registros
    )

@bp.route('/validar/<int:id>', methods=['GET', 'POST'])
@login_required
def validar(id):
    """Validação de um registro de produção"""
    registro = ProducaoSUS.query.get_or_404(id)
    
    # Verifica permissão (apenas admin e supervisor podem validar)
    if not current_user.perfil in ['admin', 'supervisor']:
        flash('Você não tem permissão para validar registros.', 'danger')
        return redirect(url_for('producao.index'))
    
    # Implementação completa seria feita em uma fase posterior
    # Por enquanto, apenas marca como validado
    if request.method == 'POST':
        registro.status = 'validado'
        db.session.commit()
        flash(f'Registro {id} validado com sucesso!', 'success')
        return redirect(url_for('producao.index'))
    
    return render_template(
        'producao/validar.html',
        title='Validar Registro',
        registro=registro
    )
