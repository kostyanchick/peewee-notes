from flask import render_template, redirect,url_for, jsonify, abort, flash
from flask import session, request
from functools import wraps
from datetime import datetime
from peewee import *
from hashlib import md5
from werkzeug.utils import secure_filename
import os

from app import pg_db, app
from models import User, Note
from forms import LoginForm, JoinForm, AddNoteForm, EditProfileForm, EditNoteForm, PhotoForm

def auth_user(user):
    # Flask gives us session object that store data like browser cookies
    # and that data can be accessible from one request to another
    session['logged_in'] = True
    session['user_id'] = user.id
    session['username'] = user.username
    flash('You are logged in as %s' % user.username)

def get_current_user():
    if session['logged_in']:
        return User.get(User.id == session['user_id'])

def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return inner

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = AddNoteForm()
    user = get_current_user()
    if form.validate_on_submit():
        if form.note.data:
            # Create a new note in db
            note = Note.create(user=user.id, content=form.note.data, timestamp=datetime.now())

            # Render a single panel with new note and return the HTML
            rendered = render_template('note.html', note=note)
            return jsonify({'note': rendered, 'success': True})
        # If there no content in form, indicate a failure
        return jsonify({'success': False})
    notes = Note.user_notes(user)
    return render_template('index.html',
                           user=user,
                           title='%s notes' % user.username,
                           notes=notes,
                           form=form)

@app.route('/archive/<int:pk>/', methods=['POST'])
@login_required
def archive_note(pk):
    user = get_current_user()
    try:
        note = Note.get(Note.id == pk, Note.user==user)
    except Note.DoesNotExist:
        abort(404)
    note.archived = True
    note.save()
    return jsonify({'success': True})

@app.route('/join', methods=['GET', 'POST'])
def join():
    if session.get('logged_in'):
        return redirect(url_for('index'))
    form = JoinForm()
    if form.validate_on_submit():
        try:
            with pg_db.atomic():
                user = User.create(
                    username=form.username.data,
                    password=md5((form.password.data).encode('utf-8')).hexdigest(),
                    email=form.email.data,
                    about_me='',
                    join_date=datetime.now())

            auth_user(user)
            return redirect(url_for('index'))

        except IntegrityError:
            flash('That username or email is already in use')

    return render_template('join.html', form=form, title='Join Us')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            pw_hash = md5(form.password.data.encode('utf-8')).hexdigest()
            user = User.get(
                (User.username == form.username.data) &
                (User.password == pw_hash))
        except User.DoesNotExist:
            flash('Entered password is incorrect')
        else:
            auth_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', form=form, title='Log In')
@app.route('/add_note', methods=['POST'])
@login_required
def add_note():
    pass

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.get(User.username == username)
    # return jsonify(user)
    return render_template('profile.html', user=user, title='Profile')

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = get_current_user()
    form = EditProfileForm()
    if form.validate_on_submit():
        try:
            with pg_db.atomic():
                edit_q = User.update(
                    username=form.username.data,
                    about_me=form.about_me.data
                ).where(
                    User.username == user.username
                )
                edit_q.execute()

            # We should update our session object with a new username
            session['username'] = form.username.data
            user = get_current_user()
            flash('Your data has been changed')
            return redirect(url_for('profile', username=user.username))

        except IntegrityError:
            flash('That username or email is already used by someone else')
    else:
        form.username.data = user.username
        form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, title='Edit your profile')

# this function get an extension of inputed file
# and check if it existing in the list of allowed extensions
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# this function create new name for file by using username
# with the same extension
def rename_file(filename):

    return md5(filename.lower().encode('utf-8')).hexdigest() + '.' + filename.rsplit('.', 1)[1]

@app.route('/upload_image', methods=['GET','POST'])
@login_required
def upload_image():
    user = get_current_user()
    form = PhotoForm()
    if form.validate_on_submit():
        file = form.photo.data
        if file and allowed_file(file.filename):
            filename = secure_filename(rename_file(file.filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            try:
                old_file = 'static/img/' + user.photo_file_name
                os.remove(old_file)
            except OSError:
                pass
            with pg_db.atomic():
                img_q = User.update(photo_file_name=filename).where(User.username == user.username)
                img_q.execute()

            flash('Your profile photo has been changed')
            return redirect(url_for('profile', username=user.username))
    return render_template('upload_image.html', form=form, title='Change your avatar')

@app.route('/edit_note/<note_id>', methods=['GET','POST'])
@login_required
def edit_note(note_id):
    pass
