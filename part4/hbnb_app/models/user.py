"""User class"""
import uuid
from .base import BaseModel
from hbnb_app import db, bcrypt
class User(BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)    
    
    places = db.relationship('Place', backref='owner', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', back_populates='owner', lazy=True, cascade='all, delete-orphan')
    

    def validate_email(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Email is required")
        email = value.strip().lower()
        if '@' not in email or '.' not in email:
            raise ValueError("Invalid email format")
        return email

    def __init__(self, *args, **kwargs):
        allowed_fields = ['first_name', 'last_name', 'email', 'password',]
        """prevents the user from creating an instance with fields not in allowed_fields"""
        if 'email' in kwargs:
            kwargs['email'] = self.validate_email(kwargs['email'])
        if 'password' in kwargs:
            if not str(kwargs['password']).startswith('$2b$'):
                self.set_password(kwargs['password'])
                kwargs.pop('password')
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in allowed_fields}
        super().__init__(*args, **filtered_kwargs)

    def validate_is_admin(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_admin must be a boolean")
        return value


    def set_password(self, password: str):
        """Sets the user's password (hashes it before storing)"""
        from hbnb_app import bcrypt
        if not password or not isinstance(password, str) or len(password) < 6:
            raise ValueError("Password must be a string with at least 6 characters.")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def hash_password(self, password: str):
        """DEPRECATED: Use set_password instead. Kept for backward compatibility."""
        self.set_password(password)

    def verify_password(self, password: str) -> bool:
        """Verifies a password against the stored hash"""
        from hbnb_app import bcrypt
        if not password:
            return False
        return bcrypt.check_password_hash(self.password, password)

    def add_place(self, place):
        """Add a place to the user list of owned places"""
        from .place import Place
        if not isinstance(place, Place):
            raise ValueError("Can only add Place instances")
        if place not in self.places:
            self.places.append(place)
    
    def add_review(self, review):
        """add a review to the user list"""
        from .review import Review
        if not isinstance(review, Review):
            raise ValueError("You can only add instances to review")
        if review not in self.reviews:
            self.reviews.append(review)

