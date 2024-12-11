#Imports
from flask import Blueprint, request, jsonify
from ..models import User, UserLoginModel, UserCreateModel
from datetime import datetime
from app import db
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

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
        user_data = UserCreateModel(**data) 
        new_user = User( #Create a new user instance
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password=user_data.password,
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
        data = request.get_json()
        if not data:
            raise ValueError("No data provided")
        
        user_data = UserLoginModel(**data)
        
        user = User.query.filter_by(email=user_data.email).first()
        if user and check_password_hash(user.password, user_data.password):
            access_token = create_access_token(identity=str(user.id))
            return jsonify({"success": True, "message": "Login successful", "access_token": access_token})
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    
#Route for getting the current user
@user_bp.route('/current', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        
        user_id = get_jwt_identity()
        
        user = User.query.get(user_id)
        if user:
            return jsonify(user.serialize())
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 200
    
    