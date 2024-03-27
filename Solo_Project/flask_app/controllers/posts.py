from flask_app import app
from flask_bcrypt import Bcrypt
from flask import flash
from flask import request, render_template, redirect, session
from flask_app.models.user import User
from flask_app.models.post import Post

bcrypt = Bcrypt(app)


@app.route("/user/post", methods = ['POST'])
def content_insert():
    if not Post.validate_content(request.form):
        return redirect('/post_page')
    Post.insert(request.form)
    print('hello')
    return redirect('/post_page')

@app.route('/delete/<int:post_id>/')
def deleted(post_id):
    data = {
        'id': post_id
    }
    Post.delete(data)
    return redirect('/post_page')
@app.route("/likes/<int:post_id>/<int:user_id>/<int:id>")
def add(post_id, user_id, id):
    data_one = {
        "post_id": post_id
    }
    data_two = {
        "post_id": post_id,
        "user_id": user_id
    }
    data_three = {
        "post_id": post_id
    }
    user_in_db = Post.likes_db(data_one)
    if session['user_id'] == id:
        print("cannot like your own post!")
        return redirect('/post_page')
    elif user_in_db == user_id:
        print(user_id)
        print(user_in_db)
        return redirect("/post_page")
    Post.add_likes(data_two)
    Post.add_one(data_three)
    return redirect('/post_page')
@app.route("/display/<int:post_id>/<int:id>")
def display(post_id, id):
    data = {
        "id": post_id
    }
    posts = Post.get_all_with_one(data)
    content = Post.get_post(data)
    dat = {
        'id' : id
    }
    user = User.get_one(dat)
    return render_template('display.html', posts = posts,user = user, content = content)
@app.route('/info/<int:user_id>')
def info( user_id):
    dat = {
        'id' : user_id
    }
    user = User.get_one(dat)
    # posts = Post.get_all_with_one(data)
    post = Post.get_all_with_posts(dat)
    posts = Post.get_all_with_likes(dat)
    return render_template('info.html', user = user, post = post, posts = posts)

