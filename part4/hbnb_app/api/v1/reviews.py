from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from hbnb_app.services.facade import facade as hbnb_facade

api = Namespace('reviews', description='Review operations')

review_input_model = api.model('ReviewInput', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, min=1, max=5, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='Place ID')
})

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

review_list_model = api.model('ReviewList', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating (1-5)'),
    'user_id': fields.String(description='User ID'),
    'place_id': fields.String(description='Place ID')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_input_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User or Place not found')
    def post(self):
        """Create a new review"""
        import sys
        print("[DEBUG] Headers:", dict(request.headers), file=sys.stderr)
        try:
            data = request.get_json()
            print("[DEBUG] Review POST data:", data, file=sys.stderr)

            if 'user_id' in data:
                print("[DEBUG] user_id found in data, aborting", file=sys.stderr)
                api.abort(400, "You cannot manually set user_id")

            current_user = get_jwt_identity()
            print("[DEBUG] get_jwt_identity():", current_user, file=sys.stderr)
            if isinstance(current_user, dict) and 'id' in current_user:
                data['user_id'] = current_user['id']
            else:
                data['user_id'] = current_user
            review = hbnb_facade.create_review(data)
            print("[DEBUG] Review created:", review.to_dict(), file=sys.stderr)
            return review.to_dict(), 201
        except ValueError as e:
            print("[DEBUG] ValueError:", str(e), file=sys.stderr)
            api.abort(400, str(e))
        except Exception as e:
            print("[DEBUG] Exception:", str(e), file=sys.stderr)
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

    @jwt_required()
    @api.expect(review_input_model)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review (owner or admin only)"""
        try:
            review = hbnb_facade.get_review(review_id)
            if not review:
                api.abort(404, 'Review not found')

            current_user = get_jwt_identity()

            if not is_admin and review.user.id != current_user['id']:
                api.abort(403, 'Unauthorized action')
            data = request.get_json()
            updated_review = hbnb_facade.update_review(review_id, data)
            return updated_review.to_dict(), 200
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(404, str(e))
    
    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review (owner or admin only)"""
        try:
            review = hbnb_facade.get_review(review_id)
            if not review:
                api.abort(404, 'Review not found')

            current_user = get_jwt_identity()

            if not is_admin and review.user.id != current_user['id']:
                api.abort(403, 'Unauthorized action')
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

