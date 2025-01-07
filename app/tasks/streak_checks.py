from datetime import datetime, timedelta
import logging
from app import create_app, db
from app.tasks.email import send_mail  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_user_streaks():
    app = create_app()
    
    with app.app_context():   
        from app.models import User, SavingsGoal, Transaction, Streak
    
        
        #Get all users
        users = User.query.all()

        for user in users:
            user_id = user.id
            email = user.email
            #Get all active weekly and monthly goals for the user
            weekly_goals = SavingsGoal.query.filter_by(user_id=user_id, status=True, saving_method=False).all()
            monthly_goals = SavingsGoal.query.filter_by(user_id=user_id, status=True, saving_method=True).all()

            all_on_track = True

            if not weekly_goals and not monthly_goals:
                all_on_track = False
                continue

            for goal in weekly_goals:
                four_weeks_ago = datetime.now() - timedelta(weeks=4)
                 #Get all transactions for the goal
                transactions = Transaction.query.filter(Transaction.goal_id == goal.id, Transaction.transaction_date >= four_weeks_ago).all()
                total_saved = sum([transaction.amount for transaction in transactions])

                #Check if the user is on track
                if total_saved < (goal.period_amount * 4):
                    all_on_track = False
                    break 

            if all_on_track:
                for goal in monthly_goals:
                    one_month_ago = datetime.now() - timedelta(weeks=4)
                    transactions = Transaction.query.filter(Transaction.goal_id == goal.id, Transaction.transaction_date >= one_month_ago).all()
                    total_saved = sum([transaction.amount for transaction in transactions])

                    if total_saved < goal.period_amount:
                        all_on_track = False
                        break

            active_streak = Streak.query.filter_by(user_id=user_id, status=True).first()

            if all_on_track:
                if active_streak:
                    if active_streak.check_date < datetime.now() - timedelta(weeks=4):
                        active_streak.current_streak = 1
                        active_streak.check_date = datetime.now()
                else:
                    streak = Streak(
                        user_id=user_id, 
                        start_date=datetime.now(), 
                        check_date=datetime.now(),
                        status=True,
                        current_streak=1
                        )
                    db.session.add(streak)
            else:
                # email sent when streak ends tomorrow
                if active_streak and active_streak.check_date == datetime.now() - timedelta(weeks=4) + timedelta(days=1):
                    subject = "Warning - streak ends tomorrow"
                    body = f"Hello {user.first_name}, your streak ends tommorow. Make a deposit to keep the streak!"
                    send_mail(subject, [email], body)
                
                # email sent wen streak is lost
                if active_streak and active_streak.check_date < datetime.now() - timedelta(weeks=4):
                    active_streak.status = False
                    active_streak.end_date = datetime.now()
                    subject = "Streak Lost"
                    body = f"Hello {user.first_name}, unfortunatly you lost your streak. no worries you can make a deposit and start again!"
                    send_mail(subject, [email], body)

            db.session.commit()
