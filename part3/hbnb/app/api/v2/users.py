from flask import request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app import HBnB_FACADE

facade = HBnB_FACADE
users_ns = Namespace('users', description='User management operations')

# Decorator admin_required
def admin_required():
    """Custom decorator to ensure the authenticated user has Admin privilege."""
    def wrapper(fn): 
        @jwt_required()
        def decorated_view(*args, **kwargs):
            claims = get_jwt()
            if claims.get("is_admin", False) is not True:
                users_ns.abort(403, message="Access forbidden: Admin privilege required.")
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

# Input model for creating users
user_model = users_ns.model('User', {
    'first_name': fields.String(required=True, description='First name', example='John'),
    'last_name': fields.String(required=True, description='Last name', example='Doe'),
    'email': fields.String(required=True, description='Email address', example='john.doe@example.com'),
    'password': fields.String(required=True, description='Password', example='StrongP@ssw0rd'),
    'is_admin': fields.Boolean(description='Admin status', default=False)
})

# Model for updating user (regular users)
user_update_model = users_ns.model('UserUpdate', {
    'first_name': fields.String(required=False, description='First name', example='John'),
    'last_name': fields.String(required=False, description='Last name', example='Doe')
})

# Model for admin updates
user_admin_update_model = users_ns.model('UserAdminUpdate', {
    'first_name': fields.String(required=False, description='First name'),
    'last_name': fields.String(required=False, description='Last name'),
    'email': fields.String(required=False, description='Email address'),
    'password': fields.String(required=False, description='New password')
})

# Output model (excludes password)
user_response_model = users_ns.model('UserResponse', {
    'id': fields.String(readOnly=True, description='User ID'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email address'),
    'is_admin': fields.Boolean(description='Admin status'),
    'created_at': fields.String(readOnly=True, description='Creation timestamp'),
    'updated_at': fields.String(readOnly=True, description='Last update timestamp')
})

# Error model
error_model = users_ns.model('Error', {
    'message': fields.String(description='Error message'),
})

@users_ns.route('/')
class UserListResource(Resource):
    @users_ns.doc('list_users', security='jwt')
    @admin_required()
    @users_ns.marshal_list_with(user_response_model)
    @users_ns.response(200, 'Success')
    @users_ns.response(401, 'Unauthorized', error_model)
    @users_ns.response(403, 'Forbidden: Admin required', error_model)
    def get(self):
        """List all users (Admin only)"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200

    @users_ns.doc('create_user')
    @users_ns.expect(user_model, validate=True)
    @users_ns.marshal_with(user_response_model, code=201)
    @users_ns.response(201, 'User created successfully')
    @users_ns.response(400, 'Invalid input data', error_model)
    @users_ns.response(409, 'Email already exists', error_model)
    def post(self):
        """Create a new user (Public registration)"""
        try:
            user_data = request.json
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except ValueError as e:
            users_ns.abort(400, message=str(e))
        except Exception as e:
            if "already exists" in str(e).lower():
                users_ns.abort(409, message=str(e))
            users_ns.abort(400, message=str(e))

@users_ns.route('/<string:user_id>')
@users_ns.param('user_id', 'The user unique identifier')
class UserResource(Resource):
    @users_ns.doc('get_user', security='jwt')
    @jwt_required()
    @users_ns.marshal_with(user_response_model)
    @users_ns.response(200, 'Success')
    @users_ns.response(404, 'User not found', error_model)
    @users_ns.response(401, 'Unauthorized', error_model)
    @users_ns.response(403, 'Forbidden', error_model)
    def get(self, user_id):
        """Retrieve a user by ID (Own profile or Admin)"""
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        
        if current_user != user_id and not is_admin:
            users_ns.abort(403, message="Access forbidden: You can only view your own profile.")
            
        user = facade.get_user(user_id)
        if user is None:
            users_ns.abort(404, message=f"User with ID {user_id} not found")
        
        return user.to_dict(), 200

    @users_ns.doc('update_user', security='jwt')
    @jwt_required()
    @users_ns.expect(user_update_model, validate=True)
    @users_ns.marshal_with(user_response_model)
    @users_ns.response(200, 'User updated successfully')
    @users_ns.response(400, 'Invalid input data', error_model)
    @users_ns.response(404, 'User not found', error_model)
    @users_ns.response(401, 'Unauthorized', error_model)
    @users_ns.response(403, 'Forbidden', error_model)
    def put(self, user_id):
        """Update user profile (Own profile only)"""
        current_user_id = get_jwt_identity()
        
        if current_user_id != user_id:
            users_ns.abort(403, message="Access forbidden: You can only modify your own profile.")
            
        user_data = users_ns.payload

        # Prevent modification of protected fields
        if 'email' in user_data or 'password' in user_data or 'is_admin' in user_data:
            users_ns.abort(400, message="You can only modify first name and last name.")
        
        try:
            updated_user = facade.update_user(user_id, user_data)
            if updated_user is None:
                users_ns.abort(404, message=f"User with ID {user_id} not found")
            return updated_user.to_dict(), 200
        except ValueError as e:
            users_ns.abort(400, message=str(e))

    @users_ns.doc('delete_user', security='jwt')
    @jwt_required()
    @users_ns.response(204, 'User deleted successfully')
    @users_ns.response(404, 'User not found', error_model)
    @users_ns.response(403, 'Forbidden: Admin required', error_model)
    def delete(self, user_id):
        """Delete a user (Admin only)"""
        claims = get_jwt()
        
        # Authorization check
        if claims.get("is_admin", False) is not True:
            users_ns.abort(403, message="Access forbidden: Admin privilege required.")
            
        # Prevent admin from deleting themselves
        current_user_id = get_jwt_identity()
        if user_id == current_user_id:
            users_ns.abort(403, message="Cannot delete your own admin account.")

        is_deleted = facade.delete_user(user_id)
        
        if not is_deleted:
            users_ns.abort(404, message=f"User with ID {user_id} not found")

        return None, 204

@users_ns.route('/<string:user_id>/admin')
@users_ns.param('user_id', 'The user unique identifier')
class UserAdminResource(Resource):
    @users_ns.doc('update_user_by_admin', security='jwt')
    @users_ns.expect(user_admin_update_model, validate=True)
    @users_ns.marshal_with(user_response_model)
    @admin_required()
    @users_ns.response(200, 'User updated successfully')
    @users_ns.response(404, 'User not found', error_model)
    @users_ns.response(403, 'Forbidden: Admin required', error_model)
    @users_ns.response(400, 'Invalid input', error_model)
    @users_ns.response(409, 'Email already exists', error_model)
    def put(self, user_id):
        """Update user (Admin only - can modify all fields)"""
        user_data = users_ns.payload
        
        if not user_data:
            users_ns.abort(400, message="No data provided")
        
        try:
            updated_user = facade.update_user_by_admin(user_id, user_data)
            if updated_user is None:
                users_ns.abort(404, message=f"User with ID {user_id} not found")
            
            return updated_user.to_dict(), 200
            
        except ValueError as e:
            users_ns.abort(400, message=str(e))
        except Exception as e:
            if "already exists" in str(e).lower():
                users_ns.abort(409, message=str(e))
            users_ns.abort(400, message=str(e))