"""Review class"""
from flask_sqlalchemy import SQLAlchemy
from .base import BaseModel
from hbnb_app import db
from datetime import datetime

class Review(BaseModel):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)

    

 

    def validate_text(self, value):
        if not value or not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Review text must be a non-empty string")
        return value.strip()

    def validate_rating(self, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user.id,
            "place_id": self.place.id,
            "user": {
                "id": self.user.id,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name
            },
            "place": {
                "id": self.place.id,
                "title": self.place.title
            },
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

