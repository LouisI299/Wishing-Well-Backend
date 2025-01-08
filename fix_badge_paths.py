from app import create_app, db
from app.models import Badge

app = create_app()

with app.app_context():
    badges = Badge.query.all()
    for badge in badges:
        badge.image_url = badge.image_url.replace("//static/images/badges/", "/static/images/badges/")
        badge.image_url = badge.image_url.replace("/static/images/badges//", "/static/images/badges/")
        
        if not badge.image_url.startswith("/static/images/badges/"):
            badge.image_url = f"/static/images/badges/{badge.image_url.split('/')[-1]}"
        
        db.session.add(badge)

    db.session.commit()
    print("Badge paden zijn nu correct aangepast!")
