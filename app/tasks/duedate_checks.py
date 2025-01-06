from datetime import datetime, timedelta
import logging
from app import create_app, db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_due_date():
    app = create_app()
    
    with app.app_context(): 
        from app.models import SavingsGoal
        
        #Get all goals
        weekly_goals = SavingsGoal.query.filter_by(status = True, saving_method = False).all()  
        monthly_goals = SavingsGoal.query.filter_by(status = True, saving_method = True).all()
        
        for goal in weekly_goals:
            if goal.next_due_date < datetime.now():
                goal.next_due_date = goal.next_due_date + timedelta(weeks=1)
                db.session.commit()
        
        for goal in monthly_goals:
            if goal.next_due_date < datetime.now():
                goal.next_due_date = goal.next_due_date + timedelta(weeks=4)
                db.session.commit()

                