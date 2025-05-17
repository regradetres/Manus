import unittest
from app import create_app, db
from app.models import User, ProcedimentoSIGTAP, ProducaoSUS, BPA, RAAS, AIH
from config import TestConfig

class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_user_model(self):
        # Teste de criação de usuário
        u = User(username='teste', email='teste@example.com', nome_completo='Usuário Teste', perfil='digitador')
        u.set_password('senha123')
        db.session.add(u)
        db.session.commit()
        
        # Verifica se o usuário foi salvo corretamente
        usuario = User.query.filter_by(username='teste').first()
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.email, 'teste@example.com')
        self.assertEqual(usuario.nome_completo, 'Usuário Teste')
        self.assertEqual(usuario.perfil, 'digitador')
        
        # Verifica a verificação de senha
        self.assertTrue(usuario.check_password('senha123'))
        self.assertFalse(usuario.check_password('senha_errada'))
        
        # Verifica a propriedade is_admin
        self.assertFalse(usuario.is_admin)
        usuario.perfil = 'admin'
        self.assertTrue(usuario.is_admin)
    
    def test_procedimento_sigtap_model(self):
        # Teste de criação de procedimento
        proc = ProcedimentoSIGTAP(
            codigo='0101010010',
            nome='CONSULTA MÉDICA EM ATENÇÃO BÁSICA',
            grupo='01',
            subgrupo='01',
            forma_organizacao='01',
            complexidade='Média Complexidade',
            valor=10.0,
            competencia_inicio='202501'
        )
        db.session.add(proc)
        db.session.commit()
        
        # Verifica se o procedimento foi salvo corretamente
        procedimento = ProcedimentoSIGTAP.query.filter_by(codigo='0101010010').first()
        self.assertIsNotNone(procedimento)
        self.assertEqual(procedimento.nome, 'CONSULTA MÉDICA EM ATENÇÃO BÁSICA')
        self.assertEqual(procedimento.valor, 10.0)
    
    def test_producao_bpa_model(self):
        # Cria usuário e procedimento para relacionamento
        u = User(username='teste', email='teste@example.com', nome_completo='Usuário Teste', perfil='digitador')
        u.set_password('senha123')
        db.session.add(u)
        
        proc = ProcedimentoSIGTAP(
            codigo='0101010010',
            nome='CONSULTA MÉDICA EM ATENÇÃO BÁSICA',
            valor=10.0
        )
        db.session.add(proc)
        db.session.commit()
        
        # Teste de criação de produção BPA
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
            usuario_id=u.id,
            tipo_bpa='I',
            cid='A00'
        )
        db.session.add(bpa)
        db.session.commit()
        
        # Verifica se a produção foi salva corretamente
        producao = BPA.query.first()
        self.assertIsNotNone(producao)
        self.assertEqual(producao.competencia, '202505')
        self.assertEqual(producao.cnes, '1234567')
        self.assertEqual(producao.tipo, 'BPA')
        self.assertEqual(producao.tipo_bpa, 'I')
        self.assertEqual(producao.cid, 'A00')
        self.assertEqual(producao.procedimento.codigo, '0101010010')
        self.assertEqual(producao.usuario.username, 'teste')

if __name__ == '__main__':
    unittest.main()
