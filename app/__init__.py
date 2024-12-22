#Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from flask_jwt_extended import JWTManager
import os
from app.tasks.scheduler import start_scheduler
import atexit


#Define the database
db = SQLAlchemy()

#Function to create the app
def create_app():
    app = Flask(__name__, static_folder="../../frontend/public", static_url_path="/static")
    app.config.from_object('instance.config.Config') #Load the config file
    
    print(f"Static folder path: {os.path.abspath(app.static_folder)}")
    
    
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}) #Allow requests from the frontend
    
    db.init_app(app) #Initialize the database
    jwt = JWTManager(app) #Initialize the web token manager
    
    with app.app_context(): #Create the database tables
        from app import models
        db.create_all()
        db.session.commit()
        #add_test_data()
        
    with app.app_context(): #Start the scheduler
        scheduler = start_scheduler(app)
        

    # Blueprints
    from app.routes import register_blueprints 
    register_blueprints(app) #Register the blueprints
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()
    
    atexit.register(lambda: scheduler.shutdown())

    return app


# Test data
USERS = [
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@m.m",
        "password": "password"
    },
    {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@m.m",
        "password": "password"
    },
    {
        "first_name": "James",
        "last_name": "Bond",
        "email": "james@m.m",
        "password": "password"
    },
    {
        "first_name": "Alex",
        "last_name": "Pereira",
        "email": "alex@m.m",
        "password": "password"
    }
]

USER_DEFAULTS = {
    "join_date": datetime.now(),
    "points": 0,
    "level": 1
}

GOALS = [
    {
        "user_id": 1,
        "name": "New Car",
        "target_amount": 20000,
        "current_amount": 0,
        "end_date": datetime(2025, 12, 31),
        "category": "car",
        "period_amount": 200,
    },
    {
        "user_id": 2,
        "name": "New House",
        "target_amount": 50000,
        "current_amount": 0,
        "end_date": datetime(2030, 12, 31),
        "category": "house",
        "period_amount": 500,
    },
    {
        "user_id": 3,
        "name": "New Phone",
        "target_amount": 1000,
        "current_amount": 100,
        "end_date": datetime(2025, 12, 31),
        "category": "electronics",
        "period_amount": 100,
    }
]

GOAL_DEFAULTS = {
    "start_date": datetime.now(),
    "status": True
}

#Function to add test users and goals
def add_test_data():
    from app.models import User, SavingsGoal
    for user in USERS:
        db.session.add(User(**user, **USER_DEFAULTS))
    db.session.commit()
    
    for goal in GOALS:
        db.session.add(SavingsGoal(**goal, **GOAL_DEFAULTS))
    db.session.commit()