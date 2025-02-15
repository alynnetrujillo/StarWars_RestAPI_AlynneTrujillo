from models import db, Planets
from app import app

# Create several planets 
with app.app_context():

    p1 = Planets(name="Earth")
    p2 = Planets(name="Mars")

    db.session.add(p1)
    db.session.add(p2)

    db.session.commit()