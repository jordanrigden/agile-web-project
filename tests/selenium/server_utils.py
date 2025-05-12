from threading import Thread
from werkzeug.serving import make_server
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

class ServerThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.server = make_server("127.0.0.1", 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

        # ✅ Step 1: Create tables
        db.create_all()

        # ✅ Step 2: Add default test user with numbered name like selenium01
        default_username = "selenium01"
        default_email = f"{default_username}@example.com"

        if not User.query.filter_by(username=default_username).first():
            user = User(
                username=default_username,
                email=default_email,
                weight=70,
                password=generate_password_hash("Selenium123")
            )
            db.session.add(user)
            db.session.commit()

    def run(self):
        print("🚀 Starting Flask live server for tests...")
        self.server.serve_forever()

    def shutdown(self):
        print("🛑 Shutting down Flask test server...")
        self.server.shutdown()
