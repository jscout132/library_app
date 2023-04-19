from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_user, logout_user, LoginManager, current_user

from forms import CreateUser, UserLogin, LibLogin
from models import db, check_password_hash, User, Librarian

auth = Blueprint('auth',__name__, template_folder='auth_templates')

@auth.route('/sign_up', methods = ['GET','POST'])
def sign_up():
    session['account_type'] = 'User'
    form = CreateUser()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            fname = form.fname.data
            lname = form.lname.data
            phone = form.phone.data
            email = form.email.data
            password = form.password.data

            user = User(fname = fname, lname = lname, phone = phone, email = email, password = password)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('site.home'))

    except:
        raise Exception('Invalid form data, please check your form')
    return render_template('sign_up.html', form=form)
        
@auth.route('/sign_in', methods = ['GET', 'POST'])
def sign_in():
    session['account_type'] = 'User'
    form = UserLogin()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                print(f'{email} logged in now')
                return redirect(url_for('site.profile'))
            else:
                return redirect(url_for('auth.sign_in', form = form))
    except:
        raise Exception('Invalid form data, please check your information')
    
    return render_template('sign_in.html', form = form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))

@auth.route('/lib_login', methods = ['GET', 'POST'])
def lib_login():
    session['account_type'] = 'Librarian'
    form = LibLogin()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            lib_email = form.lib_email.data
            lib_password = form.lib_password.data

            logged_user = Librarian.query.filter(Librarian.lib_email == lib_email).first()
            print('logged user',logged_user.lib_fname)
            print('logged user id', logged_user.id)
            if logged_user and check_password_hash(logged_user.lib_password, lib_password):
                login_user(logged_user)
                print(f'{lib_email} logged in now')
                return redirect(url_for('site.librarian'))
            else:
                return redirect(url_for('auth.lib_login', form = form))
    except:
        raise Exception('Invalid form data, please check your information')
    
    return render_template('lib_login.html', form = form)



