#Imports
from flask import Blueprint, request, jsonify
from ..models import Friendship, User
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta

#Make a Blueprint for goals
friend_bp = Blueprint('friend_bp', __name__)



#Routes

@friend_bp.route('/all', methods=['GET'])
@jwt_required()
def get_friends():
    try:
        user_id = get_jwt_identity()
        friendships_1 = Friendship.query.filter(
            Friendship.user_id1 == user_id,
            Friendship.status == True
        ).all()
        
        friendships_2 = Friendship.query.filter(
            Friendship.user_id2 == user_id,
            Friendship.status == True
        ).all()
        
        friend_ids = []
        
        for friendship in friendships_1:
            friend_ids.append(friendship.user_id2)
            
        for friendship in friendships_2:
            friend_ids.append(friendship.user_id1)
        
        
        friends = User.query.filter(User.id.in_(friend_ids)).all()
        if not friends:
            return jsonify([])
        return jsonify([friend.serialize() for friend in friends])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@friend_bp.route('/requests', methods=['GET'])
@jwt_required()
def get_requests():
    try:
        user_id = get_jwt_identity()
        friendships = Friendship.query.filter_by(user_id2=user_id, status=False).all()
        
        return jsonify([friendship.serialize() for friendship in friendships])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@friend_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_friend(id):
    try:
        friendship = Friendship.query.get(id)
        if friendship:
            friend_id = friendship.user_id2
            friend = User.query.get(friend_id)
            return jsonify(friend.serialize())
        else:
            return jsonify({"error": "Friend not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@friend_bp.route('/add', methods=['POST'])
@jwt_required()
def add_friend():
    try:
        data = request.get_json()
        if not data:
            raise ValueError("No data provided")
        
        user_id = get_jwt_identity()
        friend_id = data['friend_id']
        
        new_friendship = Friendship(
            user_id1=user_id,
            user_id2=friend_id,
            status=False,
            date = datetime.now()
        )
        
        db.session.add(new_friendship)
        db.session.commit()
        
        return jsonify(new_friendship.serialize()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@friend_bp.route('/accept/<int:id>', methods=['PUT'])
@jwt_required()
def accept_friend(id):
    try:
        friendship = Friendship.query.get(id)
        if friendship:
            friendship.status = True
            db.session.commit()
            return jsonify(friendship.serialize())
        else:
            return jsonify({"error": "Friend not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@friend_bp.route('/decline/<int:id>', methods=['DELETE'])
@jwt_required()
def decline_friend(id):
    try:
        friendship = Friendship.query.get(id)
        if friendship:
            db.session.delete(friendship)
            db.session.commit()
            return jsonify(friendship.serialize())
        else:
            return jsonify({"error": "Friend not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500   
    
