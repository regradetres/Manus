import unittest
from app import create_app, db
from app.models import User, ProcedimentoSIGTAP, BPA, RAAS, AIH, Exportacao
from config import TestConfig
import os

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        
        # Cria usuário admin para testes
        admin = User(username='admin', email='admin@example.com', 
                     nome_completo='Administrador', perfil='admin')
        admin.set_password('senha123')
        db.session.add(admin)
        db.session.commit()
        
        # Login como admin
        self.client.post('/auth/login', data={
            'username': 'admin',
            'password': 'senha123',
            'remember_me': False
        })
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_fluxo_completo(self):
        """Testa o fluxo completo de cadastro, validação e exportação"""
        
        # 1. Cadastro de procedimento SIGTAP
        proc = ProcedimentoSIGTAP(
            codigo='0101010010',
            nome='CONSULTA MÉDICA EM ATENÇÃO BÁSICA',
            grupo='01',
            subgrupo='01',
            forma_organizacao='01',
            valor=10.0
        )
        db.session.add(proc)
        db.session.commit()
        
        # Verifica se o procedimento foi cadastrado
        response = self.client.get('/sigtap/procedimentos')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'0101010010', response.data)
        
        # 2. Cadastro de produção BPA
        from datetime import date
        bpa = BPA(
            competencia='202505',
            cnes='1234567',
            cns_profissional='123456789012345',
            cbo='123456',
            cns_paciente='987654321098765',
            data_atendimento=date(2025, 5, 15),
            procedimento_id=proc.id,
            quantidade=1,
            valor_calculado=10.0,
            status='pendente',
            usuario_id=1,
            tipo_bpa='I',
            cid='A00'
        )
        db.session.add(bpa)
        db.session.commit()
        
        # Verifica se a produção foi cadastrada
        response = self.client.get('/producao/listar/BPA')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'1234567', response.data)
        
        # 3. Validação da produção
        response = self.client.post(f'/producao/validar/{bpa.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'validado com sucesso', response.data)
        
        # Verifica se o status foi alterado
        bpa_validado = BPA.query.get(bpa.id)
        self.assertEqual(bpa_validado.status, 'validado')
        
        # 4. Exportação
        response = self.client.get('/exportacao/exportar?tipo=BPA&competencia=202505&apenas_validados=True', 
                                  follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Exporta\xc3\xa7\xc3\xa3o', response.data)
        self.assertIn(b'conclu\xc3\xadda com sucesso', response.data)
        
        # Verifica se a exportação foi registrada
        exportacao = Exportacao.query.filter_by(tipo='BPA', competencia='202505').first()
        self.assertIsNotNone(exportacao)
        self.assertEqual(exportacao.quantidade_registros, 1)
        
        # 5. Download do arquivo exportado
        response = self.client.get(f'/exportacao/download/{exportacao.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/octet-stream')

if __name__ == '__main__':
    unittest.main()
