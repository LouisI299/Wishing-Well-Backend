from flask import Blueprint, request, jsonify

goal_bp = Blueprint('goal', __name__)

@goal_bp.route('/goals', methods=['GET'])
def get_goals():
    return jsonify({"message": "List of goals"})