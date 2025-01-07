# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
import os
import atexit
from datetime import datetime

# Initialize extensions
db = SQLAlchemy()
mail = Mail()


# Application Factory Pattern
def create_app():
    app = Flask(__name__, static_folder="../../frontend/public", static_url_path="/static")
    app.config.from_object('instance.config.Config') 

    # Database initialization
    db.init_app(app)

    # Logging static folder path for debugging
    print(f"Static folder path: {os.path.abspath(app.static_folder)}")

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    # Initialize JWT and Mail
    db.init_app(app)
    jwt = JWTManager(app)
    mail.init_app(app)

    # Mailtrap Config
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    with app.app_context():
        # Import models here to avoid circular imports
        from app import models
        db.create_all()
        db.session.commit()

        # Start the scheduler
        from app.tasks.scheduler import start_scheduler
        scheduler = start_scheduler(app)
        atexit.register(lambda: scheduler.shutdown())

    # Register Blueprints
    from app.routes import register_blueprints
    register_blueprints(app)

    # Cleanup database session
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app


# Test Data
USERS = [
    {"first_name": "John", "last_name": "Doe", "email": "john@m.m", "password": "password"},
    {"first_name": "Jane", "last_name": "Doe", "email": "jane@m.m", "password": "password"},
    {"first_name": "James", "last_name": "Bond", "email": "james@m.m", "password": "password"},
    {"first_name": "Alex", "last_name": "Pereira", "email": "alex@m.m", "password": "password"},
]

USER_DEFAULTS = {"join_date": datetime.now(), "points": 0, "level": 1}

GOALS = [
    {"user_id": 1, "name": "New Car", "target_amount": 20000, "current_amount": 0,
     "end_date": datetime(2025, 12, 31), "category": "car", "period_amount": 200},
    {"user_id": 2, "name": "New House", "target_amount": 50000, "current_amount": 0,
     "end_date": datetime(2030, 12, 31), "category": "house", "period_amount": 500},
    {"user_id": 3, "name": "New Phone", "target_amount": 1000, "current_amount": 100,
     "end_date": datetime(2025, 12, 31), "category": "electronics", "period_amount": 100},
]

GOAL_DEFAULTS = {"start_date": datetime.now(), "status": True}

BADGES = [
    {"name": "Streak 1", "description": "Behaald na 1 dag streak", "image_url": "streak1.png"},
    {"name": "Streak 3", "description": "Behaald na 3 dagen streak", "image_url": "streak3.png"},
    {"name": "Streak 5", "description": "Behaald na 5 dagen streak", "image_url": "streak5.png"},
    {"name": "Level 5", "description": "Behaald bij level 5", "image_url": "level5.png"},
    {"name": "Level 10", "description": "Behaald bij level 10", "image_url": "level10.png"},
    {"name": "Totaal €1000", "description": "Behaald bij €1000 gespaard", "image_url": "total1000.png"},
    {"name": "Totaal €2000", "description": "Behaald bij €2000 gespaard", "image_url": "total2000.png"},
]


# Voeg testdata toe
def add_test_data():
    from app.models import User, SavingsGoal, Badge

    for user in USERS:
        if not User.query.filter_by(email=user["email"]).first():
            db.session.add(User(**user, **USER_DEFAULTS))

    for goal in GOALS:
        db.session.add(SavingsGoal(**goal, **GOAL_DEFAULTS))

    for badge in BADGES:
        if not Badge.query.filter_by(name=badge["name"]).first():
            db.session.add(Badge(**badge))

    db.session.commit()
    print("Testdata succesvol toegevoegd!")
