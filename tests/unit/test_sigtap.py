import unittest
from flask import url_for
from app import create_app, db
from app.models import User, ProcedimentoSIGTAP
from config import TestConfig
import io

class TestSigtap(unittest.TestCase):
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
        
        # Cria alguns procedimentos para testes
        proc1 = ProcedimentoSIGTAP(
            codigo='0101010010',
            nome='CONSULTA MÉDICA EM ATENÇÃO BÁSICA',
            grupo='01',
            subgrupo='01',
            forma_organizacao='01',
            valor=10.0
        )
        proc2 = ProcedimentoSIGTAP(
            codigo='0201010372',
            nome='TESTE RÁPIDO PARA HIV',
            grupo='02',
            subgrupo='01',
            forma_organizacao='01',
            valor=15.0
        )
        db.session.add_all([proc1, proc2])
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
    
    def test_sigtap_index(self):
        # Testa se a página principal do SIGTAP é carregada corretamente
        response = self.client.get('/sigtap/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'SIGTAP', response.data)
        self.assertIn(b'0101010010', response.data)
    
    def test_sigtap_importar(self):
        # Testa se a página de importação é carregada corretamente
        response = self.client.get('/sigtap/importar')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Importa\xc3\xa7\xc3\xa3o da Tabela SIGTAP', response.data)
    
    def test_sigtap_procedimentos(self):
        # Testa se a lista de procedimentos é carregada corretamente
        response = self.client.get('/sigtap/procedimentos')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'0101010010', response.data)
        self.assertIn(b'CONSULTA M\xc3\x89DICA', response.data)
        self.assertIn(b'0201010372', response.data)
        self.assertIn(b'TESTE R\xc3\x81PIDO PARA HIV', response.data)
    
    def test_sigtap_procedimentos_busca(self):
        # Testa a busca de procedimentos
        response = self.client.get('/sigtap/procedimentos?busca=HIV')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'0201010372', response.data)
        self.assertIn(b'TESTE R\xc3\x81PIDO PARA HIV', response.data)
        self.assertNotIn(b'0101010010', response.data)
        self.assertNotIn(b'CONSULTA M\xc3\x89DICA', response.data)
    
    def test_sigtap_procedimento_detalhe(self):
        # Testa a visualização detalhada de um procedimento
        response = self.client.get('/sigtap/procedimentos/0101010010')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'0101010010', response.data)
        self.assertIn(b'CONSULTA M\xc3\x89DICA', response.data)
    
    def test_sigtap_importar_post(self):
        # Testa o envio de um arquivo para importação
        data = {
            'arquivo': (io.BytesIO(b'fake zip content'), 'sigtap.zip'),
            'confirmar': 'on'
        }
        response = self.client.post('/sigtap/importar', data=data, 
                                    content_type='multipart/form-data',
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Arquivo recebido', response.data)

if __name__ == '__main__':
    unittest.main()
