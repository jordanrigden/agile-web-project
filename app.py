from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from config import Config
from models import db, User, Workout, Share
from forms import RegisterForm, LoginForm, WorkoutForm, WeightUpdateForm, ShareForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_migrate import Migrate
from sqlalchemy import desc, and_
from collections import defaultdict
from static.py.activities import activities

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
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_pw,
            weight=form.weight.data 
        )
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

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = WeightUpdateForm()
    workouts = Workout.query.filter_by(user_id=current_user.id).order_by(desc(Workout.date)).limit(8).all()
    return render_template('profile.html', workouts=workouts, form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    flash('Ensure correct weight in profile before upload.', 'info')
    form = WorkoutForm()
    if form.validate_on_submit():

        met = Workout.MET_VALUES.get(form.activity.data, 1.0)
        duration = form.duration.data
        calories = Workout.calculate_calories(met, current_user.weight, duration)

        workout = Workout(
            date=form.date.data,
            description=form.description.data,
            activity=form.activity.data,
            duration=duration,
            calories=calories,
            user_id=current_user.id
        )
        db.session.add(workout)
        db.session.commit()
        flash('Workout uploaded successfully!', 'success')
        return redirect(url_for('visualize'))
    return render_template('upload.html', form=form, activities=activities)

@app.route('/visualize')
@login_required
def visualize():
    range_type = request.args.get('range', 'week')
    today = datetime.today()

    if range_type == 'month':
        start_date = today - timedelta(days=30)
    elif range_type == 'year':
        start_date = today - timedelta(days=365)
    else:
        start_date = today - timedelta(days=6)

    workouts = Workout.query.filter(
        Workout.user_id == current_user.id,
        Workout.date >= start_date
    ).order_by(Workout.date).all()

    if range_type == 'year':
        monthly_labels = []
        current_month = today.replace(day=1)
        for _ in range(12):
            monthly_labels.append(current_month.strftime('%Y-%m'))
            current_month -= timedelta(days=1)
            current_month = current_month.replace(day=1)

        monthly_data = {month: {'duration': 0, 'calories': 0} for month in monthly_labels}
        for workout in workouts:
            month = workout.date.strftime('%Y-%m')
            if month in monthly_data:
                monthly_data[month]['duration'] += workout.duration
                monthly_data[month]['calories'] += workout.calories

        labels = monthly_labels[::-1]
        durations = [monthly_data[month]['duration'] for month in labels]
        calories = [monthly_data[month]['calories'] for month in labels]

        total_duration = sum(durations)
        total_calories = sum(calories)
        non_zero_months = len([m for m in durations if m > 0])
        avg_duration = round(total_duration / non_zero_months, 2) if non_zero_months > 0 else 0
        avg_calories = round(total_calories / non_zero_months, 2) if non_zero_months > 0 else 0
    else:
        grouped_data = defaultdict(lambda: {'duration': 0, 'calories': 0})
        for workout in workouts:
            date_str = workout.date.strftime('%Y-%m-%d')
            grouped_data[date_str]['duration'] += workout.duration
            grouped_data[date_str]['calories'] += workout.calories

        date_list = []
        current_date = start_date
        while current_date <= today:
            date_list.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)

        labels = date_list
        durations = [grouped_data[date]['duration'] for date in date_list]
        calories = [grouped_data[date]['calories'] for date in date_list]

        total_duration = sum(durations)
        total_calories = sum(calories)
        non_zero_days = len([d for d in durations if d > 0])
        avg_duration = round(total_duration / non_zero_days, 2) if non_zero_days > 0 else 0
        avg_calories = round(total_calories / non_zero_days, 2) if non_zero_days > 0 else 0

    return render_template('visualize.html',
        labels=labels,
        durations=durations,
        calories=calories,
        workouts=workouts,
        weekly_count=len(workouts),
        avg_duration=avg_duration,
        avg_calories=avg_calories,
        selected_range=range_type
    )

@app.route('/update_weight', methods=['POST'])
@login_required
def update_weight():
    form = WeightUpdateForm()
    if form.validate_on_submit():
        current_user.weight = form.weight.data
        db.session.commit()
        flash('Weight updated successfully!', 'success')
    else:
        flash('Failed to update weight. Please try again.', 'danger')
    return redirect(url_for('profile', form=form))

@app.route('/share', methods=['GET', 'POST'])
@login_required
def share():
    form = ShareForm()
    workouts = Workout.query.filter_by(user_id=current_user.id).order_by(desc(Workout.date)).limit(30).all()
    form.workout_id.choices = [(w.id, f"{w.date.strftime('%Y-%m-%d')} - {w.description}") for w in workouts]

    if form.validate_on_submit():
        username = request.form['username']
        workout_id = request.form['workout_id']
        user_to_share = User.query.filter_by(username=username).first()

        if not user_to_share:
            flash('User not found!', 'danger')
            return redirect(url_for('share'))

        existing_share = Share.query.filter(
            and_(
                Share.workout_id == workout_id,
                Share.shared_with_user_id == user_to_share.id,
                Share.owner_id == current_user.id
            )
        ).first()

        if existing_share:
            flash('This workout has already been shared with this user!', 'warning')
            return redirect(url_for('share'))

        shared_workout = Share(
            workout_id=workout_id,
            shared_with_user_id=user_to_share.id,
            owner_id=current_user.id
        )
        db.session.add(shared_workout)
        db.session.commit()
        flash(f'Workout shared to {username}!', 'success')
    return render_template('share.html', workouts=workouts, form=form)

@app.route('/shared_with_me', methods=['GET', 'POST'])
@login_required
def shared_with_me():
    share_records = Share.query.filter_by(shared_with_user_id=current_user.id).all()
    workouts_with_usernames = []

    for share in share_records:
        workout = Workout.query.get(share.workout_id)
        if workout:
            sharing_user = User.query.get(share.owner_id)
            if sharing_user:
                workouts_with_usernames.append({
                    'workout': workout,
                    'sharing_username': sharing_user.username
                })

    return render_template('shared_with_me.html', workouts=workouts_with_usernames)

@app.route('/search_users')
@login_required
def search_users():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    users = User.query.filter(User.username.ilike(f"%{query}%")).limit(10).all()
    usernames = [user.username for user in users if user.id != current_user.id]
    return jsonify(usernames)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
