# 🏋️‍♂️ FitTrack

**FitTrack** is a fitness tracking and sharing platform that allows users to upload their workout records, view analytical charts, and share selected data with friends.

---

## ✨ Features

- 🧍 User authentication: Register, log in, and log out
- 📤 Upload workout data (activity, duration, distance, calories)
- 📊 Visualize workout trends using Chart.js
- 🤝 Share selected workouts with other users
- 💡 Simple and intuitive UI built with Bootstrap

---

## 📁 Project Structure





---

## 🚀 How to Run (Development Mode)

```bash
# 1. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 2. Install project dependencies
pip install -r requirements.txt

# 3. Initialize the database (only on first run)
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
...     exit()

# 4. Start the Flask app
python app.py
```

---

## How to Upgrade the Database
```bash
# You can bring your database up to date by running
flask db upgrade

# To automatically create a database migration script
flask db migrate -m "Description of your migration"

```