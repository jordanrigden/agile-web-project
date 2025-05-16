# 🏋️‍♂️ FitTrack

## 👥 Group Members

| UWA ID    | Name            | GitHub Username     |
|-----------|------------------|----------------------|
| 22496593  | Jordan Rigden    | jordanrigden         |
| 24535749  | Mehnaz Monsur    | Mehnaz-M             |
| 23913189  | Han Sun          | HanSun23913189       |
| 23912137  | Ahmed Shadab     | Shadab0708           |


**FitTrack** is a fitness tracking and sharing platform that allows users to upload their workout records, view analytical charts, and share selected data with friends.

---

## ✨ Features

- 🧍 User authentication: Register, log in, and log out
- 📤 Upload workout data (activity, duration, calories)
- 📊 Visualize workout trends using Chart.js
- 🤝 Share selected workouts with other users
- 💡 Simple and intuitive UI built with Bootstrap

---

---

## 🚀 How to Run (Development Mode)

```bash
# 1. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 2. Install project dependencies
pip install -r requirements.txt


# 3. Start the Flask app
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

---

## 🧪 Running Tests

Before running tests, make sure all dependencies are installed:

```bash
pip install -r requirements.txt

#To run all core unit tests (e.g., forms, models, basic app logic):
python -m unittest discover -s tests -p "test_*.py"

#o run all Selenium-based UI tests located in the tests/selenium/ folder:
python -m unittest discover -s tests/selenium -p "test_*.py"




