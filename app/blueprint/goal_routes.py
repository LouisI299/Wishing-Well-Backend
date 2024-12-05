from flask import Blueprint, request, jsonify

goal_bp = Blueprint('goal_bp', __name__)

@goal_bp.route('/', methods=['GET'])
def get_goals():
    return jsonify({"message": "Goals Message"})