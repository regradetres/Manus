from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.sigtap import bp
from app import db
from app.models import ProcedimentoSIGTAP
import os
import zipfile
import pandas as pd
from werkzeug.utils import secure_filename

@bp.route('/')
@login_required
def index():
    """Página principal do módulo SIGTAP"""
    procedimentos = ProcedimentoSIGTAP.query.order_by(ProcedimentoSIGTAP.codigo).limit(20).all()
    return render_template('sigtap/index.html', title='SIGTAP', procedimentos=procedimentos)

@bp.route('/importar', methods=['GET', 'POST'])
@login_required
def importar():
    """Rota para importação da tabela SIGTAP"""
    if request.method == 'POST':
        # Verifica se o arquivo foi enviado
        if 'arquivo' not in request.files:
            flash('Nenhum arquivo selecionado', 'danger')
            return redirect(request.url)
        
        arquivo = request.files['arquivo']
        
        # Verifica se o nome do arquivo está vazio
        if arquivo.filename == '':
            flash('Nenhum arquivo selecionado', 'danger')
            return redirect(request.url)
        
        # Verifica se é um arquivo ZIP
        if arquivo and arquivo.filename.endswith('.zip'):
            # Salva o arquivo temporariamente
            filename = secure_filename(arquivo.filename)
            temp_path = os.path.join(current_app.instance_path, filename)
            arquivo.save(temp_path)
            
            try:
                # Processa o arquivo ZIP
                flash('Arquivo recebido. Processamento iniciado em segundo plano.', 'info')
                # Aqui seria implementado o processamento assíncrono
                # Por enquanto, apenas simula o processamento
                
                # Exemplo de como seria o processamento:
                # processar_sigtap(temp_path)
                
                return redirect(url_for('sigtap.index'))
            except Exception as e:
                flash(f'Erro ao processar arquivo: {str(e)}', 'danger')
                return redirect(request.url)
        else:
            flash('Formato de arquivo inválido. Por favor, envie um arquivo ZIP.', 'danger')
            return redirect(request.url)
    
    return render_template('sigtap/importar.html', title='Importar SIGTAP')

@bp.route('/procedimentos')
@login_required
def procedimentos():
    """Lista de procedimentos importados da tabela SIGTAP"""
    page = request.args.get('page', 1, type=int)
    busca = request.args.get('busca', '')
    
    if busca:
        procedimentos = ProcedimentoSIGTAP.query.filter(
            (ProcedimentoSIGTAP.codigo.contains(busca)) | 
            (ProcedimentoSIGTAP.nome.contains(busca))
        ).paginate(page=page, per_page=20)
    else:
        procedimentos = ProcedimentoSIGTAP.query.order_by(
            ProcedimentoSIGTAP.codigo
        ).paginate(page=page, per_page=20)
    
    return render_template(
        'sigtap/procedimentos.html', 
        title='Procedimentos SIGTAP',
        procedimentos=procedimentos,
        busca=busca
    )

@bp.route('/procedimentos/<codigo>')
@login_required
def procedimento_detalhe(codigo):
    """Detalhes de um procedimento específico"""
    procedimento = ProcedimentoSIGTAP.query.filter_by(codigo=codigo).first_or_404()
    return render_template(
        'sigtap/procedimento_detalhe.html',
        title=f'Procedimento {procedimento.codigo}',
        procedimento=procedimento
    )

def processar_sigtap(arquivo_zip):
    """Função para processar o arquivo ZIP da tabela SIGTAP"""
    # Esta função seria chamada de forma assíncrona
    # Implementação completa seria feita em uma fase posterior
    pass
