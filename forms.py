from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import Workout
from datetime import datetime

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    weight = FloatField('Weight (kg)', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class WorkoutForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired(), Length(max=200)])
    activity = SelectField(
        'Type of Activity',
        choices=[(activity, activity) for activity in Workout.MET_VALUES.keys()],
        validators=[DataRequired()]
    )
    duration = FloatField('Duration (min)', validators=[DataRequired()])
    submit = SubmitField('Upload')

class WeightUpdateForm(FlaskForm):
    weight = FloatField('Weight (kg)', validators=[DataRequired()])
    submit = SubmitField('Update Weight')

class ShareForm(FlaskForm):
    username = StringField('Share With', validators=[DataRequired(), Length(min=4, max=25)])
    workout_id = SelectField('Workout', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Share')
