from flask_restx import Namespace, Resource, fields
from app import HBnB_FACADE
facade = HBnB_FACADE

places_ns = Namespace('places', description='Place operations')

# --- NESTED DATA MODELS (For API Response) ---

# Model for owner data (User)
user_model = places_ns.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Model for amenity data
amenity_model = places_ns.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

# --- INPUT MODEL (POST/PUT - Receives IDs) ---

# The input model receives the IDs for the owner and amenities
place_input_model = places_ns.model('PlaceInput', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

# --- RESPONSE MODEL (GET/POST/PUT - Returns Nested Objects) ---

# The response model uses nested objects (owner, amenities)
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


@places_ns.route('/')
class PlaceList(Resource):
    @places_ns.doc('create_place')
    @places_ns.expect(place_input_model, validate=True) # Use input model
    @places_ns.marshal_with(place_response_model, code=201) # Marshalling the response
    @places_ns.response(201, 'Place successfully created')
    @places_ns.response(400, 'Invalid input data (validation error)')
    @places_ns.response(404, 'Owner or Amenity not found')
    def post(self):
        """Register a new place"""
        place_data = places_ns.payload

        try:
            # The facade returns an already enriched dictionary
            new_place_dict = facade.create_place(place_data)
            return new_place_dict, 201

        except LookupError as e:
            # Handles 404 for related IDs (owner_id, amenities)
            places_ns.abort(404, message=str(e))
        except (TypeError, ValueError) as e:
            # Handles 400 if model validation fails
            places_ns.abort(400, message=str(e))


    @places_ns.doc('list_places')
    @places_ns.marshal_list_with(place_response_model) # Marshalling the list
    @places_ns.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        # The facade returns a list of enriched dictionaries
        places_list = facade.get_all_places()
        return places_list, 200

# -----------------------------

@places_ns.route('/<string:place_id>') # Use <string:place_id> for routing
class PlaceResource(Resource):
    @places_ns.doc('get_place')
    @places_ns.marshal_with(place_response_model)
    @places_ns.response(200, 'Place details retrieved successfully')
    @places_ns.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place_dict = facade.get_place(place_id)
        
        if not place_dict:
            places_ns.abort(404, message=f"Place with ID '{place_id}' not found")
        
        return place_dict, 200

    @places_ns.doc('update_place')
    @places_ns.expect(place_input_model, validate=True) # Use input model
    @places_ns.marshal_with(place_response_model)
    @places_ns.response(200, 'Place updated successfully')
    @places_ns.response(404, 'Place not found or related entity not found')
    @places_ns.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = places_ns.payload
        
        try:
            updated_place_dict = facade.update_place(place_id, place_data)

            if not updated_place_dict:
                places_ns.abort(404, message=f"Place with ID '{place_id}' not found")
            
            return updated_place_dict, 200
            
        except LookupError as e:
            places_ns.abort(404, message=str(e))
        except (TypeError, ValueError) as e:
            places_ns.abort(400, message=str(e))
