from flask import Blueprint, request, jsonify
from ..models import User
from datetime import datetime
from app import db

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])

@user_bp.route('/', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password'],
            join_date=datetime.now(),
            points=0,
            level=1
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
    