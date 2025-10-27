from flask import request
from flask_restx import Resource, Namespace, fields
from app import HBnB_FACADE

facade = HBnB_FACADE

# Initialization with better description
users_ns = Namespace('users', description='User management operations')

# Definition of the input model (for POST/PUT)
user_model = users_ns.model('User', {
    'first_name': fields.String(
        required=True, 
        description='The user first name',
        example='John'
    ),
    'last_name': fields.String(
        description='The user last name',
        example='Doe'
    ),
    'email': fields.String(
        required=True, 
        description='The user email address',
        example='john.doe@example.com'
    ),
    'is_admin': fields.Boolean(
        description='Whether the user is an admin',
        default=False
    ),
    'password': fields.String(
        required=True,
        description='The user password',
        example='StrongP@ssw0rd'
    ),
})

# Model for basic OUTPUT (base fields without password)
user_base_output_model = users_ns.model('UserBaseOutput', {
    'first_name': fields.String(description='The user first name'),
    'last_name': fields.String(description='The user last name'),
    'email': fields.String(description='The user email address'),
    'is_admin': fields.Boolean(description='Whether the user is an admin'),
    # Password is explicitly omitted here 🔒
})

# Definition of the response model (with IDs and dates)
user_response_model = users_ns.inherit('UserResponse', user_base_output_model, {
    'id': fields.String(
        readOnly=True, 
        description='The unique identifier',
        example='3fa85f64-5717-4562-b3fc-2c963f66afa6'
    ),
    'created_at': fields.String(
        readOnly=True, 
        description='Timestamp of creation',
        example='2024-01-15T10:30:00'
    ),
    'updated_at': fields.String(
        readOnly=True, 
        description='Timestamp of last update',
        example='2024-01-15T10:30:00'
    ),
})

# Error response model for better documentation
error_model = users_ns.model('Error', {
    'message': fields.String(description='Error message'),
})


# ----------------------------------------------------
# 1. Resource for the collection : /users (GET all, POST)
# ----------------------------------------------------
@users_ns.route('/')
class UserListResource(Resource):
    @users_ns.doc('list_users')
    @users_ns.marshal_list_with(user_response_model)
    @users_ns.response(200, 'Success')
    def get(self):
        """List all users"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200

    @users_ns.doc('create_user')
    @users_ns.expect(user_model, validate=True)
    @users_ns.marshal_with(user_response_model, code=201)
    @users_ns.response(201, 'User created successfully')
    @users_ns.response(400, 'Invalid input data', error_model)
    @users_ns.response(409, 'Email already exists')
    def post(self):
        """Create a new User"""
        try:
            user_data = request.json
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except ValueError as e:
            # Handle validation errors (email format, missing fields, etc.)
            users_ns.abort(400, message=str(e))
        except Exception as e:
            # Handle other errors (email already exists, etc.)
            if "already exists" in str(e).lower():
                users_ns.abort(409, message=str(e))
            users_ns.abort(400, message=str(e))


# ----------------------------------------------------
# 2. Resource for a single item : /users/<user_id> (GET one, PUT)
# ----------------------------------------------------
@users_ns.route('/<string:user_id>')
@users_ns.param('user_id', 'The user unique identifier')
class UserResource(Resource):
    @users_ns.doc('get_user')
    @users_ns.marshal_with(user_response_model)
    @users_ns.response(200, 'Success')
    @users_ns.response(404, 'User not found', error_model)
    def get(self, user_id):
        """Retrieve a User by ID"""
        user = facade.get_user(user_id)
        if user is None:
            users_ns.abort(404, message=f"User with ID {user_id} not found")
        return user.to_dict(), 200

    @users_ns.doc('update_user')
    @users_ns.expect(user_model, validate=True)
    @users_ns.marshal_with(user_response_model)
    @users_ns.response(200, 'User updated successfully')
    @users_ns.response(400, 'Invalid input data', error_model)
    @users_ns.response(404, 'User not found', error_model)
    @users_ns.response(409, 'Email already exists')
    @users_ns.response(401, 'Unauthorized', error_model)
    def put(self, user_id):
        """Update an existing User"""
        try:
            user_data = request.json
            updated_user = facade.update_user(user_id, user_data)
            if updated_user is None:
                users_ns.abort(404, message=f"User with ID {user_id} not found")
            return updated_user.to_dict(), 200
        except ValueError as e:
            # Handle validation errors
            users_ns.abort(400, message=str(e))
        except Exception as e:
            # Handle other errors
            if "already exists" in str(e).lower():
                users_ns.abort(409, message=str(e))
            users_ns.abort(400, message=str(e))
        except PermissionError as e:
            if "unauthorized" in str(e).lower():
                users_ns.abort(401, message=str(e))
