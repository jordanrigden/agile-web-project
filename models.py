from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import date

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    weight = db.Column(db.Float, nullable=False)  # User's weight in kilograms

    workouts = db.relationship('Workout', backref='user', lazy=True)
    shares = db.relationship('Share', backref='owner', lazy=True)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    activity = db.Column(db.String(64))
    duration = db.Column(db.Float)  # minutes
    distance = db.Column(db.Float)  # km
    calories = db.Column(db.Float)  # kcal
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Predefined list of activities and their MET values
    MET_VALUES = {
        'Very Light': 2.0,
        'Light': 3.0,
        'Moderate': 4.5,
        'Vigorous': 6.0,
        'Very Vigorous': 8.0
    }

    @staticmethod
    def calculate_calories(met, weight, duration):
        duration_hours = duration / 60  # Convert minutes to hours
        return met * weight * duration_hours

class Share(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'))
    shared_with = db.Column(db.String(64))  # Username of the recipient
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
