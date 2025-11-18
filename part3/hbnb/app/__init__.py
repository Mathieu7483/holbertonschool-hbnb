from flask import Flask
from flask_restx import Api
from app.extensions import bcrypt, jwt, db
from flask_cors import CORS

# Import models to ensure they are registered with SQLAlchemy
import app.models

HBnB_FACADE = None

def create_app(config_class="config.DevelopmentConfig"):
    """App Factory function to create and configure the Flask application"""
    global HBnB_FACADE
    
    # 1. Initialize Flask application
    app = Flask(__name__)
    CORS(app)

    # 2. Load configuration from the provided config class
    app.config.from_object(config_class)

    # 3. Initialize extensions
    jwt.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)

    # create database tables
    with app.app_context():
        db.create_all()
        
        if HBnB_FACADE is None:
            from .services.facade import HBnBFacade
            HBnB_FACADE = HBnBFacade()

    # 4. Define Swagger Authorizations
    authorizations = {
        'jwt': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Enter your token here in format: **Bearer <your_token_jwt>**"
        }
    }

    # 5. Initialize Flask-RESTX API with Swagger config
    api = Api(
        app,
        version='2.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v2/docs',
        authorizations=authorizations,
        security='jwt'
    )

    # 6. Register API namespaces (blueprints)
    from app.api.v2.users import users_ns
    from app.api.v2.places import places_ns
    from app.api.v2.reviews import reviews_ns
    from app.api.v2.amenities import amenities_ns
    from app.api.v2.auth import auth_ns

    # Add namespaces with prefix
    api.add_namespace(users_ns, path='/api/v2/users')
    api.add_namespace(places_ns, path='/api/v2/places')
    api.add_namespace(reviews_ns, path='/api/v2/reviews')
    api.add_namespace(amenities_ns, path='/api/v2/amenities')
    api.add_namespace(auth_ns, path='/api/v2/auth')

    return app

def get_facade():
    """Helper function to get the facade instance"""
    return HBnB_FACADE