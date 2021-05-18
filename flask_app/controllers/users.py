from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'uuid' in session:
        return redirect('/dashboard')
    else:
        return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'uuid' not in session:
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/create', methods = ['POST'])
def create():
    list_of_users = User.get_by_email(request.form['email']) 
    if len(list_of_users) > 0:
        flash('Email already exists')
        return redirect ('/')
    if not User.validate_inputs(request.form):
        return redirect ('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form["first_name"],
        'last_name': request.form["last_name"],
        'email': request.form["email"],
        'password': pw_hash
    }
    user_id = User.create(data)
    print(user_id)
    session['uuid'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods = ['POST'])
def login():
    list_of_users = User.get_by_email(request.form['email'])
    if len(list_of_users) == 0:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(list_of_users[0]['password'], request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    else:
        session['uuid'] = list_of_users[0]['id']
        return redirect("/dashboard")

@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')
