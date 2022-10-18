# Flask Feedback

## Step 0: Set Up Environment

- [x] Make a venv
- [ ] Install packages
- [ ] Create a repo and post it to GitHub
- [x] Make a .gitignore
- [ ] Update requirements.txt

## Step 1: Create User Model

- Make a User model for SQLAlchemy:
  - [ ] username - unique PK, no longer than 20 characters
  - [ ] password - non-nullable text column
  - [ ] email - non-nullable unique column no long that 50 characters
  - [ ] first_name - non-nullable column no longer than 30 characters
  - [ ] last_name - non-nullable column no longer than 30 characters

## Step 2: Make a Base Template

- [x] Make a base template with slots for page title and content
- [x] Use Bootstrap, don't worry too much about styling

## Step 3: Make Routes

- [ ] **GET /**
  - [ ] Redirect to /register
- [ ] **GET /register**
  - [ ] Show a form that, when submitted, will register a user
  - [ ] Should accept a username, password, email, first name, and last name
  - [ ] Use WTForms
  - [ ] Password input should hide characters
- [ ] **POST /register**
  - [ ] Process registration form by adding user
  - [ ] Redirect to /secret
- [ ] **GET /login**
  - [ ] Show a login form
  - [ ] Should accept a username and password
  - [ ] Be sure to use WTForms and hide password input
- [ ] **POST /login**
  - [ ] Process login form, making sure user is authenticated and going to /secret if they are
- [ ] **GET /secret**
  - [ ] Return text 'You made it!' (to be changed)

## Step 4: Restrict Access to /secret

- [ ] Protect route for /secret and make sure only logged in users can access it
- [ ] Whenever a user logs in after having registered, store info in session
- [ ] After user successfully logs in or registers, store their username in session

## Step 5: Log Out Users

- **GET /logout**
  - Clear info from session and redirect to /

## Step 6: Change /secret to /users/<user_name>

- After user logs in take them to...
- [ ] **GET /users/<user_name>**
  - [ ] Display a template that shows info about the user (everything but the password)
  - [ ] Only logged in users should be able to access this page!

## Step 7: Give Some Feedback

- [ ] Create a Feedback model in models.py
  - [ ] id - unique PK that's an auto-incrementing integer
  - [ ] title - non-nullable text column that's at most 100 characters
  - [ ] content - non-nullable text column
  - [ ] username - FK referencing username column

## Step 8: Make/Modify Routes for Users and Feedback

- [ ] **GET /users/<user_name>**
  - [ ] Show info about the user
  - [ ] Show all of the feedback the user's given
  - [ ] For each piece of feedback, display a link to a form to edit the feedback and a button to delete it
- [ ] **POST /users/<username>/delete**
  - [ ] Remove the user from the DB and delete all of their feedback
  - [ ] Clear any user info in the session and redirect to /
  - [ ] Only the user who's logged in can delete their account!
- [ ] **GET /users/<username>/feedback/add**
  - [ ] Display a form to add feedback
  - [ ] Only users who are logged in can see this form!
- [ ] **POST /users/<username>/feedback/add**
  - [ ] Add a new piece of feedback and redirect to /users/<username>
  - [ ] Only users who are logged in can use this route!
- [ ] **GET /users/<feedback-id>/update**
  - [ ] Display form to edit feedback
  - [ ] Only users who've written feedback should be able to see this form!
- [ ] **POST /users/<feedback-id>/update**
  - [ ] Update specified piece of feedback
  - [ ] Redirect to /users/<username>
  - [ ] Only users who've written feedback should be able to update it
- [ ] **POST /users/<feedback-id>/delete**
  - [ ] Delete specified piece of feedback
  - [ ] Redirect to /users/<username>
  - [ ] Only the user who wrote the feedback should be able to delete it

## Further Study

- Make sure registration and authentication logic is handled in models.py
- Don't let users see the registration or login forms if there's already a username in session
- Add a 404 page when a user or feedback can't be found
- Add a 401 page when users aren't authenticated or not authorized
- Add a boolean column to users table called is_admin which defaults to false
  - If user's an admin, they should be able to add, update, or delete feedback for any user and delete users
- 

## Takeaways