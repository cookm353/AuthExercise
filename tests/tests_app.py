from unittest import TestCase
from app import app
from models import User, db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_auth_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class TestApp(TestCase):
    def setUp(self):
        User.query.delete()
        dude_data = {
            'username':'TheDude', 'password': 'Abides', 
            'email':'thedude@aol.com', 'first_name':'Jeff', 'last_name': 'Lebowski'}
        
        dude = User.register(dude_data)
        User.add_user(dude)
        
        db.session.add(dude)
        db.session.commit()
        
    def tearDown(self):
        db.session.rollback()
        
    def test_home_page_logged_out(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Register', html)
            self.assertIn('Login', html)
            
    def test_registration_form(self):
        with app.test_client() as client:
            resp = client.get('/register')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Password', html)
            self.assertIn('Email', html)
            self.assertIn('Submit', html)
            
    def test_registering(self):
        with app.test_client() as client:
            formData = {
                'username': 'SunBro', 'password': 'PraiseTheSun!',
                'email': 'solaire@astoraknights.org', 'first_name': 'Solaire', 
                'last_name': 'of Astora' 
            }
            resp = client.post('/register', data=formData)
            
            self.assertEqual(resp.status_code, 302)
            
    def test_register_redirect(self):
        with app.test_client() as client:
            formData = {
                'username': 'SunBro', 'password': 'PraiseTheSun!',
                'email': 'solaire@astoraknights.org', 'first_name': 'Solaire', 
                'last_name': 'of Astora' 
            }
            resp = client.post('/register', data=formData, follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('SunBro', html)
            
    def test_login_form(self):
        with app.test_client() as client:
            resp = client.get('/login')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Username', html)
            self.assertIn('Password', html)
            self.assertNotIn('email', html)
            
    def test_logging_in(self):
        with app.test_client() as client:
            formData = {'username': 'TheDude', 'password': 'Abides'}
            resp = client.post('/login',  data=formData)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 302)
            
    def test_log_in_redirect(self):
        with app.test_client() as client:
            formData = {'username': 'TheDude', 'password': 'Abides'}
            resp = client.post('/login',  data=formData, follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Lebowski', html)
            self.assertNotIn('Abides', html)
            
    def test_user_info_redirect(self):
        with app.test_client() as client:
            resp = client.get('/users/TheDude', follow_redirects=True)
            html = resp.get_data(as_text=True)            
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Register', html)
            self.assertNotIn('Lebowski', html)