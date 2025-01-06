from flask import Blueprint, jsonify, request
from ..models import Streak
from flask_jwt_extended import jwt_required, get_jwt_identity

streaks_bp = Blueprint('streaks_bp', __name__)

# current streak
@streaks_bp.route('/', methods=['GET'])
@jwt_required()
def get_streaks():
    user_id = get_jwt_identity()
    streak = Streak.query.filter_by(user_id=user_id, status=True).first()
    return jsonify(streak.serialize()) if streak else jsonify(0), 200

# highest streak
@streaks_bp.route('/highest', methods=['GET'])
@jwt_required()
def get_highest_streak():
    user_id = get_jwt_identity()
    from ..models import Streak
    
    # alle streaks van de gebruiker ophalen
    streaks = Streak.query.filter_by(user_id=user_id).all()
    
    # hoogste streak berekenen
    highest_streak = max((streak.current_streak for streak in streaks), default=0)
    
    return jsonify({"highest_streak": highest_streak}), 200
