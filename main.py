from flask import Flask, render_template, request, session, redirect, url_for
from users.manage_users import ManageUsers, User

app = Flask(__name__, template_folder='templates')
app.secret_key = '\xd9J\xde\xec\xb5\'\x08\x89jG\xe3\xb2\x06\xb5\xbf\x88\xe9"\x84e\xd2\xf0\x95\xdd'
user_manager = ManageUsers()

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if 'username' in session: # We were already logged in
        return redirect(url_for('index'))
    if request.method == 'POST': # Someone submitted the form
        if user_manager.login_user(request.form['username'], request.form['password']): # We successfully logged in
            session['username'] = request.form['username']
            return redirect(url_for('index')) # Go to the calendar
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)

@app.route('/register', methods=['POST']) # Only handles the register POST request
def register():
    error = None
    if request.form['password'] != request.form['confirm_password']:
        error = "Passwords don't match"
    new_user = User(Username=request.form['username'], Password=request.form['password'], FirstName=request.form['first_name'], LastName=request.form['last_name'], Email=request.form['email'])
    if user_manager.add_user(new_user):
        session['username'] = request.form['username']
        return redirect(url_for('index')) # Go to the calendar
    else:
        error = "Username is already taken"
    return render_template('login.html', error=error)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session: # We are not logged in
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'signout' in request.form:
            session.pop('username', None)
            return redirect(url_for('login'))

    return render_template('index.html', username=session['username'])