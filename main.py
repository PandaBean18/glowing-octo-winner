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

# find the current user 
def current_user():
    if session.get('session_token'): 
        return User.find_by_session_token(session.get('session_token'))
    else: 
        return None 

#home route 
@app.route("/")
def hello_world():
    posts = Post.all()
    return render_template('home.html', posts=posts, current_user=current_user())

# session routes 
# new session
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

# destroy session
@app.route("/logout")
def logout(): 
    current_user().reset_session_token()
    session['session_token'] = None 
    return redirect('/login')


# user routes 
# show user 
@app.route("/users/<id>")
def user_show(id):
    user = User.find_by_id(int(id))
    if user: 
        return render_template('user_show.html', user=user, current_user=current_user())
    else: 
        return redirect('/')

#create user
@app.route("/users/new", methods=['POST', 'GET'])
def new_user():
    if current_user() == None:
        if request.method == 'GET':
            return render_template('new_user.html')
        else: 
            username = request.form['user[name]']
            password = request.form['user[pass]']

            user = User(username, password).create()
            return redirect(f"/users/{user.id}")
    else:
        return redirect(f"/users/{current_user().id}")

# post routes 
# post show
@app.route("/posts/<id>")
def post_show(id): 
    post = Post.find_by_id(int(id)) 
    if post: 
        return render_template('post_show.html', post=post, current_user=current_user())
    else: 
        return redirect('/')

# create post
@app.route("/posts/new", methods=['POST', 'GET'])
def new_post():
    if current_user():
        if request.method == 'GET':
            return render_template('new_post.html', current_user=current_user())
        else: 
            author_id = current_user().id 
            title = request.form['post[title]']
            body = request.form['post[desc]']
            post_id = Post(title, body, author_id).create().id
            return redirect(f'/posts/{post_id}')
    else: 
        return redirect(f"/login")

# delete a post
@app.route("/posts/<id>/destroy", methods=['POST'])
def delete_post(id): 
    id = int(id)
    post = Post.find_by_id(id)
    if current_user() and current_user().id == post.author_id: 
        if request.form["_method"] == 'DELETE': 
            Post.destroy(id)
            return redirect("/")
    else: 
        return redirect("/")

@app.route("/posts/<id>/edit", methods=['GET', 'POST'])
def edit_post(id): 
    id = int(id)
    post = Post.find_by_id(id)
    if current_user() and current_user().id == post.author_id: 
        if request.method == 'GET': 
            return render_template("edit_post.html", post=post, current_user=current_user())
        else: 
            print(1)
            attributes = {}
            attributes['title'] = request.form['post[title]']
            attributes['body'] = request.form['post[body]']

            if Post.update(id, attributes): 
                print(2)
                return redirect(f'/posts/{id}')
            else: 
                print(3)
                return redirect(f'/posts/{id}/edit')
    else: 
        return redirect(f'/posts{id}')
    

# creating new snippets 
@app.route("/posts/<post_id>/snippets/new", methods=['GET', 'POST'])
def new_snippet(post_id): 
    from snippets import Snippet
    post_id = int(post_id)
    if current_user(): 
        if request.method == 'GET':
            return render_template("new_snippet.html", post_id=post_id, current_user=current_user())
        else:
            language = request.form['snippet[language]']
            content = request.form['snippet[content]']
            author_id = current_user().id 
            snippet = Snippet(language, content, post_id, author_id).create()
            print(r'{}'.format(snippet.content))
            return redirect(f'/posts/{post_id}')
    


