#Imports
from flask import Blueprint, request, jsonify
from ..models import SavingsGoal
from flask_jwt_extended import jwt_required

#Make a Blueprint for goals
goal_bp = Blueprint('goal_bp', __name__)

#Routes

#Route for getting all goals
@goal_bp.route('/', methods=['GET'])
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
    
