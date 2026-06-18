from ext import app, db
from routes import *


with app.app_context():
    ensure_database_schema()


if __name__ == "__main__":
    app.run(debug=True)
