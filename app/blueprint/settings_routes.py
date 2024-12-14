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
 
@settings_bp.route('/', methods=['PUT'])
@jwt_required()
def edit_account():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        data = request.get_json()  # Get the JSON data from the request
        action = data.get('action')  # This will determine which operation to perform

        if not action:
            return jsonify({"error": "Action is required"}), 400

        # Handle email update
        if action == 'update_email':
            email = data.get('email')

            if not isinstance(email, str) or not email.strip():
                return jsonify({"error": "Please provide a valid email"}), 400

            if "@" not in email or "." not in email.split("@")[-1]:
                return jsonify({"error": "The email address is not in a valid format"}), 400

            # Check if the email has changed
            if email == user.email:
                return jsonify({"msg": "No changes to the email were detected"}), 200

            # Update the email
            user.email = email
            db.session.commit()

            return jsonify({
                "msg": "Email updated successfully",
                "email": user.email
            }), 200
        
        # Handle password change
        elif action == 'change_password':
            old_password = data.get('old_password')
            new_password = data.get('new_password')

            if not old_password or not new_password:
                return jsonify({"error": "Old and new passwords are required"}), 400

            if new_password == old_password:
                return jsonify({"error": "New password cannot be the same as the old password"}), 400

            # Check if the old password matches
            if check_password_hash(user.password, old_password):
                user.password = generate_password_hash(new_password)
                db.session.commit()
                return jsonify({"msg": "Password changed successfully"}), 200
            else:
                return jsonify({"error": "Invalid old password"}), 401
        
        else:
            return jsonify({"error": "Invalid action specified"}), 400

    except Exception as e:
        db.session.rollback()
        # Log the exception (replace with logging in production)
        print(f"Error updating account: {e}")
        return jsonify({"msg": "An error occurred while updating account"}), 500

    # Er staat nog niks van notificaties in de db, dus dit kan nog niet getest worden
    #@settings_bp.route('/change_notification_settings', methods=['PUT'])
        #@jwt_required()
        #def change_notification_settings():
            #try:
               # user_id = get_jwt_identity()
                #user = User.query.get(user_id)

               # if not user:
                #    return jsonify({"error": "User not found"}), 404

                #data = request.get_json()
                #email_notifications = data.get('email_notifications')
                #push_notifications = data.get('push_notifications')
                #sms_notifications = data.get('sms_notifications')

               # if email_notifications is not None:
                   # user.email_notifications = email_notifications
                #if push_notifications is not None:
                    #user.push_notifications = push_notifications
               # if sms_notifications is not None:
                    #user.sms_notifications = sms_notifications

                #db.session.commit()
                #return jsonify({"msg": "Notification settings updated successfully"}), 200   

           # except Exception as e:
               # db.session.rollback()
                # Log the exception (replace with logging in production)
                #print(f"Error changing notification settings: {e}")
                #return jsonify({"msg": "An error occurred while changing notification settings"}), 500
            
    


    

    
    
        
        
    