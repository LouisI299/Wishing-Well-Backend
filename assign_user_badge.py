from app import create_app, db
from app.models import UserBadge, Badge, User
from datetime import datetime

app = create_app()

with app.app_context():
    user = User.query.get(1)
    badge = Badge.query.get(1) 

    if user and badge:
        user_badge = UserBadge(user_id=user.id, badge_id=badge.id, awarded_at=datetime.utcnow())
        db.session.add(user_badge)
        db.session.commit()
        print(f"Badge '{badge.name}' succesvol toegewezen aan gebruiker '{user.first_name} {user.last_name}'")
    else:
        print("Gebruiker of badge niet gevonden!")
