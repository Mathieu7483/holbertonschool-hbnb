from flask import request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import HBnB_FACADE

facade = HBnB_FACADE
places_ns = Namespace('places', description='Place operations')

# --- NESTED DATA MODELS (No change needed) ---

user_model = places_ns.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

amenity_model = places_ns.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

# --- INPUT MODEL ---

place_input_model = places_ns.model('PlaceInput', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

place_update_model = places_ns.model('PlaceUpdate', {
    'title': fields.String(required=False, description='Title of the place'),
    'description': fields.String(required=False, description='Description of the place'),
    'price': fields.Float(required=False, description='Price per night'),
    'latitude': fields.Float(required=False, description='Latitude coordinate'),
    'longitude': fields.Float(required=False, description='Longitude coordinate'),
    'owner_id': fields.String(required=False, description='ID of the owner user'), 
    'amenities': fields.List(fields.String, required=False, description='List of amenity IDs')
})

# --- RESPONSE MODEL ---

place_response_model = places_ns.model('PlaceResponse', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner': fields.Nested(user_model, description='Owner details'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of place amenities'),
    'created_at': fields.String(description='Creation date'),
    'updated_at': fields.String(description='Last update date')
})

# Error model
error_model = places_ns.model('Error', {
    'message': fields.String(description='Error message'),
})

# --- Custom Decorator for Admin Check (Imported or Defined Here) ---
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


# ----------------------------------------------------
# 1. Resource for the collection : /places (GET all, POST)
# ----------------------------------------------------
@places_ns.route('/')
class PlaceList(Resource):
    @places_ns.doc('create_place', security='jwt')
    @places_ns.expect(place_input_model, validate=True)
    @places_ns.marshal_with(place_response_model, code=201)
    @places_ns.response(201, 'Place successfully created')
    @places_ns.response(400, 'Invalid input data (validation error)', error_model)
    @places_ns.response(404, 'Owner or Amenity not found', error_model)
    @places_ns.response(409, 'Place already exists', error_model)
    @jwt_required()
    def post(self):
        """Register a new place (Requires Authentication)"""
        user_id = get_jwt_identity()
        place_data = places_ns.payload
        
        # Security check: Ensure the owner_id provided matches the authenticated user's ID
        if place_data.get('owner_id') != user_id:
             places_ns.abort(403, message="Unauthorized action: The 'owner_id' must match the authenticated user.")

        try:
            new_place_dict = facade.create_place(place_data)
            return new_place_dict, 201

        except LookupError as e:
            places_ns.abort(404, message='place not found')
        except (TypeError, ValueError) as e:
            places_ns.abort(400, message=str(e))
        except Exception as e:
            if "already exists" in str(e).lower():
                places_ns.abort(409, message='place already exists')
            places_ns.abort(400, message=str(e))


    @places_ns.doc('list_places')
    @places_ns.marshal_list_with(place_response_model)
    @places_ns.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places (Public)"""
        places_list = facade.get_all_places()
        return places_list, 200

# ----------------------------------------------------
# 2. Resource for a single item : /places/<string:place_id> (GET one, PUT)
# ----------------------------------------------------
@places_ns.route('/<string:place_id>')
@places_ns.param('place_id', 'The place unique identifier')
class PlaceResource(Resource):
    
    @places_ns.doc('get_place')
    @places_ns.marshal_with(place_response_model)
    @places_ns.response(200, 'Place details retrieved successfully')
    @places_ns.response(404, 'Place not found', error_model)
    def get(self, place_id):
        """Get place details by ID (Public)"""
        place_dict = facade.get_place(place_id)
        
        if not place_dict:
            places_ns.abort(404, message=f"Place with ID '{place_id}' not found")
        
        return place_dict, 200

    @places_ns.doc('update_place', security='jwt')
    @places_ns.expect(place_update_model, validate=True)
    @places_ns.marshal_with(place_response_model)
    @places_ns.response(200, 'Place updated successfully')
    @places_ns.response(404, 'Place not found or related entity not found', error_model)
    @places_ns.response(400, 'Invalid input data', error_model)
    @places_ns.response(403, 'Unauthorized action', error_model)
    @jwt_required()
    def put(self, place_id):
        """Update a place's information (Owner Only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        place_data = places_ns.payload
        
        # 1. Retrieve current place data (must be a dict or similar structure)
        place = facade.get_place(place_id) 
        
        if not place:
            places_ns.abort(404, message=f"Place with ID '{place_id}' not found")
            
        # 2. Authorization Check (Owner ID from the fetched place vs. current user ID)
        place_owner_id = place.owner_id
        
        # Authorization logic: Only the owner OR an admin can update
        is_admin = claims.get("is_admin", False)
        
        if place_owner_id != current_user_id and is_admin is not True:
            places_ns.abort(403, message="Unauthorized action: You can only update your own places.")

        # Optional: Prevent changing owner_id via PUT payload unless user is admin
        if 'owner_id' in place_data and place_data['owner_id'] != place_owner_id and is_admin is not True:
             places_ns.abort(403, message="Unauthorized action: Only an admin can change the 'owner_id'.")


        # 3. Proceed with update
        try:
            # Assuming update_place returns the updated dictionary (or object that can be converted)
            updated_place = facade.update_place(place_id, place_data)
            
            # Note: Assuming facade.update_place() doesn't return None if successful
            # The 404 is handled above, so this check might be redundant if the facade is strict.
            if not updated_place:
                 places_ns.abort(404, message=f"Place with ID '{place_id}' not found after update") 
            
            # Assuming update_place returns an object with .to_dict() or the facade is adjusted 
            # to return a dict consistent with get_place(). Let's return the dict directly:
          
            return updated_place, 200 
            
        except LookupError as e:
            places_ns.abort(404, message=str(e))
        except (TypeError, ValueError) as e:
            places_ns.abort(400, message=str(e))



    @places_ns.doc('delete_place', security='jwt')
    @places_ns.response(204, 'Place successfully deleted')
    @places_ns.response(401, 'Unauthorized', error_model)
    @places_ns.response(403, 'Forbidden: Owner or Admin required', error_model)
    @places_ns.response(404, 'Place not found', error_model)
    @jwt_required()
    def delete(self, place_id):
        """Delete a place by ID (owner and admin only)"""
        user_id = get_jwt_identity()
        # Admin check
        claims = get_jwt()
        if claims.get("is_admin", False) is not True:
            places_ns.abort(403, message="Access forbidden: Admin privilege required.")
        
        # Proceed with deletion
        is_deleted = facade.delete_place(place_id)
        
        if not is_deleted:
            places_ns.abort(404, message=f"Place with ID '{place_id}' not found")

        return 'Place successfully deleted', 204