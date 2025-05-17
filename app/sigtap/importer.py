from app import db
import csv
import xml.etree.ElementTree as ET
import os
from datetime import datetime

class SIGTAPImporter:
    """Classe para importação da tabela SIGTAP usando módulos padrão do Python"""
    
    def __init__(self, app):
        self.app = app
        self.upload_folder = app.config['SIGTAP_UPLOAD_FOLDER']
    
    def process_zip_file(self, zip_path, competencia):
        """Processa arquivo ZIP da tabela SIGTAP"""
        from zipfile import ZipFile
        
        # Cria diretório temporário para extração
        import tempfile
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Extrai arquivos
            with ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Processa arquivos extraídos
            self.process_extracted_files(temp_dir, competencia)
            
            return True, "Importação concluída com sucesso"
        except Exception as e:
            return False, f"Erro ao processar arquivo: {str(e)}"
        finally:
            # Limpa diretório temporário
            import shutil
            shutil.rmtree(temp_dir)
    
    def process_extracted_files(self, directory, competencia):
        """Processa arquivos extraídos do ZIP"""
        from app.models import ProcedimentoSIGTAP
        
        # Procura arquivo de procedimentos
        proc_file = None
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().startswith('tb_procedimento'):
                    proc_file = os.path.join(root, file)
                    break
        
        if not proc_file:
            raise Exception("Arquivo de procedimentos não encontrado")
        
        # Processa arquivo de procedimentos
        with open(proc_file, 'r', encoding='latin-1') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)  # Pula cabeçalho
            
            # Limpa procedimentos existentes para a competência
            ProcedimentoSIGTAP.query.filter_by(competencia_inicio=competencia).delete()
            
            # Insere novos procedimentos
            for row in reader:
                if len(row) < 5:
                    continue
                    
                codigo = row[0].strip()
                nome = row[1].strip()
                
                # Extrai grupo, subgrupo e forma de organização do código
                grupo = codigo[:2] if len(codigo) >= 2 else ''
                subgrupo = codigo[2:4] if len(codigo) >= 4 else ''
                forma_org = codigo[4:6] if len(codigo) >= 6 else ''
                
                # Valor padrão se não disponível
                valor = 0.0
                try:
                    if len(row) > 4 and row[4].strip():
                        valor = float(row[4].replace(',', '.'))
                except ValueError:
                    pass
                
                proc = ProcedimentoSIGTAP(
                    codigo=codigo,
                    nome=nome,
                    grupo=grupo,
                    subgrupo=subgrupo,
                    forma_organizacao=forma_org,
                    valor=valor,
                    competencia_inicio=competencia
                )
                db.session.add(proc)
            
            db.session.commit()
