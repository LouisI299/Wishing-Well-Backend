from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Badge, User
from app import db

badge_bp = Blueprint('badge_bp', __name__)

@badge_bp.route('/badges', methods=['GET'])
def get_all_badges():
    badges = Badge.query.all()
    return jsonify([{
        'id': badge.id,
        'name': badge.name,
        'description': badge.description,
        'image_url': badge.image_url
    } for badge in badges]), 200

@badge_bp.route('/user/badges', methods=['GET'])
@jwt_required()
def get_user_badges():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify([{
        'id': badge.id,
        'name': badge.name,
        'description': badge.description,
        'image_url': badge.image_url
    } for badge in user.badges]), 200

# add badge remotly (admin only)
@badge_bp.route('/user/<int:user_id>/badge/<int:badge_id>', methods=['POST'])
@jwt_required()
def assign_badge_to_user(user_id, badge_id):
    user = User.query.get(user_id)
    badge = Badge.query.get(badge_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    if not badge:
        return jsonify({"error": "Badge not found"}), 404
    
    if badge in user.badges:
        return jsonify({"message": "User already has this badge"}), 400
    
    user.badges.append(badge)
    db.session.commit()
    
    return jsonify({"message": f"Badge '{badge.name}' assigned to user '{user.first_name}'"}), 200

@badge_bp.route('/badges/<int:badge_id>', methods=['GET'])
def get_badge(badge_id):
    badge = Badge.query.get(badge_id)
    if not badge:
        return jsonify({"error": "Badge not found"}), 404
    
    return jsonify({
        'id': badge.id,
        'name': badge.name,
        'description': badge.description,
        'image_url': badge.image_url
    }), 200
