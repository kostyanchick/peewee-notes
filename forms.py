from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, EqualTo, Length, Email

formValidators = {
    'username': [Length(min=4, max=20, message='Username should have 4-20 characters')],
    'email': [Length(min=6, max=35, message='Email should have 6-35 characters'),
              Email(message='Please enter a valid email address like example@email.com')],
    'password': [Length(min=4, max=20, message='Password should be 4-20 characters')],
    'confirm_password': [Length(min=4, max=20, message='Password should be 4-20 characters'),
                        EqualTo('password', message='Passwords must match')]
}


class LoginForm(Form):

    username = StringField('Username', render_kw={"placeholder": 'username'})
    password = PasswordField('Password', render_kw={"placeholder": 'password'})
    remember_me = BooleanField('Remember me')
    # submit = SubmitField('Log In')

class JoinForm(Form):
    username = StringField('Username', validators=formValidators['username'], render_kw={"placeholder": 'username'})
    email = StringField('Email',
                         validators=formValidators['email'],
                         render_kw={"placeholder": 'example@email.com'})
    password = PasswordField('Password',
                             validators=formValidators['confirm_password'],
                             render_kw = {"placeholder": 'password'})
    confirm_password = PasswordField('Confirm your password',
                                     validators= formValidators['confirm_password'],
                                     render_kw={"placeholder": 'password'})
    remember_me = BooleanField('Remember me')
    # submit = SubmitField('Submit')

class EditProfileForm(Form):
    username = StringField('Username', validators=formValidators['username'])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])

class PhotoForm(Form):
    photo = FileField('New photo', validators=[FileRequired(message='No selected file')])

class AddNoteForm(Form):
    note = TextAreaField('Add something you want to note',
                         validators=[DataRequired(message='Add some content'),
                                     Length(min=1, max=255)],
                         id='content')

class EditNoteForm(Form):
    pass

