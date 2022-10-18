from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
class User(db.Model):
    __tablename__ = 'users'
    
    username = db.Column(db.String(20), primary_key=True, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    
    def __repr__(self):
        return f"<User username={self.username} email={self.email} first_name={self.first_name} last_name={self.last_name}>"

    @classmethod    
    def register(cls, formData):
        """Create a new user based on form data"""
        username = formData['username']
        password = formData['password']
        email = formData['email']
        first_name = formData['first_name']
        last_name = formData['last_name']
        
        hashed_pwd = bcrypt.generate_password_hash(password)
        
        hashed_utf8 = hashed_pwd.decode('utf-8')
        
        return cls(username=username, password=hashed_utf8, email=email,
                   first_name=first_name, last_name=last_name)
        
    @classmethod
    def authenticate(cls, formData):
        username = formData['username']
        pwd = formData['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False
        
    def hash_password(pwd):
        hashed_passwd = bcrypt.generate_password_hash(pwd)
        return hashed_passwd.decode('utf-8')
        
    def add_user(user):
        db.session.add(user)
        db.session.commit()
        
    def get_user(username):
        """Retrieve a user"""
        return User.query.get_or_404(username)
    
    def get_all_users():
        return User.query.all()
            
    def delete_user():
        ...
        

class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)    
    content = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f"<Feedback title={self.title} content={self.content}>"
    
    def add_feedback():
        ...
    
    def get_feedback(id):
        return Feedback.query.get_or_404(id)
    
    def delete_feedback(id):
        ...