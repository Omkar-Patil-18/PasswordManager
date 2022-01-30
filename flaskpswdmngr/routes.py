from genericpath import exists
from flask import render_template, url_for, flash, redirect, request
from flaskpswdmngr import app, db, bcrypt
from flaskpswdmngr.forms import RegistrationForm, LoginForm
from flaskpswdmngr.models import User,Record
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        title = request.form['title']
        password_record = request.form['password_record']
        user_id = current_user.username
        record = Record(title=title, password_record=password_record,user_id=user_id)
        db.session.add(record)
        db.session.commit()
        # global exists
        # exists = db.session.query(db.exists().where(Record.user_id == current_user)).scalar()
    allrecord = Record.query.all() 
    return render_template('home.html', allTodo=allrecord,myUser = current_user)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

