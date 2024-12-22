from flask import Blueprint, jsonify, request
from ..models import Streak
from flask_jwt_extended import jwt_required, get_jwt_identity





streaks_bp = Blueprint('streaks_bp', __name__)

@streaks_bp.route('/', methods=['GET'])
@jwt_required()
def get_streaks():
    user_id = get_jwt_identity()
    streak = Streak.query.filter_by(user_id=user_id, status = True).first()
    return jsonify(streak.serialize()) if streak else jsonify(0), 200