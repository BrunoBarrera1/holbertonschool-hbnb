from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade as hbnb_facade

api = Namespace('reviews', description='Review operations')

# Review model for input
review_input_model = api.model('ReviewInput', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, min=1, max=5, description='Rating (1-5)'),
    'user_id': fields.String(required=True, description='User ID'),
    'place_id': fields.String(required=True, description='Place ID')
})

# Review model for response
review_response_model = api.model('ReviewResponse', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating (1-5)'),
    'user_id': fields.String(description='User ID'),
    'place_id': fields.String(description='Place ID'),
    'user': fields.Nested(api.model('ReviewUser', {
        'id': fields.String,
        'first_name': fields.String,
        'last_name': fields.String
    })),
    'place': fields.Nested(api.model('ReviewPlace', {
        'id': fields.String,
        'title': fields.String
    }))
})

# Simplified review model for lists
review_list_model = api.model('ReviewList', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating (1-5)'),
    'user_id': fields.String(description='User ID'),
    'place_id': fields.String(description='Place ID')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_input_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User or Place not found')
    def post(self):
        """Create a new review"""
        try:
            data = request.get_json()
            review = hbnb_facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(404, str(e))

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Get all reviews"""
        reviews = hbnb_facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get a review by ID"""
        review = hbnb_facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')
        return review.to_dict(), 200

    @api.expect(review_input_model)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review"""
        try:
            data = request.get_json()
            review = hbnb_facade.update_review(review_id, data)
            return review.to_dict(), 200
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(404, str(e))

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            hbnb_facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except ValueError as e:
            api.abort(404, str(e))

@api.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of place reviews retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a place"""
        try:
            reviews = hbnb_facade.get_reviews_by_place(place_id)
            return [r.to_dict() for r in reviews], 200
        except ValueError as e:
            api.abort(404, str(e))
