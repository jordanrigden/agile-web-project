from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
from models import Workout
from datetime import datetime

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=4, max=25, message="Username must be between 4 and 25 characters")
    ])
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(message="Please enter a valid email address")
    ])
    weight = FloatField('Weight (kg)', validators=[
        DataRequired(),
        NumberRange(min=0.1, max=500, message="Please enter a valid weight between 0.1 and 500 kg")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message="Password must be at least 6 characters long")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message="Passwords must match")
    ])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username is required")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required")
    ])
    submit = SubmitField('Login')

class WorkoutForm(FlaskForm):
    date = DateField('Date', validators=[
        DataRequired(message="Date is required")
    ])
    description = StringField('Description', validators=[
        DataRequired(),
        Length(max=200, message="Description cannot exceed 200 characters")
    ])
    activity = SelectField(
        'Intensity',
        choices=[(activity, activity) for activity in Workout.MET_VALUES.keys()],
        validators=[DataRequired(message="Please select an activity intensity")]
    )
    duration = FloatField('Duration (min)', validators=[
        DataRequired(),
        NumberRange(min=0.1, max=1440, message="Duration must be between 0.1 and 1440 minutes")
    ])
    submit = SubmitField('Upload')

    def validate_date(self, field):
        if field.data > datetime.now().date():
            raise ValidationError("Date cannot be in the future")

class WeightUpdateForm(FlaskForm):
    weight = FloatField('Weight (kg)', validators=[
        DataRequired(),
        NumberRange(min=0.1, max=500, message="Please enter a valid weight between 0.1 and 500 kg")
    ])
    submit = SubmitField('Update Weight')

class ShareForm(FlaskForm):
    username = StringField('Share With', validators=[
        DataRequired(), 
        Length(min=4, max=25, message="Username must be between 4 and 25 characters")
    ])
    workout_id = SelectField('Workout', coerce=int, validators=[
        DataRequired(message="Please select a workout to share")
    ])
    submit = SubmitField('Share')

    def __init__(self, *args, **kwargs):
        super(ShareForm, self).__init__(*args, **kwargs)
        if not self.workout_id.choices:
            self.workout_id.choices = []