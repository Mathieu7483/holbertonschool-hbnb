from flask import request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import HBnB_FACADE

facade = HBnB_FACADE
# Namespace description for Swagger
places_ns = Namespace('places', description='Place operations')

def admin_required():
    def wrapper(fn):
        @jwt_required()
        def decorated_view(*args, **kwargs):
            claims = get_jwt()
            if claims.get("is_admin", False) is not True:
                places_ns.abort(403, message="Access forbidden: Admin privilege required.")
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

user_model = places_ns.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email')
})

amenity_model = places_ns.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Amenity name')
})

place_input_model = places_ns.model('PlaceInput', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'owner_id': fields.String(required=True, description='Owner ID'),
    'amenities': fields.List(fields.String, required=True, description="List of amenity IDs")
})

place_update_model = places_ns.model('PlaceUpdate', {
    'title': fields.String(required=False, description='Place title'),
    'description': fields.String(required=False, description='Place description'),
    'price': fields.Float(required=False, description='Price per night'),
    'latitude': fields.Float(required=False, description='Latitude'),
    'longitude': fields.Float(required=False, description='Longitude'),
    'amenities': fields.List(fields.String, required=False, description='List of amenity IDs')
})

place_response_model = places_ns.model('PlaceResponse', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude'),
    'owner': fields.Nested(user_model, description='Owner details'),
    'amenities': fields.List(fields.String, description='Amenities IDs'),
    'reviews_count': fields.Integer(description='Number of reviews'),
    'created_at': fields.String(description='Creation date'),
    'updated_at': fields.String(description='Last update date')
})

error_model = places_ns.model('Error', {
    'message': fields.String(description='Error message'),
})

@places_ns.route('/')
class PlaceList(Resource):
    @places_ns.doc('create_place', security='jwt', description='Create a new Place (Requires authentication, owner_id must match token)')
    @places_ns.expect(place_input_model, validate=True)
    @places_ns.marshal_with(place_response_model, code=201)
    @places_ns.response(201, 'Place successfully created')
    @places_ns.response(400, 'Invalid input data', error_model)
    @places_ns.response(403, 'Unauthorized action', error_model)
    @places_ns.response(404, 'Owner or Amenity not found', error_model)
    @jwt_required()
    def post(self):
        """Create a new Place (Authenticated users only)"""
        user_id = get_jwt_identity()
        place_data = places_ns.payload
        
        if place_data.get('owner_id') != user_id:
            places_ns.abort(403, message="Unauthorized: owner_id must match authenticated user.")

        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
        except ValueError as e:
            error_str = str(e).lower()
            if "not found" in error_str:
                places_ns.abort(404, message=str(e))
            places_ns.abort(400, message=str(e))
        except Exception as e:
            places_ns.abort(400, message=str(e))

    @places_ns.doc('list_places', description='Retrieve a list of all existing places.')
    @places_ns.marshal_list_with(place_response_model)
    @places_ns.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve all Places (Public)"""
        places_list = facade.get_all_places()
        return [place.to_dict() for place in places_list], 200

@places_ns.route('/<string:place_id>')
# Parameter description for the route variable
@places_ns.param('place_id', 'The unique identifier of the Place') 
class PlaceResource(Resource):
    @places_ns.doc('get_place', description='Retrieve details for a specific Place by ID.')
    @places_ns.marshal_with(place_response_model)
    @places_ns.response(200, 'Place details retrieved successfully')
    @places_ns.response(404, 'Place not found', error_model)
    def get(self, place_id):
        """Get Place details by ID (Public)"""
        place = facade.get_place(place_id)
        
        if not place:
            places_ns.abort(404, message=f"Place with ID '{place_id}' not found")
        
        return place.to_dict(), 200

    @places_ns.doc('update_place', security='jwt', description='Update an existing Place. Only the owner or an Admin can modify.')
    @places_ns.expect(place_update_model, validate=True)
    @places_ns.marshal_with(place_response_model)
    @places_ns.response(200, 'Place updated successfully')
    @places_ns.response(404, 'Place not found', error_model)
    @places_ns.response(400, 'Invalid input data', error_model)
    @places_ns.response(403, 'Unauthorized action', error_model)
    @jwt_required()
    def put(self, place_id):
        """Update a Place (Owner or Admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        place_data = places_ns.payload
        
        place = facade.get_place(place_id)
        
        if not place:
            places_ns.abort(404, message=f"Place with ID '{place_id}' not found")
        
        if place.owner_id != current_user_id and not is_admin:
            places_ns.abort(403, message="Unauthorized: You can only update your own places.")

        if 'owner_id' in place_data and not is_admin:
            places_ns.abort(403, message="Unauthorized: Only admins can change owner_id.")

        try:
            updated_place = facade.update_place(place_id, place_data)
            
            if not updated_place:
                places_ns.abort(404, message=f"Place with ID '{place_id}' not found")
            
            return updated_place.to_dict(), 200
            
        except ValueError as e:
            error_str = str(e).lower()
            if "not found" in error_str:
                places_ns.abort(404, message=str(e))
            places_ns.abort(400, message=str(e))
        except Exception as e:
            places_ns.abort(400, message=str(e))

    @places_ns.doc('delete_place', security='jwt', description='Delete a Place. Only accessible to Admins.')
    @places_ns.response(204, 'Place successfully deleted')
    @places_ns.response(401, 'Unauthorized', error_model)
    @places_ns.response(403, 'Forbidden: Admin required', error_model)
    @places_ns.response(404, 'Place not found', error_model)
    @admin_required()
    def delete(self, place_id):
        """Delete a Place (Admin only)"""
        is_deleted = facade.delete_place(place_id)
        
        if not is_deleted:
            places_ns.abort(404, message=f"Place with ID '{place_id}' not found")

        return None, 204