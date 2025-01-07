#Imports
from flask import Blueprint, request, jsonify
from ..models import Friendship, User, SavingsGoal, Comment
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta

#Make a Blueprint for goals
comment_bp = Blueprint('comment_bp', __name__)

#Routes

@comment_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_comments(id):
    try:
        comments = Comment.query.filter_by(goal_id=id).all()
        return jsonify([comment.serialize() for comment in comments])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@comment_bp.route('/<int:id>', methods=['POST'])
@jwt_required()
def create_comment(id):
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        goal = SavingsGoal.query.get(id)
        
        if not goal:
            return jsonify({"error": "Goal not found"}), 404
        
        new_comment = Comment(
            user_id=user_id,
            goal_id=id,
            text=data['text'],
            date = datetime.now()
        )
        db.session.add(new_comment)
        db.session.commit()
        return jsonify(new_comment.serialize()), 200
    except Exception as e:
        return jsonify({"error": str (e)}), 500