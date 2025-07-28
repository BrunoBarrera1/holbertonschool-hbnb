from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from flask import request
from hbnb_app.services import facade

auth_ns = Namespace('auth', description='Authentication operations')

login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = request.get_json()

        user = facade.get_user_by_email(credentials['email'])

        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'is_admin': user.is_admin}
        )

        return {'access_token': access_token}, 200

api = auth_ns