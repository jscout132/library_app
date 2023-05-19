from flask import Blueprint, url_for, render_template, request, redirect, flash, jsonify
from flask_login import login_user

from forms import UserLogin, LibLogin
from models import User, Librarian, Books, check_password_hash

site = Blueprint('site',__name__, template_folder='site_pages')

@site.route('/')
@site.route('/home', methods = ['GET','POST'])
def home():
    books = Books.query.all()
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
                return redirect(url_for('auth.sign_in', form = form, books = books))
    except:
        raise Exception('Invalid form data, please check your information')
    
    return render_template('index.html', form = form, books=books)


@site.route('/books')
def books():
    books = Books.query.all()
    #makes a list of all books that are less than 300 pages
    quick_read = [i.title for i in books if i.length_ < 300]
    qr_isbn = [i.isbn for i in books if i.length_ <300]

    #makes a list of all books published since 2017
    new_books = [i.title for i in books if i.year_published > 2017]
    nb_isbn = [i.isbn for i in books if i.year_published > 2017]

    #makes a set of all genres sorted alphabetically
    genre_set = sorted(set([i.genre for i in books]))
    gs_isbn = sorted(set([i.genre for i in books]))

    book_dict = {
        'quick_read':quick_read,
        'qr_isbn':qr_isbn,
        'new_books':new_books,
        'nb_isbn': nb_isbn,
        'genre_set': genre_set,
        'gs_isbn': gs_isbn
    }
    return render_template('books.html', books = books, **book_dict)


@site.route('/profile')
def profile():
    user = User.query.all()
    return render_template('profile.html', user = user)

@site.route('/librarian')
def librarian():
    books = Books.query.all()
    users = User.query.all()
    return render_template('librarian.html', books = books, users = users)


book_page = Blueprint('book_page', __name__, url_prefix='/books')
@book_page.route('/<isbn>', methods = ['GET'])
def get_books(isbn):
    books = Books.query.get(isbn)
    return render_template('book_page.html', books = books)

@site.route('/genre')
def genre():
    books = Books.query.all()
    genre_set = sorted(set([i.genre for i in books]))        

    return render_template('genre.html', books = books, genre_set = genre_set)