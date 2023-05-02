from flask import Flask, jsonify, redirect, render_template, flash, request
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User

from forms import RegistrationForm, LoginForm

# from forms import NewSongForPlaylistForm, AddSongForm, AddPlaylistForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///notes_app"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

app.config["SECRET_KEY"] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

"""Flask app for Notes"""

@app.get("/")
def show_homepage():
    """Redirect to Registration."""

    return redirect("/register")


@app.route("/register", method=["GET", "POST"])
def register_user():
    """displays and processes the registration form"""
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User(username = username,
                        password = password
                        email = email
                        first_name = first_name
                        last_name = last_name)

        db.session.add(new_user)
        db.session.commit()

        # return redirect

    else:
        return render_template('register.html', form=form)


@app.route("/login", method=["GET", "POST"])
def login_user():
    """displays and processes the login form"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        return redirect(f"/users/{username}")

    else:
        return render_template('login.html', form=form)


@app.get('/users/<username>')
def display_user(username):
    """ displays user page """

    user = User.query.get_or_404(username)

    return render_template("user_page.html", user=user)