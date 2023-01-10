from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from sqlalchemy.sql import func
# Current user in below import only works because of UserMixin as part of user class
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)  # Allows us to use the views to tell the site where to go


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter(func.lower(User.email).ilike(func.lower(email))).first()
        if not user:
            user = User.query.filter(func.lower(User.username).ilike(func.lower(email))).first()
        if user:
            if check_password_hash(user.password, password):
                flash(f'Welcome back, {user.username}!', category='success')
                login_user(user, remember=True)  # Keeps track of user logged in - by cookie?
                return redirect(url_for('views.index'))
            else:
                flash('Incorrect password. Please try again.', category='error')
        else:
            flash('Email or Username not found. Please try again or create a new account.', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required  # Will not allow us to access this page if no one is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        username_check = User.query.filter(func.lower(User.username).ilike(func.lower(username))).first()
        email_check = User.query.filter(func.lower(User.email).ilike(func.lower(email))).first()
        if email_check:
            flash('That email address is already in use. Please try again.', category='error')
        elif username_check:
            flash('That username is already in use. Please try again.', category='error')
        elif len(email) < 5:
            flash('Invalid email entered.', category='error')
        elif len(username) < 8:
            flash('Username must be at least 8 characters.', category='error')
        elif len(first_name) < 2:
            flash('Length of first name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Length of last name must be greater than 1 character.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif password2 != password1:
            flash('Passwords do not match. Please re-enter.', category='error')
        else:
            new_user = User(email=email, username=username, first_name=first_name, last_name=last_name,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created successfully!', category='success')
            return redirect(url_for('views.index'))

    return render_template('signup.html', user=current_user)
