from app import create_app, db
from app.models.user import User

app = create_app()
app.app_context().push()


user = User.query.filter_by(email="admin@example.com").first()
if user:
    db.session.delete(user)
    db.session.commit()

admin = User(
    first_name="Admin",
    last_name="User",
    email="admin@example.com",
    is_admin=True
)
admin.set_password("admin123")
  # Set a
db.session.add(admin)
db.session.commit()

print("Admin creado correctamente")
