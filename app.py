from flask import Flask, render_template, redirect, session, request
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegistrationForm, LoginForm, FeedbackForm
from models import connect_db, User, Feedback

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'yummy'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def index():
    if session.get('username'):
        return redirect('/users')
    else:
        return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def registration_form():
    """Show the registration form and handle its submission"""
    if session.get('username'):
        return redirect('/users')
    else:
        form = RegistrationForm()
        
        if form.validate_on_submit():        
            formData = {
                'username': form.username.data, 'password': form.password.data,
                'email': form.email.data, 'first_name': form.first_name.data,
                'last_name': form.last_name.data}
            
            new_user = User.register(formData)
            User.add(new_user)
            
            session['username'] = new_user.username
            
            return redirect(f'/users/{new_user.username}')
        
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle displaying login form and processing it"""
    if session.get('username'):
        return redirect('/users')
    else:
        form = LoginForm()
        
        if form.validate_on_submit():
            formData = {'username': form.username.data, 'password': form.password.data}
            user = User.authenticate(formData)
            
            if user:
                session['username'] = user.username
                return redirect(f'/users/{user.username}')
            else:
                form.username.errors = ['Invalid username or password']
                # return redirect('/login')
        
        return render_template('login.html', form=form)

# No longer needed
"""@app.route('/secret')
def show_secret():
    if session.get('username'):
        return '<h1>You made it!</h1>'
    else:
        return redirect('/')"""

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')

@app.route('/users')
def show_users():
    users = User.get_all()
    
    if session.get('username'):
        return render_template('users.html', users=users)

    return redirect ('/')
    
@app.route('/users/<username>')
def show_user_info(username):
    if session.get('username'):
        user = User.get(username)
        return render_template('user_info.html', user=user)
    else:
        return redirect('/')

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    # Delete user if they're logged in and redirect to home
    if session.get('username') == username:
        User.delete(username)
        session.pop('username')

    return redirect('/')
    
"""Feedback routes"""
    
@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    form = FeedbackForm()
    
    if session.get('username'):
        if form.validate_on_submit():
            formData = {'title': form.title.data, 'content': form.content.data}
            
            Feedback.add(username, formData)
            
            return redirect(f'/users/{username}')
        else:
            user = User.get(username)
            return render_template('add_feedback.html', user=user, form=form)
    else:
        return redirect('/')
    
@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    feedback = Feedback.get(feedback_id)
    form = FeedbackForm(obj=feedback)
    
    if session.get('username') and feedback.username == session.get('username'):
        if form.validate_on_submit():
            formData = {'title': form.title.data, 'content': form.content.data}
            Feedback.edit(feedback_id, formData)
            return redirect(f'/users/{feedback.username}')
        else:
            return render_template('edit_feedback.html', form=form, feedback=feedback)
    else:
        return redirect('/')
    
@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.get(feedback_id)    
    print('Bloop')
    
    if session.get('username') and feedback.username == session.get('username'):
        Feedback.delete(feedback_id)
        
    return redirect('/')