#Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from flask_jwt_extended import JWTManager


#Define the database
db = SQLAlchemy()

#Function to create the app
def create_app():
    app = Flask(__name__)
    app.config.from_object('instance.config.Config') #Load the config file
    
    
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}) #Allow requests from the frontend
    
    db.init_app(app) #Initialize the database
    jwt = JWTManager(app) #Initialize the web token manager
    
    with app.app_context(): #Create the database tables
        from app import models
        db.create_all()
        db.session.commit()
        #add_test_data()

    # Blueprints
    from app.routes import register_blueprints 
    register_blueprints(app) #Register the blueprints

    return app

#Function to add test users and goals
def add_test_data():
    from app.models import User, SavingsGoal
    user1 = User(first_name='John', last_name='Doe', email = 'john@m', password = 'password', join_date = datetime.now(), points = 0, level = 1)
    # db.session.add(user1)
    user2 = User(first_name='Jane', last_name='Doe', email = 'jane@m', password = 'password', join_date = datetime.now(), points = 0, level = 1)
    user3 = User(first_name='Test', last_name='User', email = 'test@m', password = 'password', join_date = datetime.now(), points = 0, level = 1)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()
    goal1 = SavingsGoal(user_id = 1, name = 'New Car', target_amount = 20000, current_amount = 0, start_date = datetime.now(), end_date = datetime(2025, 12, 31), completed = False, status = 'In Progress')
    goal2 = SavingsGoal(user_id = 2, name = 'New House', target_amount = 50000, current_amount = 0, start_date = datetime.now(), end_date = datetime(2030, 12, 31), completed = False, status = 'In Progress')
    goal3 = SavingsGoal(user_id = 3, name = 'New Phone', target_amount = 1000, current_amount = 0, start_date = datetime.now(), end_date = datetime(2025, 12, 31), completed = False, status = 'In Progress')
    db.session.add(goal1)
    db.session.add(goal2)
    db.session.add(goal3)
    
    db.session.commit()