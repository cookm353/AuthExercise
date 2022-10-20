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
dude = User(username='TheDude', password=User.hash_password('Abides'), email='thedude@aol.com', 
            first_name='Jeff', last_name='Lebowski')

db.session.add_all([jsnow, dumbledore, mario, dude])
db.session.commit()

Feedback.query.delete()

watch = Feedback(title='My Watch Has Ended', content='Suck it, Olly', 
                 username='AzorAhai')
itsme = Feedback(title="It's a Me!", content='Mario!', username='ItsAMe')
socks = Feedback(title='Wardrobe Tips', content='One can never have enough socks',
                 username='BeardedOne')
opinion = Feedback(title="Well that's just like your opinion", content='Man',
                   username='TheDude')

db.session.add_all([watch, itsme, socks, opinion])
db.session.commit()