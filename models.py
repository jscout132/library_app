from flask import session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow
import secrets

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()
sess = Session()

@login_manager.user_loader
def load_user(user_id):
    if session['account_type'] == 'User':
        return User.query.get(user_id)
    elif session['account_type'] == 'Librarian':
        return Librarian.query.get(user_id)

#creates user database
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    fname = db.Column(db.String(150), nullable=True, default='')
    lname =  db.Column(db.String(150), nullable=True, default='')
    phone = db.Column(db.String(25), nullable=True, default='')
    email = db.Column(db.String(200), nullable=False, default='')
    password = db.Column(db.String, nullable=False, default='')
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)

    def __init__(self, fname='', lname='', phone='', email='', password='', token=''):
        self.id = self.set_id()
        self.fname = fname
        self.lname = lname
        self.phone = phone
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(6)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pass_hash = generate_password_hash(password)
        return self.pass_hash
    
    def set_token(self, length):
        return secrets.token_hex(length)
    
    def __repr__(self):
        return f'User {self.email} has been added to the database'

#creates the librarians database
class Librarian(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True, unique = True, default='')
    lib_fname = db.Column(db.String(150), default = '')
    lib_lname = db.Column(db.String(150), default = '')
    lib_email = db.Column(db.String(150), nullable = False, default = '')
    lib_password = db.Column(db.String, nullable = False, default='')    

    def __init__(self, id = '', lib_fname = '', lib_lname='', lib_email='', lib_password=''):
        self.id = id
        self.lib_fname = lib_fname
        self.lib_lname = lib_lname
        self.lib_email = lib_email
        self.lib_password = self.set_lib_password(lib_password)

    def set_lib_password(self, password):
        return generate_password_hash(password)

    def __repr__(self):
        return f'{self.lib_fname} has been added'

#creates the books database
class Books(db.Model, UserMixin):
    isbn = db.Column(db.String(20), default='', primary_key = True)
    title = db.Column(db.String(400), default='')
    author_fname = db.Column(db.String(150), default='')
    author_lname = db.Column(db.String(150), default='')
    length_ = db.Column(db.Integer)
    genre = db.Column(db.String(150))
    binding = db.Column(db.String(10))
    quantity = db.Column(db.Integer)
    year_published = db.Column(db.Integer)
    lib_id = db.Column(db.String, db.ForeignKey('librarian.id'))
    

    def __init__(self, isbn, title, author_fname, author_lname, length_, genre, binding, quantity, year_published, lib_id):
        self.isbn = isbn
        self.title = title
        self.author_fname = author_fname
        self.author_lname = author_lname
        self.length_ = length_
        self.genre = genre
        self.binding = binding
        self.quantity = quantity
        self.year_published = year_published
        self.lib_id = lib_id

    def __repr__(self):
        return f'{self.title} has been added to the database'
    
class BookStatus(db.Model, UserMixin):
    trans_id = db.Column(db.String, primary_key=True)
    checkout_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    isbn = db.Column(db.String, db.ForeignKey('books.isbn'), nullable = False)
    id = db.Column(db.String, db.ForeignKey('user.id'), nullable = False)
    
    def __init__(self, trans_id, checkout_date, due_date, isbn, id):
        self.trans_id = trans_id
        self.checkout_date = checkout_date
        self.due_date = due_date
        self.isbn = isbn
        self.id = id

    def __repr__(self):
        return f'{self.trans_id} has been added to the database'
    

# still need to add some schemas from marshmallow down here
class BookSchema(ma.Schema):
    class Meta:
        fields = ['isbn', 
                  'title', 
                  'author_fname',
                  'author_lname',
                  'length_',
                  'genre', 
                  'binding',
                  'quantity',
                  'year_published',
                  'lib_id']
        
book_schema = BookSchema()
books_schema = BookSchema(many = True)

class LibSchema(ma.Schema):
    class Meta:
        fields = ['id',
                  'lib_fname',
                  'lib_lname',
                  'lib_email',
                  'lib_password']
        
lib_schema = LibSchema()


class UserSchema(ma.Schema):
    class Meta:
        fields=['id',
                'fname',
                'lname',
                'phone',
                'email',
                'token',
                'date_created']

user_schema = UserSchema()
users_schema = UserSchema(many=True)