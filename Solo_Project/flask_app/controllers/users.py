from flask_app import app
from flask_bcrypt import Bcrypt
from flask import flash
from flask import request, render_template, redirect, session
from flask_app.models.user import User
from flask_app.models.post import Post
from datetime import datetime
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register/user', methods=["POST"])
def register():
    # validate the form here ...
    if not User.validate_user(request.form):
        return redirect('/')
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    # Call the save @classmethod on User
    user_id = User.save(data)
    # store user id into session
    session['user_id'] = user_id
    return redirect("/post_page")

@app.route('/login/user', methods=['POST'])
def login():
    if not User.validate_email(request.form):
        return redirect('/')
    data = { 
            "email" : request.form["email"]
        }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email", 'login')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Password", 'login')
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/post_page")

@app.route('/post_page')
def dash():
    if 'user_id' not in session:
        flash('must sign in first')
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    all_posts = Post.get_all_with_creator()
    return render_template('post.html', user = User.get_one(data), all_posts = all_posts)
@app.route('/post')
def backHome():
    return redirect('/post_page')

@app.route('/logout')
def log():
    session.clear()
    return redirect('/')