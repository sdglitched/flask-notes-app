from flask import Blueprint, render_template, request, flash


auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<h1>You are logged out</h1>"

@auth.route('/sign-up', methods=['GET','POST'])
def signUp():
    if request.method == 'POST':
        fullName = request.form.get('fullName')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if len(email) < 4:
            flash('Email must be greater than 4 letters', category='error')
        elif len(fullName) < 3:
            flash('Name must be greater than 2 letters', category='error')
        elif (password1 != password2) or len(password1) < 7:
            flash('Password does not match', category='error')
        else:
            flash('Account created', category='success')
    return render_template("signUp.html")