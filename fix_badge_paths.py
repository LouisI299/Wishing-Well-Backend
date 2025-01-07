from app import create_app, db
from app.models import Badge

app = create_app()

with app.app_context():
    badges = Badge.query.all()
    for badge in badges:
        if "//static/images/badges/" in badge.image_url:
            badge.image_url = badge.image_url.replace("//static/images/badges/", "/static/images/badges/")
            db.session.add(badge)
        elif badge.image_url.startswith("/static/images/badges//"):
            badge.image_url = badge.image_url.replace("/static/images/badges//", "/static/images/badges/")
            db.session.add(badge)
        elif not badge.image_url.startswith("/static/images/badges/"):
            badge.image_url = f"/static/images/badges/{badge.image_url}"
            db.session.add(badge)

    db.session.commit()
    print("Badge paden succesvol gecorrigeerd!")
