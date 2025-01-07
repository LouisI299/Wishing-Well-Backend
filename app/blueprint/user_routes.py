#Imports
from flask import Blueprint, request, jsonify
from ..models import User, UserLoginModel, UserCreateModel
from datetime import datetime, timedelta
from app import db
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from pydantic import ValidationError


#Blueprint for users
user_bp = Blueprint('user_bp', __name__)

#Routes

#Route for getting all users
@user_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all() #Get all users from the database
    return jsonify([user.serialize() for user in users]) #Return a JSON response for the frontend

@user_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify(user.serialize())
    else:
        return jsonify({"error": "User not found"}), 404
    

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
            access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))
            
            return jsonify({
            'access_token': access_token,
            
        }), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
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
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 200
    

# Route for deleting the current user account
@user_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_user():
    try:
        user_id = get_jwt_identity()
        
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({"error": "Invalid user ID"}), 400
        
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        
        return jsonify({"message": "User account deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting user: {e}")
        return jsonify({"error": "An error occurred while deleting the user"}), 500
    
    
@user_bp.route('/search', methods=['GET'])
@jwt_required()
def search_users():
    try:
        user_id = get_jwt_identity()
        query = request.args.get('query', '').lower()  # Get search query from URL
        if not query:
            return jsonify([])  # Return an empty list if no query is provided
        
        # Search for users that match the query in first_name or last_name (case-insensitive)
        users = User.query.filter(
            (User.first_name.ilike(f'%{query}%')) | (User.last_name.ilike(f'%{query}%'))
        ).filter(User.id != user_id).all()
        # Return serialized user data (except the logged-in user)
        result = [user.serialize() for user in users if user.id != user_id]
        return jsonify(result)
    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error 
