from unittest import TestCase
from models import db, User
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_auth_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class TestUser(TestCase):
    def setUp(self):
        User.query.delete()
        dude_data = {
            'username':'TheDude', 'password': 'Abides', 
            'email':'thedude@aol.com', 'first_name':'Jeff', 'last_name': 'Lebowski'}
        
        dude = User.register(dude_data)
        User.add(dude)
        
        db.session.add(dude)
        db.session.commit()
        
    def tearDown(self):
        db.session.rollback()
    
    def test_register(self):
        dude_data = {
            'username':'TheDude', 'password': 'Abides', 
            'email':'thedude@aol.com', 'first_name':'Jeff', 
            'last_name': 'Lebowski'
        }
        
        dude = User.register(dude_data)
        
        self.assertIsInstance(dude, User)
        
    def test_authentication(self):
        dude_data = {
            'username': 'TheDude', 'password': 'Abides'
        }
        
        self.assertIsInstance(User.authenticate(dude_data), User)
        
    def test_get_user(self):
        dude = User.get('TheDude')
        
        self.assertIsInstance(dude, User)
        self.assertEqual(dude.username, 'TheDude')
        self.assertNotEqual(dude.password, 'Abides')
        
    def test_get_all_users(self):
        users = User.get_all()
        
        self.assertEqual(users[0].username, 'TheDude')