# app/api/__init__.py
from flask_restx import Api

api = Api(title='HBnB API', version='1.0')

from .v1.reviews import api as reviews_ns
from .v1.amenities import api as amenities_ns
from .v1.users import api as users_ns
from .v1.places import api as places_ns


api.add_namespace(reviews_ns, path="/api/v1/reviews")
api.add_namespace(amenities_ns, path="/api/v1/amenities")
api.add_namespace(users_ns, path="/api/v1/users")
api.add_namespace(places_ns, path="/api/v1/places")
