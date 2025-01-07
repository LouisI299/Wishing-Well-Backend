from app import create_app, db
from app.models import User, Badge, UserBadge
from datetime import datetime

app = create_app()

with app.app_context():
    user_id = 1
    badge_id = 1 

    user = User.query.get(user_id)
    badge = Badge.query.get(badge_id)

    if user and badge:
        existing_badge = UserBadge.query.filter_by(user_id=user_id, badge_id=badge_id).first()
        if existing_badge:
            print("Badge is al toegewezen aan de gebruiker.")
        else:
            # Maak een nieuwe UserBadge aan
            new_user_badge = UserBadge(
                user_id=user_id,
                badge_id=badge_id,
                awarded_at=datetime.utcnow()
            )
            db.session.add(new_user_badge)
            db.session.commit()
            print(f"Badge '{badge.name}' succesvol toegewezen aan gebruiker '{user.first_name} {user.last_name}'.")
    else:
        if not user:
            print("Gebruiker niet gevonden.")
        if not badge:
            print("Badge niet gevonden.")
