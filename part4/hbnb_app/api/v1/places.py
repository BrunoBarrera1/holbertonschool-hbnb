from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from hbnb_app.services import facade


api = Namespace('places', description='Place operations')

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        data = request.get_json()
        if not data:
            api.abort(400, 'No input data provided')

        from flask_jwt_extended import get_jwt
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)
        data['owner_id'] = current_user_id
        data['user'] = {
            'id': current_user_id,
            'is_admin': is_admin
        }

        try:                                                    
            place = facade.create_place(data)
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner_id': place.owner.id,
                'amenities': [a.id for a in place.amenities]
            }, 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f'place {place_id} not found')
        return place.to_dict(), 200
    
    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        data = request.get_json()
        if not data:
            api.abort(400, 'No input data provided')

        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f'Place {place_id} not found')

        current_user = get_jwt_identity()
        user_id = current_user.get('id') if isinstance(current_user, dict) else current_user
        is_admin = current_user.get('is_admin', False) if isinstance(current_user, dict) else False

        if place.owner.id != user_id and not is_admin:
            api.abort(403, 'Unauthorized action')

        if 'owner_id' in data and data['owner_id'] != str(place.owner.id):
                api.abort(400, 'Changing the owner of a place is not allowed')

                    
        if 'amenities' in data:
            amenity_ids = []
            for amenity in data['amenities']:
                if isinstance(amenity, int) or (isinstance(amenity, str) and amenity.isdigit()):
                    amenity_ids.append(int(amenity))
                else:
                    found = None
                    for a in facade.get_all_amenities():
                        if a.name == amenity:
                            found = a.id
                            break
                    if found is not None:
                        amenity_ids.append(found)
                    else:
                        api.abort(400, f"Amenity '{amenity}' not found")
            data['amenities'] = amenity_ids
        try:
            updated = facade.update_place(place_id, data)
            if not updated:
                api.abort(404, f'Place {place_id} not found')
            return {'message': 'Place updated successfully'}, 200
        except ValueError as e:
            api.abort(400, str(e))

    @jwt_required()
    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    def delete(self, place_id):
        """delete a place"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f'place {place_id} not found')

        current_user = get_jwt_identity()
        user_id = current_user.get('id') if isinstance(current_user, dict) else current_user
        is_admin = current_user.get('is_admin', False) if isinstance(current_user, dict) else False

        if not is_admin:
            if not place.owner or place.owner.id != user_id:
                api.abort(403, 'unauthorized action')

        facade.delete_place(place_id)
        return {'message': 'Place deleted successfully'}, 200

