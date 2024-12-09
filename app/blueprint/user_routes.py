#Imports
from flask import Blueprint, request, jsonify
from ..models import User
from datetime import datetime
from app import db
from werkzeug.security import check_password_hash

#Blueprint for users
user_bp = Blueprint('user_bp', __name__)

#Routes

#Route for getting all users
@user_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all() #Get all users from the database
    return jsonify([user.serialize() for user in users]) #Return a JSON response for the frontend

#Route for creating a new user
@user_bp.route('/', methods=['POST'])
def create_user():
    try:
        data = request.get_json() #Get the JSON data from the frontend
        new_user = User( #Create a new user instance
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password'],
            join_date=datetime.now(),
            points=0,
            level=1
        )
        db.session.add(new_user) #Add the new user to the database 
        db.session.commit()
        return jsonify(new_user.serialize()), 201 
    except Exception as e: #Catch errors 
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
#Route for logging in a user
@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json() #Get the JSON data from the frontend
        if not data: #Check if the data is empty
            raise ValueError()
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password: #Check if there is no email or password 
            raise ValueError()

        user = User.query.filter_by(email=email).first() #Get the user from the database with the email
        if user and check_password_hash(user.password, password): #Check if the user exists and the password is correct
            return jsonify({"success": True, "message": "Login successful"})
        else: #If the user does not exist or the password is incorrect
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e: #Catch errors
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

    
    