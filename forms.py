from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, DateField
from wtforms.validators import DataRequired, Email

class UserLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField('Submit')

class CreateUser(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField('Submit')

class CreateLib(FlaskForm):
    lib_fname = StringField('First Name', validators=[DataRequired()])
    lib_lname = StringField('Last Name', validators=[DataRequired()])
    lib_email = StringField('Email', validators=[DataRequired(), Email()])
    lib_password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField()

class LibLogin(FlaskForm):
    id = StringField('ID', validators=[DataRequired()])
    lib_email = StringField('Email', validators=[DataRequired(), Email()])
    lib_password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField('Submit')

class AddBook(FlaskForm):
    isbn = StringField('Book ISBN', validators=[DataRequired()])
    title = StringField('Book Title', validators=[DataRequired()])
    author_fname = StringField('Author First Name', validators=[DataRequired()])
    author_lname = StringField('Author Last Name', validators=[DataRequired()])
    length_ = IntegerField('Book Length', validators=[DataRequired()])
    genre = StringField('Book Genre', validators=[DataRequired()])
    binding = StringField('Type of Book Binding', validators=[DataRequired()])
    quantity = IntegerField('Number of Book', validators=[DataRequired()])
    year_published = IntegerField('Year Published', validators=[DataRequired()])
    submit_button = SubmitField()

class CheckBook(FlaskForm):
    trans_id = StringField('Transaction ID', validators=[DataRequired()])
    checkout_date = DateField('Check Out Date', validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[DataRequired()])
    submit_button = SubmitField()
    