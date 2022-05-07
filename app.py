from project.utils import loginUtil
from project.utils import utility
from flask_login import LoginManager
from flask import Flask, flash
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user
from flask import render_template, redirect, url_for, session
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import time
import os
from flask_login import UserMixin

template_dir = os.path.abspath('project/templates/')
static_dir = os.path.abspath('project/static/')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config.from_object(loginUtil.Config)
bootstrap = Bootstrap4(app)

# login_manager needs to be initiated before running the app
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80))
    password_hash = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(80))
    location = db.Column(db.String(80))
    __table_args__ = {'schema':'snipnshop'}

    def __init__(self, email, firstname, lastname, password, gender, location):
        self.email = email
        self.set_password(password)
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.location = location

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class RegisterTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    register_time = db.Column(db.Integer)
    email = db.Column(db.String(80), db.ForeignKey(User.email))
    __table_args__ = {'schema':'snipnshop'}

    def __init__(self, email):
        self.email = email
        self.register_time = time.time()


class LoginTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_time = db.Column(db.Integer)
    email = db.Column(db.String(80), db.ForeignKey(User.email))
    __table_args__ = {'schema':'snipnshop'}

    def __init__(self, email):
        self.email = email
        self.login_time = time.time()


db.create_all()
db.session.commit()


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/home')
def home_redirect():
    return render_template('home.html')


@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')


@app.route('/demo')
def demo():
    return render_template('demo.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = loginUtil.LogInForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = User.query.filter_by(email=email).first()

        # Login and validate the user.
        if user is not None and user.check_password(password):
            login_user(user)
            session['loginsuccess'] = True
            session['firstname'] = user.firstname
            session['lastname'] = user.lastname
            session['location'] = user.location
            session['gender'] = user.gender
            session['email'] = user.email
            return redirect(url_for('home'))
        else:
            flash('Invalid email and password combination!')
    return render_template('login.html', form=login_form)


@app.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    return render_template('home.html', session=session)


@app.route("/register", methods=['GET', 'POST'])
def register():
    # https://flask.palletsprojects.com/en/2.1.x/patterns/wtforms/
    registration_form = loginUtil.RegistrationForm()
    if registration_form.validate_on_submit():
        email = registration_form.email.data
        password = registration_form.password.data
        firstname = registration_form.firstname.data
        lastname = registration_form.lastname.data
        gender = registration_form.gender.data
        location = registration_form.location.data
        user_count = User.query.filter_by(email=email).count()

        if (user_count > 0):
            flash('Error - Existing user : ' + email)
        else:
            user = User(email, firstname, lastname, password, gender, location)
            rt = RegisterTime(email)
            db.session.add(user)
            db.session.commit()
            db.session.add(rt)
            db.session.commit()
            flash('Thanks for registering!')
            return redirect(url_for('login'))
    return render_template('register.html', form=registration_form)


@app.route("/reset_password")
def reset():
    return render_template('reset_password.html')


@app.route("/change_password")
def change_password():
    return render_template('change_password.html')


@app.route("/my_profile")
@login_required
def my_profile():
    return render_template('my_profile.html',firstname=session['firstname'], lastname = session['lastname'],\
                           location= session['location'], gender=session['gender'], email = session['email'])


@app.route("/edit_profile")
@login_required
def edit_profile():
    return render_template('edit_profile.html',firstname=session['firstname'], lastname = session['lastname'],\
                           location= session['location'], gender=session['gender'], email = session['email'])


@app.route("/download")
def download():
    return render_template('download.html')


@app.route("/pricing")
def pricing():
    return render_template('pricing.html')


@app.route("/about")
def about():
    images, urls, names, designations = utility.get_team()
    return render_template('about_us.html', images=images,
                           urls=urls, names=names, designts=designations)


@app.errorhandler(401)
def re_route(e):
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host='0.0.0.0', port=5000, debug=True)
