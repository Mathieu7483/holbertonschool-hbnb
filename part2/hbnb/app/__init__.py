from flask import Flask
from flask_restx import Api
from .services.facade import HBnBFacade 

HBnB_FACADE = HBnBFacade()

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Register the route namespace
    from .api.v1.users import users_ns
    from .api.v1.amenities import amenities_ns
    from .api.v1.places import places_ns
    from .api.v1.reviews import reviews_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    return app


    
