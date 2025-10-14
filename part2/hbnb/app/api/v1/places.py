from flask_restx import Namespace, Resource, fields
from app.services import facade

places_ns = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = places_ns.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = places_ns.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = places_ns.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@places_ns.route('/')
class PlaceList(Resource):
    @places_ns.expect(place_model)
    @places_ns.response(201, 'Place successfully created')
    @places_ns.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        # Placeholder for the logic to register a new place
        pass

    @places_ns.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        # Placeholder for logic to return a list of all places
        pass

@places_ns.route('/<place_id>')
class PlaceResource(Resource):
    @places_ns.response(200, 'Place details retrieved successfully')
    @places_ns.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        # Placeholder for the logic to retrieve a place by ID, including associated owner and amenities
        pass

    @places_ns.expect(place_model)
    @places_ns.response(200, 'Place updated successfully')
    @places_ns.response(404, 'Place not found')
    @places_ns.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        # Placeholder for the logic to update a place by ID
        pass