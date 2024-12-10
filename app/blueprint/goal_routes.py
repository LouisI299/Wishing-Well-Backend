#Imports
from flask import Blueprint, request, jsonify
from ..models import SavingsGoal
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

#Make a Blueprint for goals
goal_bp = Blueprint('goal_bp', __name__)

#Routes

#Route for getting all goals
@goal_bp.route('/all', methods=['GET'])
def get_goals():
    goals = SavingsGoal.query.all()
    return jsonify([goal.serialize() for goal in goals])

#Route for getting current user goals
@goal_bp.route('/user', methods=['GET'])
@jwt_required()
def getCurrentUser_goals():
    try : 
        user_id = get_jwt_identity()
        
        savingsGoal = SavingsGoal.query.filter_by(user_id=user_id).all()
        if savingsGoal:
            return jsonify([savingsGoal.serialize() for goal in savingsGoal]), 200
        else:
            return jsonify({"error": "You have no goals. Add one!"}), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500