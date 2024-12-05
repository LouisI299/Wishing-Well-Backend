from flask import Blueprint, request, jsonify
from ..models import SavingsGoal

goal_bp = Blueprint('goal_bp', __name__)

@goal_bp.route('/', methods=['GET'])
def get_goals():
    goals = SavingsGoal.query.all()
    return jsonify([goal.serialize() for goal in goals])