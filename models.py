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
    is_admin = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"<User username='{self.username}' email='{self.email}' first_name='{self.first_name}' last_name='{self.last_name}'>"

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
        
    @staticmethod
    def hash_password(password):
        """Helper method for seed"""
        return bcrypt.generate_password_hash(password).decode('utf-8')
        
    @staticmethod
    def add(user):
        db.session.add(user)
        db.session.commit()
        
    @staticmethod
    def get(username):
        """Retrieve a user"""
        return User.query.get_or_404(username)
    
    @staticmethod
    def get_all():
        return User.query.all()
    
    @staticmethod
    def delete(username):
        User.query.filter_by(username=username).delete()
        db.session.commit()
        
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
        

class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)    
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, db.ForeignKey('users.username', 
                                                ondelete='CASCADE', 
                                                onupdate='CASCADE'))
    
    user = db.relationship('User', backref='feedback')
    
    def __repr__(self):
        return f"<Feedback title='{self.title}' content='{self.content}' username='{self.username}'>"
    
    @staticmethod
    def add(username, formData):
        title = formData['title']
        content = formData['content']
        feedback = Feedback(username=username, title=title, content=content)
        
        db.session.add(feedback)
        db.session.commit()
    
    @staticmethod
    def get(id):
        return Feedback.query.get_or_404(id)
    
    @staticmethod
    def edit(id, formData):
        feedback = Feedback.get(id)
        
        feedback.title = formData.get('title')
        feedback.content = formData.get('content')
        
        db.session.add(feedback)
        db.session.commit()
    
    @staticmethod
    def delete(id):
        Feedback.query.filter_by(id=id).delete()
        db.session.commit()