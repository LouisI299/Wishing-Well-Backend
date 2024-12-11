#Imports
from flask import Blueprint, request, jsonify
from ..models import SavingsGoal
from ..models import User
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from werkzeug.security import check_password_hash

#Blueprint for settings
settings_bp = Blueprint('settings_bp', __name__)

#Route to edit the user's profile
@settings_bp.route('/EditProfile', methods=['GET', 'POST'])
@jwt_required()
def edit_profile():
    user_id = get_jwt_identity()
    user = user.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method == 'GET':
        # Return the current user's profile
        try:
            return jsonify(user.serialize()), 200
        except Exception as e:
            print(f"Error serializing user: {e}")
            return jsonify({"error": "Error fetching profile"}), 500

    elif request.method == 'POST':
    # Update the user's profile
        try:
            data = request.get_json()  # Get the JSON data from the request
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')

            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if email:
                user.email = email

            db.session.commit()
            return jsonify({
                "msg": "Profile updated successfully",
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email
            }), 200
        except Exception as e:
            db.session.rollback()
            print(f"Error updating profile: {e}")
            return jsonify({"msg": "Error updating profile", "error": str(e)}), 500
        
#Route to change the user's password // 
@settings_bp.route('/ChangePassword', methods=['POST'])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        data = request.get_json()  # Get the JSON data from the request
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not old_password or not new_password:
            return jsonify({"error": "Old and new passwords are required"}), 400

        if new_password == old_password:
            return jsonify({"error": "New password cannot be the same as the old password"}), 400

        #Add additional password strength validation here

        if check_password_hash(user.password, old_password):
            user.password = generate_password_hash(new_password)
            db.session.commit()
            return jsonify({"msg": "Password changed successfully"}), 200
        else:
            return jsonify({"error": "Invalid old password"}), 401

    except Exception as e:
        db.session.rollback()
        # Log the exception (replace with logging in production)
        print(f"Error changing password: {e}")
        return jsonify({"msg": "An error occurred while changing password"}), 500
    

    


    

    
    
        
        
    