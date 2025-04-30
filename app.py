from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, User, Workout  
from forms import RegisterForm, LoginForm, WorkoutForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_current_user():
    return dict(current_user=current_user)

@app.route('/')
def index():
    return render_template('intro.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken.', 'danger')
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = WorkoutForm()
    if form.validate_on_submit():

        # Get MET value for the activity
        met = Workout.MET_VALUES.get(form.activity.data, 1.0)  # Default to 1.0 if activity not found

        # Calculate calories
        duration = form.duration.data
        calories = Workout.calculate_calories(met, current_user.weight, duration)

        workout = Workout(
            date=form.date.data,
            activity=form.activity.data,
            duration=duration,
            distance=form.distance.data,
            calories=calories,
            user_id=current_user.id
        )
        db.session.add(workout)
        db.session.commit()
        flash('Workout uploaded successfully!', 'success')
        return redirect(url_for('visualize'))
    return render_template('upload.html', form=form)

@app.route('/visualize')
@login_required
def visualize():
    workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.date).all()
    labels = [w.date.strftime('%Y-%m-%d') for w in workouts]
    durations = [w.duration for w in workouts]
    calories = [w.calories for w in workouts]

    start_of_week = datetime.now().date() - timedelta(days=datetime.now().weekday())
    weekly_workouts = [w for w in workouts if w.date >= start_of_week]
    weekly_count = len(weekly_workouts)
    avg_duration = round(sum(w.duration for w in weekly_workouts) / weekly_count, 2) if weekly_count else 0
    avg_calories = round(sum(w.calories for w in weekly_workouts) / weekly_count, 2) if weekly_count else 0

    return render_template('visualize.html',
        labels=labels, durations=durations, calories=calories,
        workouts=workouts, weekly_count=weekly_count,
        avg_duration=avg_duration, avg_calories=avg_calories)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
