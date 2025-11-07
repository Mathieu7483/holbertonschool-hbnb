from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import HBnB_FACADE
facade = HBnB_FACADE


amenities_ns = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = amenities_ns.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# Model for amenity response
amenity_response_model = amenities_ns.model('AmenityResponse', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity'),
    'created_at': fields.String(description='Creation date'),
    'updated_at': fields.String(description='Last update date')
})

@amenities_ns.route('/')
class AmenityList(Resource):
    @amenities_ns.doc('list_amenities')
    @amenities_ns.marshal_list_with(amenity_response_model)
    @amenities_ns.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return amenities, 200

    @amenities_ns.doc('create_amenity')
    @amenities_ns.expect(amenity_model, validate=True)
    @amenities_ns.response(201, 'Amenity successfully created')
    @amenities_ns.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = amenities_ns.payload

        try:
            # Create new amenity
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400

@amenities_ns.route('/<amenity_id>')
class AmenityResource(Resource):
    @amenities_ns.doc('get_amenity')
    @amenities_ns.response(200, 'Amenity details retrieved successfully')
    @amenities_ns.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name,
            'created_at': amenity.created_at,
            'updated_at': amenity.updated_at
        }, 200

    @amenities_ns.doc('update_amenity')
    @amenities_ns.expect(amenity_model, validate=True)
    @amenities_ns.response(200, 'Amenity updated successfully')
    @amenities_ns.response(404, 'Amenity not found')
    @amenities_ns.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        amenity_data = amenities_ns.payload

        try:
            # Update amenity using the model's update method
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            if not updated_amenity:
                amenities_ns.abort(404, message='Amenity not found')
            return {
                'id': updated_amenity.id,
                'name': updated_amenity.name,
                'created_at': updated_amenity.created_at,
                'updated_at': updated_amenity.updated_at
            }, 200
        except Exception as e:
            amenities_ns.abort(400, message=str(e))