import unittest
from flask import url_for
from app import create_app, db
from app.models import User, ProcedimentoSIGTAP, BPA, Exportacao
from config import TestConfig
from datetime import date, datetime

class TestExportacao(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        
        # Cria um usuário para testes
        self.admin = User(username='admin', email='admin@example.com', 
                          nome_completo='Administrador', perfil='admin')
        self.admin.set_password('senha123')
        db.session.add(self.admin)
        
        # Cria um procedimento para testes
        self.proc = ProcedimentoSIGTAP(
            codigo='0101010010',
            nome='CONSULTA MÉDICA EM ATENÇÃO BÁSICA',
            grupo='01',
            subgrupo='01',
            forma_organizacao='01',
            valor=10.0
        )
        db.session.add(self.proc)
        
        # Cria registros de produção para testes
        self.bpa = BPA(
            competencia='202505',
            cnes='1234567',
            cns_profissional='123456789012345',
            cbo='123456',
            cns_paciente='987654321098765',
            data_atendimento=date(2025, 5, 15),
            procedimento_id=1,
            quantidade=1,
            valor_calculado=10.0,
            status='validado',
            usuario_id=1,
            tipo_bpa='I',
            cid='A00'
        )
        db.session.add(self.bpa)
        
        # Cria um registro de exportação para testes
        self.exportacao = Exportacao(
            tipo='BPA',
            competencia='202505',
            nome_arquivo='BPA_202505_20250517.txt',
            caminho_arquivo='/tmp/BPA_202505_20250517.txt',
            quantidade_registros=1,
            status='gerado',
            data_geracao=datetime.now(),
            usuario_id=1
        )
        db.session.add(self.exportacao)
        db.session.commit()
        
        # Faz login
        self.client.post('/auth/login', data={
            'username': 'admin',
            'password': 'senha123',
            'remember_me': False
        })
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_exportacao_index(self):
        # Testa se a página principal de exportação é carregada corretamente
        response = self.client.get('/exportacao/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Exporta\xc3\xa7\xc3\xa3o DATASUS', response.data)
        self.assertIn(b'BPA_202505', response.data)
    
    def test_configurar_exportacao(self):
        # Testa se a página de configuração de exportação é carregada corretamente
        response = self.client.get('/exportacao/configurar')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Configurar Exporta\xc3\xa7\xc3\xa3o', response.data)
        self.assertIn(b'Tipo de Arquivo', response.data)
        self.assertIn(b'Compet\xc3\xaancia', response.data)
    
    def test_exportar(self):
        # Testa a exportação
        response = self.client.get('/exportacao/exportar?tipo=BPA&competencia=202505&apenas_validados=True', 
                                  follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Exporta\xc3\xa7\xc3\xa3o', response.data)
        self.assertIn(b'conclu\xc3\xadda com sucesso', response.data)
    
    def test_resultado_exportacao(self):
        # Testa a visualização do resultado da exportação
        response = self.client.get(f'/exportacao/resultado/{self.exportacao.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Resultado da Exporta\xc3\xa7\xc3\xa3o', response.data)
        self.assertIn(b'BPA_202505', response.data)

if __name__ == '__main__':
    unittest.main()
