from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Initialize LoginManager
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
 
    # Add the is_active method
    def is_active(self):
        return True

    # Add the get_id method
    def get_id(self):
        return str(self.id)
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def calculate_bmi(weight, height):
    # Calculate BMI (Body Mass Index)
    bmi = weight / (height * height)
    return round(bmi, 2)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        bmi = calculate_bmi(weight, height)
        return render_template('result.html', bmi=bmi)
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html')

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin, login_required, current_user

# ... other code ...

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('login_success'))
    return render_template('login.html')

@app.route('/login_success')
@login_required
def login_success():
    return render_template('login_success.html')




def create_database():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_database()
    app.run(debug=True)
