from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class WorkoutForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    activity = StringField('Activity', validators=[DataRequired()])
    duration = FloatField('Duration (min)', validators=[DataRequired()])
    distance = FloatField('Distance (km)', validators=[DataRequired()])
    calories = FloatField('Calories Burned', validators=[DataRequired()])
    submit = SubmitField('Upload')
