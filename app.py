from flask import Flask, render_template, redirect, session, request
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegistrationForm, LoginForm, FeedbackForm
from models import connect_db, User, Feedback

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'yummy'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def index():
    if session.get('username'):
        return redirect('/secret')
    else:
        return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def show_register_form():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        new_user = User.register(form)
        User.add_user(new_user)
        
        session['username'] = new_user.username
        
        return redirect(f'/users/{new_user.username}')
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.authenticate(form)
        
        if user:
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username or password']
            return redirect('/login')
    else:
        return render_template('login.html', form=form)
    
# @app.route('/secret')
# def show_secret():
#     if session.get('username'):
#         return '<h1>You made it!</h1>'
#     else:
#         return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')
    
@app.route('/users/<username>')
def show_user_info(username):
    if session.get('username'):
        user = User.get_user(username)
        return render_template('user_info.html', user=user)
    else:
        return redirect('/')