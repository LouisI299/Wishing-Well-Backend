from app import create_app, db
from app.models import Badge

app = create_app()

with app.app_context():
    base_path = "/static/images/badges/"
    badge_updates = {
        "Streak 1": f"{base_path}streak1.png",
        "Streak 3": f"{base_path}streak3.png",
        "Streak 5": f"{base_path}streak5.png",
        "Level 5": f"{base_path}level5.png",
        "Level 10": f"{base_path}level10.png",
        "Totaal €1000": f"{base_path}total1000.png",
        "Totaal €2000": f"{base_path}total2000.png"
    }

    for name, url in badge_updates.items():
        badge = Badge.query.filter_by(name=name).first()
        if badge:
            badge.image_url = url
            db.session.add(badge)

    db.session.commit()
    print("Badge paden succesvol bijgewerkt!")
