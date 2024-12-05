from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    join_date = db.Column(db.DateTime, nullable=False)
    points = db.Column(db.Integer, nullable=False, default=0)
    level = db.Column(db.Integer, nullable=False, default=1)
    
class SavingsGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    target_amount = db.Column(db.Integer, nullable=False)
    current_amount = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    status = db.Column(db.String(50), nullable=False, default='In Progress')
    
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('savings_goal.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(50), nullable=False)
