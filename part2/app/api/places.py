from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String(),
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True)
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    def post(self):
        data = api.payload
        place = facade.create_place(data)
        if not place:
            return {'error': 'Invalid owner or data'}, 400
        return place.to_dict(), 201

    def get(self):
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

@api.route('/<string:place_id>')
class PlaceDetail(Resource):
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200

    @api.expect(place_model, validate=True)
    def put(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        updated = facade.update_place(place_id, api.payload)
        return updated.to_dict(), 200
