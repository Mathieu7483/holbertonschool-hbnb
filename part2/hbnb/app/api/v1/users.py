from flask import request
from flask_restx import Resource, Namespace, fields
from app import HBnB_FACADE
facade = HBnB_FACADE # Ensure the import is correct

# Initialization: Using the requested naming convention 'user_ns'
user_ns = Namespace('users', description='User related operations (Excluding Delete)')

# Definition of the data model (for OpenAPI/Swagger documentation)
user_model = user_ns.model('User', {
    'first_name': fields.String(required=True, description='The user first name'),
    'last_name': fields.String(description='The user last name'),
    'email': fields.String(required=True, description='The user email address'),
    'is_admin': fields.Boolean(description='Whether the user is an admin'),
})

# Definition of the response model (with IDs and dates)
user_response_model = user_ns.inherit('UserResponse', user_model, {
    'id': fields.String(readOnly=True, description='The unique identifier'),
    'created_at': fields.String(readOnly=True, description='Timestamp of creation'),
    'updated_at': fields.String(readOnly=True, description='Timestamp of last update'),
})

# ----------------------------------------------------
# 1. Resource for the collection : /users (GET all, POST)
# ----------------------------------------------------
@user_ns.route('/')
class UserListResource(Resource):
    @user_ns.doc('list_users')
    @user_ns.marshal_list_with(user_response_model)
    def get(self):
        """List all users"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200

    @user_ns.doc('create_user')
    @user_ns.expect(user_model)
    @user_ns.marshal_with(user_response_model, code=201)
    def post(self):
        """Create a new User"""
        try:
            user_data = request.json
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except Exception as e:
            # Handle validation errors or missing data from the Facade/Model
            user_ns.abort(400, message=str(e))


# ----------------------------------------------------
# 2. Resource for a single item : /users/<user_id> (GET one, PUT)
# ----------------------------------------------------
@user_ns.route('/<string:user_id>')
@user_ns.response(404, 'User not found')
class UserResource(Resource):
    @user_ns.doc('get_user')
    @user_ns.marshal_with(user_response_model)
    def get(self, user_id):
        """Retrieve a User by ID"""
        user = facade.get_user(user_id)
        if user is None:
            user_ns.abort(404, message=f"User with ID {user_id} not found")
        return user.to_dict(), 200

    @user_ns.doc('update_user')
    @user_ns.expect(user_model)
    @user_ns.marshal_with(user_response_model)
    def put(self, user_id):
        """Update an existing User"""
        try:
            user_data = request.json
            updated_user = facade.update_user(user_id, user_data)
            if updated_user is None:
                 user_ns.abort(404, message=f"User with ID {user_id} not found")
            return updated_user.to_dict(), 200
        except Exception as e:
            # Handle validation errors from the Facade/Model during update
            user_ns.abort(400, message=str(e))
