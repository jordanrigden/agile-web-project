from flask import Flask, render_template
from config import Config
from models import db, User
from flask_login import LoginManager, current_user

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_current_user():
    return dict(current_user=current_user)


@app.route('/')
def index():
    return render_template('intro.html')

# login placeholder
@app.route('/login')
def login():
    return "<h3>Login page coming soon.</h3>"

# register placeholder
@app.route('/register')
def register():
    return "<h3>Register page coming soon.</h3>"

# ✅ activate app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
