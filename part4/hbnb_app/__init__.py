import os
from flask import Flask, jsonify
from flask_restx import Api
from config import DevelopmentConfig
from hbnb_app.extensions import bcrypt, jwt, db

authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"'
    }
}

def create_app(config_class=DevelopmentConfig):
    # Rutas absolutas a templates y static
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(config_class)

    # Init extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # Import models so SQLAlchemy knows them
    import hbnb_app.models  

    # JWT error handlers
    import logging
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        logging.warning(f"JWT unauthorized: {callback}")
        return jsonify({'msg': 'Missing Authorization Header'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        logging.warning(f"JWT invalid token: {callback}")
        return jsonify({'msg': 'Invalid token', 'debug': str(callback)}), 422

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        logging.warning(f"JWT expired: header={jwt_header}, payload={jwt_payload}")
        return jsonify({'msg': 'Token has expired'}), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        logging.warning(f"JWT revoked: header={jwt_header}, payload={jwt_payload}")
        return jsonify({'msg': 'Token has been revoked'}), 401

    # Swagger API setup
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='API for managing places, users, reviews, and amenities',
        prefix='/api/v1',
        doc='/api/docs',
        authorizations=authorizations,
        security='Bearer'
    )

    # Register Namespaces
    from hbnb_app.api.v1.places    import api as places_ns
    from hbnb_app.api.v1.users     import api as users_ns
    from hbnb_app.api.v1.reviews   import api as reviews_ns
    from hbnb_app.api.v1.amenities import api as amenities_ns
    from hbnb_app.api.v1.auth      import api as auth_ns

    api.add_namespace(users_ns,     path='/users')
    api.add_namespace(places_ns,    path='/places')
    api.add_namespace(reviews_ns,   path='/reviews')
    api.add_namespace(amenities_ns, path='/amenities')
    api.add_namespace(auth_ns,      path='/auth')

    # Register frontend Blueprint
    from hbnb_app.frontend_routes import frontend
    app.register_blueprint(frontend)

    return app
