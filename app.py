"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

#flask debugtoolbar settings
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app) 

connect_db(app)
db.create_all()

#ROUTES
@app.route('/') 
def homepage(): 
    """ Redirect to list of users. (We'll fix this in a later step). """
    # return render_template("home.html")
    return redirect('/users')

@app.route('/users')
def list_user():
    """ 
        Show all users.
        Make these links to view the detail page for the user.
        Have a link here to the add-user form.
    """
    users = User.query.all()
    return render_template("users.html", users = users)

@app.route('/users/new')
def new_user():
    """ Show an add form for users"""
    return render_template("new_user_form.html")

@app.route('/users/new', methods=["POST"]) 
def post_user():
    """ Process the add form, adding a newly created user and going back to /users"""
    first_name = request.form["first_name"]
    last_name = request.form.get("last_name")
    img_url = request.form.get("img_url")
    # create user model instance
    new_user = User(first_name=first_name, last_name=last_name,img_url=img_url)
    # commit the new user to the psql database thanx to SQLALCHEMY
    
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def detail_user(user_id):
    """ 
        Show information about the given user.
        Have a button to get to their edit page,
          and a button to delete the user.
    """
    user = User.query.get_or_404(user_id)
    return render_template("details_user.html", user=user)

@app.route('/users/<int:user_id>/edit')
def show_user_edit_page(user_id):
    """
        Show the edit page for a user.
        Have a cancel button that returns to the detail page for a user,
          and a save button that updates the user.
    """
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_the_user(user_id):
    """Process the edit form, returning the user to the /users page."""
    edit_first_name = request.form["first_name"]
    edit_last_name = request.form["last_name"]
    edit_img_url = request.form["img_url"]
    
    editing_user = User.query.get_or_404(user_id)

    editing_user.first_name = edit_first_name
    editing_user.last_name = edit_last_name
    editing_user.img_url = edit_img_url
    
    db.session.add(editing_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_the_user(user_id):
    """Delete The User"""
    db.session.delete(User.query.get_or_404(user_id))
    db.session.commit()
    return redirect("/users")
