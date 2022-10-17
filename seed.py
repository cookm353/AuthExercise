from app import app
from flask_bcrypt import Bcrypt
from models import db, User, Feedback

bcrypt = Bcrypt()

db.drop_all()
db.create_all()

User.query.delete()

jsnow = User(username='AzorAhai', password=User.hash_password("JonAndYgritte4Ever"), 
             email='jsnow@thwatch.org', first_name='Jon', last_name='Snow')
dumbledore = User(username='BeardedOne', password=User.hash_password('ShutUpLucy'),
                  email='adumbledore@hogwarts.edu', first_name='Albus',
                  last_name='Dumbledore')
mario = User(username='ItsAMe', password=User.hash_password('AMario!'), email='MM@mushroomkingdom.net',
             first_name='Mario', last_name='Mario')


db.session.add_all([jsnow, dumbledore, mario])
db.session.commit()