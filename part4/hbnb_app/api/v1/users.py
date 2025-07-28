from flask_restx import Namespace, Resource, fields
from flask import request
from hbnb_app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

# Model for user registration
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password (min 6 characters)')
})

# Model for updating user info (only name fields)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid input')
    def post(self):

        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            api.abort(400, 'Email already registered')
        try:    
            new_user = facade.create_user(user_data)
        except ValueError as e:
            api.abort(400, str(e))
            
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201
@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200


    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid update fields')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Modify any user (admin only, including email/password)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            api.abort(403, 'Admin privileges required')

        data = request.get_json() or {}

        if 'email' in data:
            existing = facade.get_user_by_email(data['email'])
            if existing and existing.id != user_id:
                api.abort(400, 'Email already in use')

        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')

        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.set_password(data['password'])

        facade.user_repo.update(user)
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
       

