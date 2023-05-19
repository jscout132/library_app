from flask import Blueprint, request, jsonify

from helpers import token_required
from models import Books, Librarian, db, book_schema, books_schema, lib_schema, User, users_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/addbook', methods = ['POST'])
@token_required
def addbooks(current_user_token):
    isbn = request.json['isbn']
    title = request.json['title']
    author_fname = request.json['author_fname']
    author_lname = request.json['author_lname']
    length_ = request.json['length_']
    genre = request.json['genre']
    binding = request.json['binding']
    quantity = request.json['quantity']
    year_published = request.json['year_published']
    lib_id = current_user_token.id

    new_book = Books(isbn = isbn,
                     title = title,
                     author_fname= author_fname,
                     author_lname=author_lname,
                     length_=length_,
                     genre=genre,
                     binding=binding,
                     quantity=quantity,
                     year_published=year_published,
                     lib_id = lib_id)
    
    db.session.add(new_book)
    db.session.commit()
    response = book_schema.dump(new_book)
    return jsonify(response)


@api.route('/books',methods=['GET'])
def get_books():
    books = Books.query.all()
    response = books_schema.dump(books)
    return jsonify(response)

@api.route('/single-book/<isbn>',methods=['GET'])
def get_book(isbn):
    book = Books.query.get(isbn)
    response = book_schema.dump(book)
    return jsonify(response)

@api.route('addlib', methods = ['POST'])
def add_lib():
    id = request.json['id']
    lib_fname = request.json['lib_fname']
    lib_lname = request.json['lib_lname']
    lib_email = request.json['lib_email']
    lib_password = request.json['lib_password']

    new_lib = Librarian(
        id = id,
        lib_fname=lib_fname,
        lib_lname=lib_lname,
        lib_email=lib_email,
        lib_password=lib_password
    )

    db.session.add(new_lib)
    db.session.commit()
    response = lib_schema.dump(new_lib)
    return jsonify(response)

@api.route('/books/<isbn>', methods = ['POST', 'PUT'])
@token_required
def update_book(current_user_token, isbn):
    book = Books.query.get(isbn)
    book.title = request.json['title']
    book.author_fname = request.json['author_fname']
    book.author_lname = request.json['author_lname']
    book.length_ = request.json['length_']
    book.genre = request.json['genre']
    book.binding = request.json['binding']
    book.quantity = request.json['quantity']
    book.year_published = request.json['year_published']
    book.lib_id = current_user_token.id

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)


#deletes book by isbn
@api.route('/books/<isbn>', methods = ['DELETE'])
@token_required
def del_book(current_user_token, isbn):
    books = Books.query.get(isbn)
    db.session.delete(books)
    db.session.commit()
    response = book_schema.dump(books)
    return jsonify(response)


#show users
@api.route('/users', methods = ['GET'])
def show_users():
    user = User.query.all()
    response = users_schema.dump(user)
    return jsonify(response)



