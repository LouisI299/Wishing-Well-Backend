#Imports
from flask import Blueprint, request, jsonify
from ..models import SavingsGoal

#Make a Blueprint for goals
goal_bp = Blueprint('goal_bp', __name__)

#Routes

#Route for getting all goals
@goal_bp.route('/', methods=['GET'])
def get_goals():
    goals = SavingsGoal.query.all()
    return jsonify([goal.serialize() for goal in goals])