from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'nerf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(hours=2)

# initialize the db
db = SQLAlchemy(app)

# --------- Models ---------- #
class Users(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    # Add board member boolean value

    def __init__(self, name, email):
        self.name = name
        self.email = email

# ---------- Routes ---------- #
@app.route('/')
def index():
    return render_template('index.html', names = ['filbert', 'tahoe', 'oreo', 'ganymeade'])

# Login, verify that the session has a user and that the user is set to the timedelta limit
@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form['nm']
        session['user'] = user

        existing_user = Users.query.filter_by(name=user).first()
        if existing_user:
            session['email'] = existing_user.email
        else:
            usr = Users(user, '')
            db.session.add(usr)
            db.session.commit()

        flash(f'You have successfully logged in. Welcome, {user}!')
        return redirect(url_for('user'))
    else:
        if 'user' in session:
            flash('You are already logged in')
            return redirect(url_for('user'))
        return render_template('login.html')

@app.route('/user/', methods=['POST', 'GET'])
def user():
    email = None
    if 'user' in session:
        # user = session['user']
        if request.method == 'POST':
            email = request.form['email']
            session['email'] = email
            existing_user = Users.query.filter_by(name=user).first()
            existing_user.email = email
            db.session.commit()
            flash('Email good, bruh')
        else:
            if 'email' in session:
                email = session['email']

        return render_template('user.html', email=email)
    else: 
        flash('You must log in')
        return redirect(url_for('login'))

@app.route('/userview/')
def user_view():
    return render_template('userview.html', values=users.query.all())

@app.route('/logout')
def logout():
    if 'user' in session:
        user = session['user']
    session.pop('user', None)
    session.pop('email', None)
    flash(f'You have successfully logged out, {user}', 'info')
    return redirect(url_for('login'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)