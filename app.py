"""Flask app for Notes"""

from flask import Flask, jsonify, request, render_template, redirect, session, flash
from flask.templating import render_template_string
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db
from forms import RegisterForm, LogInForm
import os

app = Flask(__name__)

API_SECRET_KEY=os.environ['API_SECRET_KEY']
app.config['SECRET_KEY'] = API_SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///notes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.get("/")
def redirect_to_register():
    """Redirect to /register"""

    return redirect("/register")

@app.route("/register", methods=["GET" , "POST"])
def register_user():
    """ Register user: produce form & handle form submission. """

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()

        session["username"] = username

        return redirect(f"/users/{username}")
    
    else: 

        return render_template("register_form.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def log_in_user():
    """ Produce login form and handle login"""

    form = LogInForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate_user(username, password)

        if user:
            session["username"] = username
            return redirect(f"/users/{username}")
        
        else:
            form.username.errors = ["Bad name/password"]
    
    return render_template("login_form.html", form=form)

@app.get("/users/<username>")
def display_user_details(username):
    """ Displays user details if a user is logged in, otherwise
    redirects to login form"""

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/login")

    else: 
        user = User.query.get_or_404(username)

        if session["username"] == username:
            return render_template("user_detail.html", user=user)
        else: 
            flash("You're not authorized to view that page")
            session_user = session["username"]

            return redirect(f"/users/{session_user}")

