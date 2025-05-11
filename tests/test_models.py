import unittest
from app import app, db
from models import User, Workout, Share
from datetime import date

class TestModels(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        user = User(username='alice', email='alice@example.com', password='secret', weight=55.0)
        db.session.add(user)
        db.session.commit()
        self.assertIsNotNone(User.query.filter_by(username='alice').first())

    def test_create_workout_and_calories(self):
        user = User(username='bob', email='bob@example.com', password='pass', weight=70.0)
        db.session.add(user)
        db.session.commit()

        met = Workout.MET_VALUES['Moderate']
        duration = 60  # minutes
        expected_calories = Workout.calculate_calories(met, user.weight, duration)

        workout = Workout(
            description='Evening Ride',
            activity='Moderate',
            duration=duration,
            calories=expected_calories,
            user_id=user.id
        )
        db.session.add(workout)
        db.session.commit()

        fetched = Workout.query.first()
        self.assertEqual(fetched.calories, expected_calories)
        self.assertEqual(fetched.user.username, 'bob')

    def test_create_share(self):
        owner = User(username='charlie', email='charlie@example.com', password='123', weight=80.0)
        recipient = User(username='dave', email='dave@example.com', password='456', weight=75.0)
        db.session.add_all([owner, recipient])
        db.session.commit()

        workout = Workout(description='Morning Run', user_id=owner.id, duration=30, calories=200)
        db.session.add(workout)
        db.session.commit()

        share = Share(workout_id=workout.id, owner_id=owner.id, shared_with_user_id=recipient.id)
        db.session.add(share)
        db.session.commit()

        self.assertEqual(share.owner.username, 'charlie')
        self.assertEqual(share.shared_with_user.username, 'dave')

if __name__ == '__main__':
    unittest.main()
