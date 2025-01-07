#Imports
from flask import Blueprint, request, jsonify
from ..models import Friendship, User, Like, SavingsGoal
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta

#Make a Blueprint for goals
like_bp = Blueprint('like_bp', __name__)


#Routes

@like_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_likes(id):
    try:
        likes = Like.query.filter_by(goal_id=id).all()
        total_likes = len(likes)
        return jsonify({"total_likes": total_likes})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@like_bp.route('/<int:id>', methods=['POST'])
@jwt_required()
def like_goal(id):
    try:
        user_id = get_jwt_identity()
        goal = SavingsGoal.query.get(id)
        
        if not goal:
            return jsonify({"error": "Goal not found"}), 404
        
        like = Like.query.filter_by(user_id=user_id, goal_id=id, status = True).first()
        if like:
            like.status = False
            db.session.commit()
            return jsonify({"message": "Unliked"}), 200
        else:
            new_like = Like(
                user_id=user_id,
                goal_id=id,
                date = datetime.now(),
                status = True
            )
            db.session.add(new_like)
            db.session.commit()
            return jsonify({"message": "Liked"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500