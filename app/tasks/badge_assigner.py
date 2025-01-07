
from app import db, create_app

def assign_badges():
    app = create_app()
    
    with app.app_context():
        from app.models import User, Badge
        
        users = User.query.all()
        badge_mapping = {
            "Streak 1": {"condition": lambda user: user.streak.current_streak >= 1},
            "Streak 3": {"condition": lambda user: user.streak.current_streak >= 3},
            "Streak 5": {"condition": lambda user: user.streak.current_streak >= 5},
            "Level 5": {"condition": lambda user: user.level >= 5},
            "Level 10": {"condition": lambda user: user.level >= 10},
            "Totaal €1000": {"condition": lambda user: sum(goal.current_amount for goal in user.goals) >= 1000},
            "Totaal €2000": {"condition": lambda user: sum(goal.current_amount for goal in user.goals) >= 2000},
        }

        for user in users:
            for badge_name, badge_data in badge_mapping.items():
                badge = Badge.query.filter_by(name=badge_name).first()
                if badge and badge_data['condition'](user):
                    if badge not in user.badges:
                        user.badges.append(badge)
                        print(f"Badge '{badge_name}' Assigned to user: {user.first_name}")

        db.session.commit()
