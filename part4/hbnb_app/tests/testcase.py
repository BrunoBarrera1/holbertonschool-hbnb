from part2.app.models.user import User
from part2.app.models.place import Place
from part2.app.models.review import Review
from part2.app.models.amenity import Amenity

def test_user_creation():
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False  # Valor por defecto
    assert len(user.places) == 0   # Lista de lugares vacía inicialmente
    print("User creation test passed!")
