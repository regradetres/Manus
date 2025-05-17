import unittest
from flask import url_for
from app import create_app, db
from app.models import User, ProcedimentoSIGTAP, BPA
from config import TestConfig
from datetime import date

class TestProducao(unittest.TestCase):
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
        db.session.commit()
        
        # Cria um registro de produção para testes
        self.bpa = BPA(
            competencia='202505',
            cnes='1234567',
            cns_profissional='123456789012345',
            cbo='123456',
            cns_paciente='987654321098765',
            data_atendimento=date(2025, 5, 15),
            procedimento_id=self.proc.id,
            quantidade=1,
            valor_calculado=10.0,
            status='pendente',
            usuario_id=self.admin.id,
            tipo_bpa='I',
            cid='A00'
        )
        db.session.add(self.bpa)
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
    
    def test_producao_index(self):
        # Testa se a página principal de produção é carregada corretamente
        response = self.client.get('/producao/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Produ\xc3\xa7\xc3\xa3o SUS', response.data)
        self.assertIn(b'BPA', response.data)
    
    def test_selecionar_tipo(self):
        # Testa se a página de seleção de tipo é carregada corretamente
        response = self.client.get('/producao/selecionar-tipo')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Selecionar Tipo de Produ\xc3\xa7\xc3\xa3o', response.data)
        self.assertIn(b'Boletim de Produ\xc3\xa7\xc3\xa3o Ambulatorial', response.data)
        self.assertIn(b'Registro das A\xc3\xa7\xc3\xb5es Ambulatoriais de Sa\xc3\xbade', response.data)
        self.assertIn(b'Autoriza\xc3\xa7\xc3\xa3o de Interna\xc3\xa7\xc3\xa3o Hospitalar', response.data)
    
    def test_novo_bpa(self):
        # Testa se a página de novo BPA é carregada corretamente
        response = self.client.get('/producao/bpa/novo')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Novo BPA', response.data)
    
    def test_listar_bpa(self):
        # Testa se a lista de BPA é carregada corretamente
        response = self.client.get('/producao/listar/BPA')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Lista de BPA', response.data)
        self.assertIn(b'1234567', response.data)  # CNES
    
    def test_validar_registro(self):
        # Testa a validação de um registro
        response = self.client.get(f'/producao/validar/{self.bpa.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Validar Registro', response.data)
        
        # Testa o POST para validar
        response = self.client.post(f'/producao/validar/{self.bpa.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'validado com sucesso', response.data)
        
        # Verifica se o status foi alterado no banco
        bpa = BPA.query.get(self.bpa.id)
        self.assertEqual(bpa.status, 'validado')

if __name__ == '__main__':
    unittest.main()
