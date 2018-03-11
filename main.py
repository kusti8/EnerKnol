from flask import Flask, render_template, request, session, redirect, url_for, flash, get_flashed_messages, jsonify, abort
from users.manage_users import ManageUsers, User
from el_search.search_manager import MovieItemManager
from elasticsearch_dsl.response import Response
import math

app = Flask(__name__, template_folder='templates')
app.secret_key = '\xd9J\xde\xec\xb5\'\x08\x89jG\xe3\xb2\x06\xb5\xbf\x88\xe9"\x84e\xd2\xf0\x95\xdd'
user_manager = ManageUsers()
movie_manager = MovieItemManager()

PAGE_SIZE = 5

def check_login(): # Checks if the user is logged in
    if 'username' not in session: # We are not logged in
        return redirect(url_for('login'))
    else:
        return None

def sub_one(value): # Used for the index page counter
    value = int(value)
    value -= 1
    if value < 1:
        value = 1
    return str(int(value))

def add_one(value, length):
    value = int(value)
    value += 1
    if value > math.ceil(length/float(PAGE_SIZE)): # Over the page limit
        value = math.ceil(length/float(PAGE_SIZE))
    return str(int(value))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if 'username' in session: # We were already logged in
        return redirect(url_for('index'))

    if request.method == 'POST': # Someone submitted the form
        if user_manager.login_user(request.form['username'], request.form['password']): # We successfully logged in
            session['username'] = request.form['username']
            return redirect(url_for('index')) # Go to the movie search
        else:
            error = 'Invalid username/password'

    errors = get_flashed_messages()
    if errors:
        error = errors[0]
    return render_template('login.html', error=error)

@app.route('/register', methods=['POST']) # Only handles the register POST request
def register():
    error = None
    if request.form['password'] != request.form['confirm_password']:
        error = "Passwords don't match"
    new_user = User(Username=request.form['username'], Password=request.form['password'], FirstName=request.form['first_name'], LastName=request.form['last_name'], Email=request.form['email'])
    if user_manager.add_user(new_user):
        session['username'] = request.form['username']
        return redirect(url_for('index')) # Go to the movie search
    else:
        error = "Username is already taken"
    
    flash(error)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def index():
    def get_length(page):
        min_range = (page-1)*PAGE_SIZE
        max_range = page*PAGE_SIZE
        if max_range > full_length:
            max_range = full_length
        return (min_range, max_range)

    if check_login():
        return check_login()
    
    if request.method == 'POST':
        if 'signout' in request.form:
            session.pop('username', None)
            return redirect(url_for('login'))

    full_length = 0
    page = int(request.args.get('page', '1'))
    if request.args.get('favorites') == 'true':
        movies = [movie_manager.get_movie(i) for i in user_manager.get_favorites(session['username'])]
        full_length = len(movies)
        min_range, max_range = get_length(page)
        movies = movies[min_range:max_range]
    elif request.args.get('q'):
        movies = movie_manager.search(request.args.get('q'), page=page, PAGE_SIZE=PAGE_SIZE)
        full_length = movies.hits.total
    else:
        movies=[]

    user = user_manager.get_info(session['username'])
    name = user.FirstName # Show the first  in the index page
    return render_template('index.html', username=session['username'], name=name, full_length=full_length, movies=movies, Response=Response, sub_one=sub_one, add_one=add_one, isinstance=isinstance, str=str, PAGE_SIZE=PAGE_SIZE, int=int)

@app.route('/item', methods=['GET', 'POST'])
def item():
    if check_login():
        return check_login()

    if request.method == 'GET':
        i = request.args.get('id')
        if not movie_manager.get_movie(i):
            abort(404)
        favorites = user_manager.get_favorites(session['username'])
        f = unicode(movie_manager.get_movie(i)['_id']) in favorites
        return render_template('item.html', movie=movie_manager.get_movie(i), favorite=f)
    else:
        favorite = request.form['favorite'] == 'true'
        user_manager.set_favorite(session['username'], request.form['id'], favorite)
        return 'Success'

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)