from flask import Flask
from flask_restx import Api


from app.api.users import api as users_ns
from app.api.places import api as places_ns
from app.api.reviews import api as reviews_ns
from app.api.amenities import api as amenities_ns


def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/')

    api.add_namespace(users_ns, path='/api/users')
    api.add_namespace(places_ns, path='/api/places')
    api.add_namespace(reviews_ns, path='/api/reviews')
    api.add_namespace(amenities_ns, path='/api/amenities')

    return app
