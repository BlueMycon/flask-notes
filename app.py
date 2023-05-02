from flask import Flask, session, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User

from forms import RegistrationForm, LoginForm, CSRFProtectForm

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

SESSION_KEY = 'username'

"""Flask app for Notes"""

@app.get("/")
def show_homepage():
    """Redirect to Registration."""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """displays and processes the registration form"""
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)
        session[SESSION_KEY] = new_user.username

        db.session.add(new_user)
        db.session.commit()

        return redirect(f"/users/{new_user.username}")

    else:
        return render_template('register.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    """displays and processes the login form"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
    else:
        form.username.errors = ["Bad name/password"]
        return render_template('login.html', form=form)


@app.get('/users/<username>')
def display_user(username):
    """ displays user page """

    if SESSION_KEY not in session or session[SESSION_KEY] != username:
        flash("You must be logged in to view!")
        # TODO: raise Unauthorized error
        return redirect("/")

    form = CSRFProtectForm()
    user = User.query.get_or_404(username)

    return render_template("user_page.html", user=user, form=form)

@app.post("/logout")
def logout_user():
    """Logs out user and redirects to registeration page"""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        # Remove "user_id" if present, but no errors if it wasn't
        session.pop("user_id", None)

    return redirect("/")
