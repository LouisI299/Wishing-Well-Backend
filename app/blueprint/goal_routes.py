#Imports
from flask import Blueprint, request, jsonify
from ..models import SavingsGoal
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

#Make a Blueprint for goals
goal_bp = Blueprint('goal_bp', __name__)

#Routes

#Route for getting all goals
@goal_bp.route('/all', methods=['GET'])
def get_goals():
    goals = SavingsGoal.query.all()
    return jsonify([goal.serialize() for goal in goals])

#Route for getting a goal by ID
@goal_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_goal(id):
    try:
        goal = SavingsGoal.query.get(id)
        if goal:
            return jsonify(goal.serialize())
        else:
            return jsonify({"error": "Goal not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


#Route for getting current user goals
@goal_bp.route('/user', methods=['GET'])
@jwt_required()
def getCurrentUser_goals():
    try : 
        user_id = get_jwt_identity()
        
        savingsGoals = SavingsGoal.query.filter_by(user_id=user_id).all()
        if savingsGoals:
            return jsonify([goal.serialize() for goal in savingsGoals]), 200
        else:
            return jsonify({"error": "You have no goals. Add one!"}), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
#route for creating a goal 
@goal_bp.route('/user', methods=['POST'])
@jwt_required()
def create_goal():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        new_goal = SavingsGoal(
            title=data['title'],
            description=data['description'],
            target_amount=data['target_amount'],
            current_amount=0,
            user_id=user_id
        )
        db.session.add(new_goal)
        db.session.commit()
    except Exception as e: #Catch errors 
        db.session.rollback()
        return jsonify(new_goal.serialize()), 201
    