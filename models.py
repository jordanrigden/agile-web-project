from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import date

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    weight = db.Column(db.Float, nullable=False)

    workouts = db.relationship('Workout', backref='user', lazy=True)

    # Relationships 
    sent_shares = db.relationship(
        'Share',
        foreign_keys='[Share.owner_id]',
        back_populates='owner',
        lazy=True
    )

    received_shares = db.relationship(
        'Share',
        foreign_keys='[Share.shared_with_user_id]',
        back_populates='shared_with_user',
        lazy=True
    )

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    description = db.Column(db.String(200), nullable=False)
    activity = db.Column(db.String(64))
    duration = db.Column(db.Float)  # minutes
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
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    shared_with_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    shared_with_user = db.relationship(
        'User',
        foreign_keys=[shared_with_user_id],
        back_populates='received_shares'
    )
    owner = db.relationship(
        'User',
        foreign_keys=[owner_id],
        back_populates='sent_shares'
    )
