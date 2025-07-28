from hbnb_app import bcrypt, create_app, db
from hbnb_app.models.user import User

app = create_app()
app.app_context().push()

user = User.query.filter_by(email="admin@example.com").first()
print(f"Usuario: {user.email}")
print(f"Password almacenado: {user.password}")

password_correct = bcrypt.check_password_hash(user.password, "admin123")
print("Contraseña correcta" if password_correct else "Contraseña incorrecta")