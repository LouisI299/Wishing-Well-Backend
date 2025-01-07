from app import create_app, db
from app.models import Badge

app = create_app()

with app.app_context():
    badges = Badge.query.all()
    for badge in badges:
        if badge.image_url.startswith("/static/images/badges//"):
            badge.image_url = badge.image_url.replace("/static/images/badges//", "/static/images/badges/")
            db.session.add(badge)
    
    db.session.commit()
    print("Badge paden succesvol gecorrigeerd!")
