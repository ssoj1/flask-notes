"""Flask app for Notes"""

from flask import Flask, jsonify, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import User, Note, db, connect_db
from forms import RegisterForm, LogInForm, LogOutForm, DeleteUserForm, AddOrEditNote
import os

app = Flask(__name__)

SECRET_KEY=os.environ['SECRET_KEY'] 
app.config['SECRET_KEY'] = SECRET_KEY #needed for debug toolbar and session

toolbar = DebugToolbarExtension(app)

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
        db.session.commit()
        flash("User successfully created")

        session["username"] = new_user.username

        return redirect(f"/users/{new_user.username}")
    
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
            session["username"] = user.username
            flash("Successfully logged in")

            return redirect(f"/users/{user.username}")

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

        form = LogOutForm()

        if session["username"] == user.username:
            # breakpoint()
            return render_template("user_detail.html", user=user, form=form)
        else: 
            flash("You're not authorized to view that page")
            session_user = session["username"]

            return redirect(f"/users/{session_user}")

@app.post("/logout")
def log_out_user():
    """ Clears out information from the session and redirects to /"""

    form = LogOutForm()

    if form.validate_on_submit():
        session.pop("username", None)
        flash("Successfully logged out")

    return redirect("/")

@app.post("/users/<username>/delete")
def delete_user_and_notes(username):
    """ Remove the user from the database and also removes all of their notes 
        Clears any user information from the session and redirects to /
    """

    form = DeleteUserForm()

    if form.validate_on_submit():
        user = User.query.get_or_404(username)

        db.session.delete(user)
        db.session.commit()

        session.pop("username", None)
        flash("Successfully deleted user")

        return redirect("/")
    
    return redirect("/")

@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def add_note(username):
    """ Displays a form to add notes and adds a new note
        After adding a new note, redirects to users/<username>
    """
    user = User.query.get_or_404(username)
    form = AddOrEditNote(owner=user.username)
    # obj=user

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        owner = form.owner.data

        new_note = Note(title=title, content=content, owner=owner)
        db.session.add(new_note)
        db.session.commit()

        flash("Successfully added new note")
        return redirect (f"/users/{user.username}")

    return render_template("add_note_form.html", form=form)

@app.route("/notes/<int:note_id>/update", methods=["GET", "POST"])
def update_note(note_id):
    """ Update a note and redirect to /users/username"""

    note = Note.query.get_or_404(note_id)
    user = note.user
    form = AddOrEditNote(obj=note)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        owner = form.owner.data

        update_note = Note(title=title, content=content, owner=owner)
        db.session.add(update_note)
        db.session.commit()

        flash("Successfully updated note")
        return redirect (f"/users/{user.username}")

    return render_template("edit_note_form.html", form=form)