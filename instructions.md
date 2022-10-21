# Flask Feedback

## Step 0: Set Up Environment

- [x] Make a venv
- [x] Install packages
- [x] Create a repo and post it to GitHub
- [x] Make a .gitignore
- [x] Update requirements.txt

## Step 1: Create User Model

- Make a User model for SQLAlchemy:
  - [x] username - unique PK, no longer than 20 characters
  - [x] password - non-nullable text column
  - [x] email - non-nullable unique column no longer that 50 characters
  - [x] first_name - non-nullable column no longer than 30 characters
  - [x] last_name - non-nullable column no longer than 30 characters

## Step 2: Make a Base Template

- [x] Make a base template with slots for page title and content
- [x] Use Bootstrap, don't worry too much about styling

## Step 3: Make Routes

- [x] **GET /**
  - [x] Redirect to /register
- [ ] **GET /register**
  - [x] Show a form that, when submitted, will register a user
  - [x] Should accept a username, password, email, first name, and last name
  - [x] Use WTForms
  - [x] Password input should hide characters
- [x] **POST /register**
  - [x] Process registration form by adding user
  - [x] Redirect to /secret
- [x] **GET /login**
  - [x] Show a login form
  - [x] Should accept a username and password
  - [x] Be sure to use WTForms and hide password input
- [x] **POST /login**
  - [x] Process login form, making sure user is authenticated and going to /secret if they are
- [x] **GET /secret**
  - [x] Return text 'You made it!' (to be changed)

## Step 4: Restrict Access to /secret

- [x] Protect route for /secret and make sure only logged in users can access it
- [x] Whenever a user logs in after having registered, store info in session
- [x] After user successfully logs in or registers, store their username in session

## Step 5: Log Out Users

- **GET /logout**
  - Clear info from session and redirect to /

## Step 6: Change /secret to /users/<user_name>

- After user logs in take them to...
- [x] **GET /users/<user_name>**
  - [x] Display a template that shows info about the user (everything but the password)
  - [x] Only logged in users should be able to access this page!

## Step 7: Give Some Feedback

- [x] Create a Feedback model in models.py
  - [x] id - unique PK that's an auto-incrementing integer
  - [x] title - non-nullable text column that's at most 100 characters
  - [x] content - non-nullable text column
  - [x] username - FK referencing username column

## Step 8: Make/Modify Routes for Users and Feedback

- [x] **GET /users/<user_name>**
  - [x] Show info about the user
  - [x] Show all of the feedback the user's given
  - [ ] For each piece of feedback, display a link to a form to edit the feedback and a button to delete it
- [x] **POST /users/<username>/delete**
  - [x] Remove the user from the DB and delete all of their feedback
  - [x] Clear any user info in the session and redirect to /
  - [x] Only the user who's logged in can delete their account!
- [x] **GET /users/<username>/feedback/add**
  - [x] Display a form to add feedback
  - [x] Only users who are logged in can see this form!
- [x] **POST /users/<username>/feedback/add**
  - [x] Add a new piece of feedback
  - [x] Redirect to /users/<username>
  - [x] Only users who are logged in can use this route!
- [x] **GET /users/<feedback-id>/update**
  - [x] Display form to edit feedback
  - [x] Only users who've written feedback should be able to see this form!
- [x] **POST /users/<feedback-id>/update**
  - [x] Update specified piece of feedback
  - [x] Redirect to /users/<username>
  - [x] Only users who've written feedback should be able to update it
- [x] **POST /users/<feedback-id>/delete**
  - [x] Delete specified piece of feedback
  - [x] Redirect to /users/<username>
  - [x] Only the user who wrote the feedback should be able to delete it

## Further Study

- [x] Make sure registration and authentication logic is handled in models.py
- [x] Don't let users see the registration or login forms if there's already a username in session
- [x] Add a 404 page when a user or feedback can't be found
- [ ] Add a 401 page when users aren't authenticated or not authorized
- [x] Add a boolean column to users table called is_admin which defaults to false
  - [ ] If user's an admin, they should be able to add, modify, or delete feedback for any user and delete users
- 

## Takeaways

- When hashing a password to store in the DB, make sure you decode it to UTF-8 so you don't have to deal with invalid salt errors
- Static methods are your friend
- Keep using different branches!
- Learn how to arrange elements in Bootstrap (including navbar)
- Create separate folders in templates for each template subtype

```python
...
  return render_template('/users/login.html')
```

- Logout should be a POST request, not a GET
- You can reference session in any Jinja template
- Specify the variable type in route definitions when possible, it'll save you a lot of headaches later
