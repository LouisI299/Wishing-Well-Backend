#Imports
from flask import Blueprint, request, jsonify
from ..models import SavingsGoal, Transaction, User, Streak
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

#Make a Blueprint for goals
transaction_bp = Blueprint('transaction_bp', __name__)

@transaction_bp.route('/', methods=['POST'])
@jwt_required()
def create_transaction():
    try:
        data = request.get_json()
        goal_id = data['goal_id']
        amount = data['amount']
        type = data['type']
        user_id = get_jwt_identity()
        
        user = User.query.get(user_id)
        active_streak = Streak.query.filter_by(user_id=user_id, status = True).first()
        
        
        new_transaction = Transaction(
            goal_id=goal_id,
            amount=amount,
            transaction_date=datetime.now(),
            type=type
        )
        
        db.session.add(new_transaction)
        
        
        transaction_goal = SavingsGoal.query.get(goal_id)
        if type == 'deposit':
            transaction_goal.current_amount += amount
        else:
            transaction_goal.current_amount -= amount
        
        points_gained = (amount / transaction_goal.period_amount) * 10
        if active_streak:
            points_gained = points_gained * active_streak.current_streak
            
        user.points += points_gained
        
        while user.points >= user.level * 100:
            user.points -= user.level * 100
            user.level += 1
        
        db.session.commit()
        
        
        return jsonify({"message": "Transaction created successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500