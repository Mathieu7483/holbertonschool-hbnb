from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

user = {}

user_model = api.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True)
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    def post(self):
        data = api.payload
        if facade.get_user_by_email(data['email']):
            return {'error': 'Email already registered'}, 400
        user = facade.create_user(data)
        return user.to_dict(), 201

    def get(self):
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200

@api.route('/<string:user_id>')
class UserDetail(Resource):
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_model, validate=True)
    def put(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        updated = facade.update_user(user_id, api.payload)
        return updated.to_dict(), 200
