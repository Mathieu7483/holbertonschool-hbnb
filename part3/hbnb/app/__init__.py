from flask import Flask
from flask_restx import Api
from .services.facade import HBnBFacade
from flask_bcrypt import Bcrypt
from app.extensions import bcrypt, jwt
from flask_sqlalchemy import SQLAlchemy


HBnB_FACADE = HBnBFacade()
db = SQLAlchemy()

def create_app(config_class="config.DevelopmentConfig"):

    # 1. Initialize Flask application
    app = Flask(__name__)

    # 2. Load configuration from the provided config class
    app.config.from_object(config_class)

    # 3. Initialize JWT Manager and Bcrypt 🔒
    app.config['JWT_SECRET_KEY'] = app.config.get('SECRET_KEY', 'super-secret')
    jwt.init_app(app)

    # initialize Bcrypt extension
    global bcrypt
    bcrypt.init_app(app)

    # 4. DEFINE Swagger Authorizations
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

    # 6. Initialize database
    db.init_app(app)

    # 7. Register API namespaces (blueprints)
    from app.api.v2.users import users_ns
    from app.api.v2.places import places_ns
    from app.api.v2.reviews import reviews_ns
    from app.api.v2.amenities import amenities_ns
    from app.api.v2.auth import auth_ns
    from app.api.v2.protected import protected_ns

    # Add namespaces with prefix
    api.add_namespace(users_ns, path='/api/v2/users')
    api.add_namespace(places_ns, path='/api/v2/places')
    api.add_namespace(reviews_ns, path='/api/v2/reviews')
    api.add_namespace(amenities_ns, path='/api/v2/amenities')
    api.add_namespace(auth_ns, path='/api/v2/auth')
    api.add_namespace(protected_ns, path='/api/v2/protected')


    return app
