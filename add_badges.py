from app import create_app, db
from app.models import Badge

app = create_app()

with app.app_context():
    badges = [
        {"name": "Streak 1", "description": "Behaald na 1 dag streak", "image_url": "streak1.png"},
        {"name": "Streak 3", "description": "Behaald na 3 dagen streak", "image_url": "streak3.png"},
        {"name": "Streak 5", "description": "Behaald na 5 dagen streak", "image_url": "streak5.png"},
        {"name": "Level 5", "description": "Behaald bij level 5", "image_url": "level5.png"},
        {"name": "Level 10", "description": "Behaald bij level 10", "image_url": "level10.png"},
        {"name": "Totaal €1000", "description": "Behaald bij €1000 gespaard", "image_url": "total1000.png"},
        {"name": "Totaal €2000", "description": "Behaald bij €2000 gespaard", "image_url": "total2000.png"},
    ]

    for badge in badges:
        if not Badge.query.filter_by(name=badge["name"]).first():
            db.session.add(Badge(**badge))

    db.session.commit()
    print("Badges succesvol toegevoegd!")
