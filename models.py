"""Models for Notes app."""

# from typing import Optional
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User."""

    __tablename__ = "users"

    username = db.Column(db.String(20), 
                            primary_key=True 
                            )
    password = db.Column(db.String(100), 
                            nullable=False
                            )
    email = db.Column(db.String(50), 
                            nullable=False,
                            unique=True
                            )
    first_name = db.Column(db.String(30), 
                            nullable=False
                            )
    last_name = db.Column(db.String(30), 
                            nullable=False
                            )

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register a user with hashed password, add to the session & 
        return user"""

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        new_user = cls(username=username, 
                        password=hashed, 
                        email=email, 
                        first_name=first_name, 
                        last_name=last_name)

        db.session.add(new_user)

        return new_user
    
    @classmethod
    def authenticate_user(cls, username, password):
        """ Validate that user exists & password is correct.
            Return user if valid and false if not.
        """
    
        user = cls.query.get_or_404(username)

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        
        else:
            return False

class Note(db.Model):
    """ Notes"""

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(100),
                    nullable=False)
    content = db.Column(db.Text,
                    nullable=False)
    owner = db.Column(db.Text,
                    db.ForeignKey("users.username"))

    user = db.relationship("User", backref="notes")