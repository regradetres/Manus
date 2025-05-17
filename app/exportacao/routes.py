from flask import render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required, current_user
from app.exportacao import bp
from app import db
from app.models import ProducaoSUS, Exportacao
import os
from datetime import datetime

@bp.route('/')
@login_required
def index():
    """Página principal do módulo de Exportação"""
    # Últimas exportações
    exportacoes = Exportacao.query.order_by(Exportacao.data_geracao.desc()).limit(10).all()
    
    return render_template(
        'exportacao/index.html',
        title='Exportação DATASUS',
        exportacoes=exportacoes
    )

@bp.route('/configurar', methods=['GET', 'POST'])
@login_required
def configurar():
    """Configuração de parâmetros para exportação"""
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        competencia = request.form.get('competencia')
        apenas_validados = 'apenas_validados' in request.form
        
        if not tipo or not competencia:
            flash('Tipo e competência são obrigatórios', 'danger')
            return redirect(request.url)
        
        # Redireciona para a página de exportação com os parâmetros
        return redirect(url_for(
            'exportacao.exportar',
            tipo=tipo,
            competencia=competencia,
            apenas_validados=apenas_validados
        ))
    
    return render_template('exportacao/configurar.html', title='Configurar Exportação')

@bp.route('/exportar')
@login_required
def exportar():
    """Exportação de arquivos para o formato DATASUS"""
    tipo = request.args.get('tipo')
    competencia = request.args.get('competencia')
    apenas_validados = request.args.get('apenas_validados') == 'True'
    
    if not tipo or not competencia:
        flash('Parâmetros inválidos', 'danger')
        return redirect(url_for('exportacao.configurar'))
    
    # Contagem de registros a serem exportados
    query = ProducaoSUS.query.filter_by(tipo=tipo, competencia=competencia)
    if apenas_validados:
        query = query.filter_by(status='validado')
    
    total_registros = query.count()
    
    if total_registros == 0:
        flash(f'Nenhum registro encontrado para {tipo} na competência {competencia}', 'warning')
        return redirect(url_for('exportacao.configurar'))
    
    # Aqui seria implementada a lógica de exportação real
    # Por enquanto, apenas simula a exportação
    
    # Cria registro de exportação
    nome_arquivo = f"{tipo}_{competencia}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
    caminho_arquivo = os.path.join('/tmp', nome_arquivo)
    
    exportacao = Exportacao(
        tipo=tipo,
        competencia=competencia,
        nome_arquivo=nome_arquivo,
        caminho_arquivo=caminho_arquivo,
        quantidade_registros=total_registros,
        usuario_id=current_user.id
    )
    
    db.session.add(exportacao)
    db.session.commit()
    
    flash(f'Exportação de {total_registros} registros concluída com sucesso!', 'success')
    return redirect(url_for('exportacao.resultado', id=exportacao.id))

@bp.route('/resultado/<int:id>')
@login_required
def resultado(id):
    """Resultado da exportação"""
    exportacao = Exportacao.query.get_or_404(id)
    
    return render_template(
        'exportacao/resultado.html',
        title='Resultado da Exportação',
        exportacao=exportacao
    )

@bp.route('/download/<int:id>')
@login_required
def download(id):
    """Download do arquivo exportado"""
    exportacao = Exportacao.query.get_or_404(id)
    
    # Em uma implementação real, verificaria se o arquivo existe
    # e retornaria o arquivo para download
    # Por enquanto, apenas simula o download
    
    # Cria um arquivo de exemplo se não existir
    if not os.path.exists(exportacao.caminho_arquivo):
        with open(exportacao.caminho_arquivo, 'w') as f:
            f.write(f"Arquivo de exemplo para {exportacao.tipo} - {exportacao.competencia}\n")
            f.write(f"Total de registros: {exportacao.quantidade_registros}\n")
    
    return send_file(
        exportacao.caminho_arquivo,
        as_attachment=True,
        download_name=exportacao.nome_arquivo
    )
