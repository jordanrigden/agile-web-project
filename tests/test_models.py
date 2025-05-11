import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Workout, Share
from config import Config
from datetime import date

class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB for testing
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(self.app)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_calorie_calculation(self):
        calories = Workout.calculate_calories(met=4.5, weight=70, duration=60)
        expected = 4.5 * 70 * 1.0  # 1 hour
        self.assertEqual(calories, expected)

    def test_create_user_and_workout(self):
        user = User(username='testuser', email='test@example.com', password='hashedpw', weight=70)
        db.session.add(user)
        db.session.commit()

        workout = Workout(
            user_id=user.id,
            date=date.today(),
            description='Running',
            activity='Moderate',
            duration=30,
            calories=Workout.calculate_calories(4.5, user.weight, 30)
        )
        db.session.add(workout)
        db.session.commit()

        self.assertEqual(Workout.query.count(), 1)
        self.assertEqual(workout.user_id, user.id)
        self.assertEqual(user.workouts[0].description, 'Running')

if __name__ == '__main__':
    unittest.main()
