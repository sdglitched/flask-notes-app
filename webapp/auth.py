from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from webapp import db

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged In', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password', category='error')
        else:
            flash('Incorrect Email', category='error')
    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def signUp():
    if request.method == 'POST':
        fullName = request.form.get('fullName')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists! Try another one.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 letters', category='error')
        elif len(fullName) < 3:
            flash('Name must be greater than 2 letters', category='error')
        elif (password1 != password2) or len(password1) < 7:
            flash('Password does not match', category='error')
        else:
            user = User(email=email, fullName=fullName, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created', category='success')
            return redirect(url_for('views.home'))
    return render_template("signUp.html", user = current_user)