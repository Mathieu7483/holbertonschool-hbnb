from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import HBnB_FACADE

facade = HBnB_FACADE
amenities_ns = Namespace('amenities', description='Amenity operations')

# Decorator admin_required
def admin_required():
    """Custom decorator to ensure the authenticated user has Admin privilege."""
    def wrapper(fn):
        @jwt_required()
        def decorated_view(*args, **kwargs):
            claims = get_jwt()
            if claims.get("is_admin", False) is not True:
                amenities_ns.abort(403, message="Access forbidden: Admin privilege required.")
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

# Input model
amenity_model = amenities_ns.model('Amenity', {
    'name': fields.String(required=True, description='Amenity name')
})

# Response model
amenity_response_model = amenities_ns.model('AmenityResponse', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Amenity name'),
    'created_at': fields.String(description='Creation date'),
    'updated_at': fields.String(description='Last update date')
})

error_model = amenities_ns.model('Error', {
    'message': fields.String(description='Error message'),
})

@amenities_ns.route('/')
class AmenityList(Resource):
    @amenities_ns.doc('list_amenities')
    @amenities_ns.marshal_list_with(amenity_response_model)
    @amenities_ns.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve all amenities (Public)"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

    @amenities_ns.doc('create_amenity', security='jwt')
    @amenities_ns.expect(amenity_model, validate=True)
    @amenities_ns.marshal_with(amenity_response_model, code=201)
    @amenities_ns.response(201, 'Amenity created successfully')
    @amenities_ns.response(400, 'Invalid input data', error_model)
    @amenities_ns.response(403, 'Forbidden: Admin required', error_model)
    @amenities_ns.response(409, 'Amenity already exists', error_model)
    @admin_required()
    def post(self):
        """Create a new amenity (Admin only)"""
        amenity_data = amenities_ns.payload

        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except ValueError as e:
            if "already exists" in str(e).lower():
                amenities_ns.abort(409, message=str(e))
            amenities_ns.abort(400, message=str(e))

@amenities_ns.route('/<amenity_id>')
class AmenityResource(Resource):
    @amenities_ns.doc('get_amenity')
    @amenities_ns.marshal_with(amenity_response_model)
    @amenities_ns.response(200, 'Amenity details retrieved successfully')
    @amenities_ns.response(404, 'Amenity not found', error_model)
    def get(self, amenity_id):
        """Get amenity details by ID (Public)"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            amenities_ns.abort(404, message='Amenity not found')
        
        return amenity.to_dict(), 200

    @amenities_ns.doc('update_amenity', security='jwt')
    @amenities_ns.expect(amenity_model, validate=True)
    @amenities_ns.marshal_with(amenity_response_model)
    @amenities_ns.response(200, 'Amenity updated successfully')
    @amenities_ns.response(404, 'Amenity not found', error_model)
    @amenities_ns.response(400, 'Invalid input data', error_model)
    @amenities_ns.response(403, 'Forbidden: Admin required', error_model)
    @amenities_ns.response(409, 'Amenity name already exists', error_model)
    @admin_required()
    def put(self, amenity_id):
        """Update an amenity (Admin only)"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            amenities_ns.abort(404, message='Amenity not found')

        amenity_data = amenities_ns.payload

        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            if not updated_amenity:
                amenities_ns.abort(404, message='Amenity not found')
            
            return updated_amenity.to_dict(), 200
            
        except ValueError as e:
            if "already exists" in str(e).lower():
                amenities_ns.abort(409, message=str(e))
            amenities_ns.abort(400, message=str(e))
