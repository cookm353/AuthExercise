from unittest import TestCase
from app import app
from models import User, Feedback, db

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
        Feedback.query.delete()
        
        dude_data = {
            'username':'TheDude', 'password': 'Abides', 
            'email':'thedude@aol.com', 'first_name':'Jeff', 'last_name': 'Lebowski'}
        walt_data = {
            'username': 'WSobchak', 'password': 'MIAKIA',
            'email': 'wsobchak@comcast.net', 'first_name': 'Walter', 'last_name': 'Sobchak'}
        
        dude = User.register(dude_data)
        User.add(dude)
        walt = User.register(walt_data)
        User.add(walt)
        
        
        db.session.add_all([dude, walt])
        db.session.commit()
        
        title = "You're not wrong Walter"
        content = "You're just an asshole"
        username = 'TheDude'
        feedback = Feedback(title=title, content=content, username=username)
        
        db.session.add(feedback)
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
            
    def test_deleting_user(self):
        with app.test_client() as client:
            data = {'username': 'TheDude'}
            delete_resp = client.post('/users/TheDude/delete', data=data, follow_redirects=True)
            html = delete_resp.get_data(as_text=True)
            
            self.assertEqual(delete_resp.status_code, 200)
            self.assertIn('Register', html)
            self.assertIn('Login', html)
            
            user_info_resp = client.get('/users/TheDude')
            self.assertEqual(user_info_resp.status_code, 302)
            
    def test_feedback_form_display(self):
        with app.test_client() as client:
            login_data = {'username': 'TheDude', 'password': 'Abides'}
            login_resp = client.post('/login', data=login_data)
            feedback_resp = client.get('/users/TheDude/feedback/add')
            html = feedback_resp.get_data(as_text=True)
            
            self.assertEqual(feedback_resp.status_code, 200)
            self.assertIn('Title', html)
                
    def test_adding_feedback(self):
        with app.test_client() as client:
            login_data = {'username': 'TheDude', 'password': 'Abides'}
            login_resp = client.post('/login', data=login_data)
            feedback_data = {'title': "Well that's just like your opinion",
                             'content': 'Man', 'username': 'TheDude'}
            feedback_resp = client.post('/users/TheDude/feedback/add', data=feedback_data, follow_redirects=True)
            html = feedback_resp.get_data(as_text=True)
            
            self.assertEqual(feedback_resp.status_code, 200)
            self.assertIn('opinion', html)
            self.assertIn('TheDude', html)
            
    def test_update_feedback_form(self):
        with app.test_client() as client:
            login_data = {'username': 'TheDude', 'password': 'Abides'}
            login_resp = client.post('/login', data=login_data)
            self.assertEqual(login_resp.status_code, 302)
            
            feedback_resp = client.get('/users/1/update')
            html = feedback_resp.get_data(as_text=True)
            
            self.assertEqual(feedback_resp.status_code, 200)
            self.assertIn('asshole', html)
    
    def test_feedback_update_access(self):
        """Making sure only the user who wrote feedback can edit"""
        with app.test_client() as client:
            login_data = {'username': 'WSobchak', 'password': 'MIAKIA'}
            login_resp = client.post('/login', data=login_data)
            self.assertEqual(login_resp.status_code, 302)
            
            feedback_resp = client.get('/users/1/update', follow_redirects=True)
            html = feedback_resp.get_data(as_text=True)
            
            self.assertEqual(feedback_resp.status_code, 200)
            self.assertIn('Sobchak', html)
            self.assertNotIn('asshole', html)
            
    def test_updating_feedback(self):
        with app.test_client() as client:
            login_data = {'username': 'TheDude', 'password': 'Abides'}
            login_resp = client.post('/login', data=login_data)
            self.assertEqual(login_resp.status_code, 302)
            
            feedback_data = {'title': "Well that's just like your opinion",
                'content': 'Man'}
            feedback_resp = client.post('/users/1/update', data=feedback_data, follow_redirects=True)
            html = feedback_resp.get_data(as_text=True)
            
            self.assertEqual(feedback_resp.status_code, 200)
            self.assertNotIn('asshole', html)
            self.assertIn('Man', html)
            
    def test_deleting_feedback(self):
        with app.test_client() as client:
            login_data = {'username': 'TheDude', 'password': 'Abides'}
            login_resp = client.post('/login', data=login_data)
            self.assertEqual(login_resp.status_code, 302)
            
            delete_resp = client.post('/users/1/delete', follow_redirects=True)
            html = delete_resp.get_data(as_text=True)
            self.assertEqual(delete_resp.status_code, 200)
            self.assertNotIn('asshole', html)