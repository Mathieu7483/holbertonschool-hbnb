from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String(),
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True)
})


partial_place_model = api.model('PartialPlace', {
    'title': fields.String(),
    'description': fields.String(),
    'price': fields.Float(),
    'latitude': fields.Float(),
    'longitude': fields.Float(),
    'owner_id': fields.String()
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    def post(self):
        data = api.payload
        owner = facade.get_user(data['owner_id'])
        if not owner:
            return {'error': 'Invalid owner or data'}, 400
        place = facade.create_place(data)
        return place.to_dict(), 201


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
