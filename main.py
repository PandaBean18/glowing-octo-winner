from flask import Flask 
from markupsafe import escape
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask import session
from users import *

app = Flask(__name__)
app.secret_key = b'3bbeb23b5e850898a4b872c5908302899d3fa8f63cda539cd2ce03205531346a'

def current_user():
    if session.get('session_token'): 
        return User.find_by_session_token(session.get('session_token'))
    else: 
        return None 

@app.route("/users/<id>")
def users_show(id):
    user = User.find_by_id(int(id))
    if user: 
        return f"<p>Hello, {user.username}</p>"
    else: 
        return "<p>Hello, World!</p>"

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/users/new", methods=['POST', 'GET'])
def new_user():
    if request.method == 'GET':
        return render_template('new_user.html')
    else: 
        username = request.form['user[name]']
        password = request.form['user[pass]']

        user = User(username, password).create()
        return redirect(f"/users/{user.id}")

@app.route("/login", methods=['POST', 'GET'])
def login(): 
    if current_user() == None:
        if request.method == 'GET':
            return render_template('login.html')
        else: 
            username = request.form['user[username]']
            password = request.form['user[pass]']

            user = User.find_by_credentials(username, password)

            if user: 
                session_token = user.reset_session_token()
                session['session_token'] = session_token
                return redirect(f"/users/{user.id}")
            
    else: 
        return redirect(f"/users/{current_user().id}")

@app.route("/logout")
def logout(): 
    session['session_token'] = None 
    return redirect('/login')

