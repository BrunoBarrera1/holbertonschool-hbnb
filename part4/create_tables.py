from hbnb_app import create_app, db
from hbnb_app.models import *  # para registrar modelos

app = create_app()

with app.app_context():
    db.create_all()
    print("Tablas creadas.")