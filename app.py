"""Blogly application."""

from flask import Flask,request,render_template,redirect,flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db,User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "aasdfjk153825"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

## Part 1
##GET Requests

@app.route('/')
def root():
    """Redirects to list of users"""     
    return redirect('/users')

@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users =User.query.all()
    return render_template('user_list.html', users = users)

@app.route('/users/new')
def show_user_form():      
    return render_template('user_form.html') 

##POST request

@app.route('/users/new', methods = ["POST"])
def create_users():
    first_name = request.form["First Name"]
    last_name = request.form["Last Name"]
    image_url = request.form["Image URL"]

    new_user = User(first_name=first_name, last_name=last_name, 
                    image_url = image_url)
    db.session.add(new_user)
    db.session.commit();

    return redirect('/users')

##Get Requests

@app.route("/<int:user_id>")
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user =user)

@app.route('/users/<int:user_id>/edit')
def show_user_form_edit(user_id):     
    user = User.query.get_or_404(user_id)
    return render_template("user_form_edit.html", user =user)


##Post request

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['First Name']
    user.last_name = request.form['Last Name']
    user.image_url = request.form['Image URL']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

##PART 2

##Get request

@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Shows new post form for user"""

    user = User.query.get_or_404(user_id)
    return render_template("postform.html", user=user)



@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new_post_form(user_id):
    """Handles new post form submission for user"""

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    db.session.add(new_post)
    db.session.commit()
    # flash(f"Post '{new_post.title}' added.")

    return redirect(f"/{user_id}") 

@app.route('/posts/<int:post_id>')
def show_user_post(post_id): 
    """Shows post detail"""    
    post = Post.query.get_or_404(post_id)      
    return render_template("showpost.html", post =post)


@app.route('/posts/<int:post_id>/edit')
def show_post_edit(post_id): 
    """Shows post edit for for user to edit post"""    
    post = Post.query.get_or_404(post_id)      
    return render_template("postformedit.html", post =post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_post_edit(post_id): 
    """Handles edit post form submission"""    
    post = Post.query.get_or_404(post_id)      
    post.title = request.form['title']
    post.content = request.form['content']
    
    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Handle delete form submission"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
   

    return redirect('/users')










   

   

