from ext import app, db
from routes import ensure_database_schema

with app.app_context():
    ensure_database_schema()
