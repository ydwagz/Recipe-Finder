from ext import app, db
from models import Recipe, Review

with app.app_context():
    db.create_all()
