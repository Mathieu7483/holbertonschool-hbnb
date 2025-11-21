from flask import request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import HBnB_FACADE

facade = HBnB_FACADE
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
    'id': fields.String(),
    'first_name': fields.String(),
    'last_name': fields.String(),
    'email': fields.String()
})

amenity_model = places_ns.model('PlaceAmenity', {
    'id': fields.String(),
    'name': fields.String()
})

place_input_model = places_ns.model('PlaceInput', {
    'title': fields.String(required=True),
    'description': fields.String(),
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'amenities': fields.List(fields.String, required=False)
})

place_update_model = places_ns.model('PlaceUpdate', {
    'title': fields.String(required=False),
    'description': fields.String(required=False),
    'price': fields.Float(required=False),
    'latitude': fields.Float(required=False),
    'longitude': fields.Float(required=False),
    'amenities': fields.List(fields.String, required=False)
})

place_response_model = places_ns.model('PlaceResponse', {
    'id': fields.String(),
    'title': fields.String(),
    'description': fields.String(),
    'price': fields.Float(),
    'latitude': fields.Float(),
    'longitude': fields.Float(),
    'owner': fields.Nested(user_model),
    'amenities': fields.List(fields.Nested(amenity_model)),
    'created_at': fields.String(),
    'updated_at': fields.String()
})

error_model = places_ns.model('Error', {
    'message': fields.String(),
})

@places_ns.route('/')
class PlaceList(Resource):
    
    @places_ns.doc('list_places')
    @places_ns.marshal_list_with(place_response_model)
    def get(self):
        places = facade.get_all_places()
        return [place for place in places], 200

    @jwt_required()
    @places_ns.doc('create_place')
    @places_ns.expect(place_input_model)
    @places_ns.marshal_with(place_response_model, code=201)
    def post(self):
        current_user_id = get_jwt_identity()
        place_data = places_ns.payload
        place_data['owner_id'] = current_user_id

        try:
            new_place = facade.create_place(place_data)
            return new_place, 201
        
        except ValueError as e:
            places_ns.abort(400, message=str(e))
        except Exception as e:
            places_ns.abort(500, message="An unexpected error occurred during place creation.")


@places_ns.route('/<string:place_id>')
class PlaceResource(Resource):
    @places_ns.doc('get_place')
    @places_ns.marshal_with(place_response_model)
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            places_ns.abort(404, f"Place with ID {place_id} not found.")
        return place, 200


    @jwt_required()
    @places_ns.doc('update_place')
    @places_ns.expect(place_update_model)
    @places_ns.marshal_with(place_response_model)
    def put(self, place_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        place_data = places_ns.payload
        
        place_data.pop('owner_id', None)
        
        try:
            place = facade.get_place(place_id)
            
            if not place:
                places_ns.abort(404, f"Place with ID {place_id} not found.")

            if place.owner_id != current_user_id and not is_admin:
                places_ns.abort(403, "You do not have permission to update this place.")

            updated_place = facade.update_place(place_id, place_data)

            return updated_place, 200
            
        except ValueError as e:
            places_ns.abort(400, message=str(e))
        except Exception as e:
            print(f"Error: {e}")
            places_ns.abort(500, message="An unexpected error occurred during place update.")

    @jwt_required()
    @places_ns.doc('delete_place')
    def delete(self, place_id):
        current_user_id = get_jwt_identity()
        
        place_to_delete = facade.get_place(place_id)
        if not place_to_delete:
            places_ns.abort(404, f"Place with ID {place_id} not found.")

        if place_to_delete.owner_id != current_user_id:
            places_ns.abort(403, "You do not have permission to delete this place.")

        facade.delete_place(place_id)
        return '', 204