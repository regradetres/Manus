import unittest
from flask import url_for
from app import create_app, db
from app.models import User
from config import TestConfig

class TestAuth(unittest.TestCase):
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
        db.session.commit()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_login_page(self):
        # Testa se a página de login é carregada corretamente
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    def test_login_success(self):
        # Testa login com credenciais corretas
        response = self.client.post('/auth/login', data={
            'username': 'admin',
            'password': 'senha123',
            'remember_me': False
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)
    
    def test_login_failure(self):
        # Testa login com credenciais incorretas
        response = self.client.post('/auth/login', data={
            'username': 'admin',
            'password': 'senha_errada',
            'remember_me': False
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Nome de usu\xc3\xa1rio ou senha inv\xc3\xa1lidos', response.data)
    
    def test_logout(self):
        # Faz login primeiro
        self.client.post('/auth/login', data={
            'username': 'admin',
            'password': 'senha123',
            'remember_me': False
        })
        
        # Testa logout
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    def test_register_page_requires_login(self):
        # Testa que a página de registro requer login
        response = self.client.get('/auth/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    def test_register_page_requires_admin(self):
        # Cria um usuário não-admin
        user = User(username='user', email='user@example.com', 
                    nome_completo='Usuário Normal', perfil='digitador')
        user.set_password('senha123')
        db.session.add(user)
        db.session.commit()
        
        # Faz login com usuário não-admin
        self.client.post('/auth/login', data={
            'username': 'user',
            'password': 'senha123',
            'remember_me': False
        })
        
        # Tenta acessar a página de registro
        response = self.client.get('/auth/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Acesso negado', response.data)

if __name__ == '__main__':
    unittest.main()
