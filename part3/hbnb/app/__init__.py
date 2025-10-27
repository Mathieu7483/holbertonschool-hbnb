from flask import Flask
from flask_restx import Api
from .services.facade import HBnBFacade
from flask_bcrypt import Bcrypt
from app.extensions import bcrypt, jwt

HBnB_FACADE = HBnBFacade()


def create_app(config_class="config.DevelopmentConfig"):

    # Initialize Flask application
    app = Flask(__name__)

    # Load configuration from the provided config class
    app.config.from_object(config_class)

    # Initialize JWT Manager
    app.config['JWT_SECRET_KEY'] = app.config.get('SECRET_KEY', 'super-secret')  # Ensure a secret key is set
    jwt.init_app(app)

    #initialize Bcrypt extension
    global bcrypt
    bcrypt.init_app(app)

    # Initialize Flask-RESTX API with Swagger documentation
    api = Api(
        app,
        version='2.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v2/docs'  # URL for Swagger UI
    )

    # Register API namespaces (blueprints)
    from app.api.v2.users import users_ns
    from app.api.v2.places import places_ns
    from app.api.v2.reviews import reviews_ns
    from app.api.v2.amenities import amenities_ns

    # Add namespaces without additional prefix
    api.add_namespace(users_ns, path='/api/v2/users')
    api.add_namespace(places_ns, path='/api/v2/places')
    api.add_namespace(reviews_ns, path='/api/v2/reviews')
    api.add_namespace(amenities_ns, path='/api/v2/amenities')

    # Initialize Bcrypt for password hashing
    bcrypt = Bcrypt()
    bcrypt.init_app(app)
    return app