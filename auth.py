from flask import Blueprint, request, flash
from . import db
from flask import Blueprint, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/doctor_login')
def login():
    return 'Login'

@auth.route('/doctor_signin')
def signup():
    return 'Signup'

@auth.route('/doctor_signin', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    return 'Logout'

@auth.route('/doctor_login')
def login():
    return render_template('doctor_login.html')

@auth.route('/doctor_signin')
def signup():
    return render_template('doctor_signin.html')

@auth.route('/doctor_signin', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')   
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))