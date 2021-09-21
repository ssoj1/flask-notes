"""Flask app for Notes"""

from flask import Flask, jsonify, request, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db
import os

app = Flask(__name__)

API_SECRET_KEY=os.environ['API_SECRET_KEY']

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///users"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.get("/")
def redirect_to_register():
    """Redirect to /register"""

    return redirect("/register")

@app.route("/register", method=["GET" , "POST"])
def register_user():
    """ """

    form = User()

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

        return redirect("/secret")
    
    else: 

        return render_template("register_form.html")

