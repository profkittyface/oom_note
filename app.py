from flask import Flask, render_template, redirect, flash, url_for, jsonify, request, g
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from config import Config
from forms import LoginForm, SignupForm, CreateForm, UpdateForm
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from model import Session, User, Note
from util import check_user_creds, hash_password
from response import ResponseGenerator

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(username):
    s = Session()
    user = s.query(User).filter_by(username=username).first()
    return user


@app.route("/")
def index():
    print(g)
    return render_template('index.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = hash_password(form.password.data)
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        s = Session()
        user = User(username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name)

        user_exist = s.query(User).filter_by(username=username)
        if user_exist != None:
            flash('User already exists')
            return render_template('signup.html', title='Sign Up', form=form)
        s.add(user)
        s.commit()
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = check_user_creds(
            username=form.username.data, password=hash_password(form.password.data))
        if user == False:
            flash('User or password incorrect')
            return redirect(url_for('login'))
        if user != False:
            login_user(user)
            return redirect(url_for('logged_in'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logged_in')
@login_required
def logged_in():
    username = current_user.username
    return render_template('logged_in.html', username=username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/list')
@login_required
def list_notes():
    note_set = []
    userid = current_user.id
    s = Session()
    nq = s.query(Note).filter_by(userid=userid)
    for note in nq:
        n = note.__dict__
        n.pop('_sa_instance_state')
        note_set.append(n)
    return jsonify(note_set)


@app.route('/delete/<noteid>')
def delete_note(noteid):
    s = Session()
    note = s.query(Note).filter_by(id=noteid).one()
    # Was note created by user?
    if note.userid == current_user.id:
        s.delete(note)
        s.commit()
    else:
        return ResponseGenerator().getResponse('No permission to delete (Note not created by logged in user)')
    return ResponseGenerator().getResponse('Suceeded')


@app.route('/create', methods=['GET', 'POST'])
def create_note():
    form = CreateForm()
    if request.method == 'POST':
        s = Session()
        if form.validate_on_submit():
            note = Note(title=form.title.data,
                        content=form.content.data, userid=current_user.id)
            s.add(note)
            s.commit()
            return jsonify('Created note')
    elif request.method == 'GET':
        return render_template('create.html', form=form)


@app.route('/update/<noteid>')
def update_note(noteid):
    form = UpdateForm()
    s = Session()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        note = s.query(Note).filter_by(id=noteid).one()
        note.title = title
        note.content = content
        s.commit()
        return jsonify('Succeeded')
    return jsonify('Update error')


if __name__ == '__main__':
    app.run(debug=True)
