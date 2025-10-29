from flask import request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app import HBnB_FACADE

facade = HBnB_FACADE

# Initialization with better description
users_ns = Namespace('users', description='User management operations')


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


# Definition of the input model (for POST)
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

# New model for updating a user (PUT) - only first_name and last_name allowed
user_update_model = users_ns.model('UserUpdate', {
    'first_name': fields.String(
        required=False, 
        description='The user first name',
        example='John'
    ),
    'last_name': fields.String(
        required=False,
        description='The user last name',
        example='Doe'
    ),
})

# Model for updating user as admin
user_admin_update_model = users_ns.model('UserAdminUpdate', {
    'first_name': fields.String(
        required=False, 
        description='The user first name',
        example='John'
    ),
    'last_name': fields.String(
        required=False,
        description='The user last name',
        example='Doe'
    ),
    'email': fields.String(
        required=False,
        description='The user email address',
        example='john.doe@example.com'
    ),
    'password': fields.String(
        required=False,
        description='The user password',
        example='StrongP@ssw0rd'
    )
})
    
# Model for basic OUTPUT (base fields without password)
user_base_output_model = users_ns.model('UserBaseOutput', {
    'first_name': fields.String(description='The user first name'),
    'last_name': fields.String(description='The user last name'),
    'email': fields.String(description='The user email address'),
    'is_admin': fields.Boolean(description='Whether the user is an admin'),
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
    @users_ns.doc('list_users', security='jwt')
    @admin_required()
    @users_ns.marshal_list_with(user_response_model)
    @users_ns.response(200, 'Success')
    @users_ns.response(401, 'Unauthorized', error_model)
    @users_ns.response(403, 'Forbidden: Admin required', error_model)
    def get(self):
        """List all users (ADMIN only)"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200

    @users_ns.doc('create_user')
    @users_ns.expect(user_model, validate=True)
    @users_ns.marshal_with(user_response_model, code=201)
    @users_ns.response(201, 'User created successfully')
    @users_ns.response(400, 'Invalid input data', error_model)
    @users_ns.response(409, 'Email already exists', error_model)
    def post(self):
        """Create a new User"""
        try:
            user_data = request.get_json()
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except ValueError as e:
            users_ns.abort(400, message=str(e))
        except Exception as e:
            if "already exists" in str(e).lower():
                users_ns.abort(409, message=str(e))
            users_ns.abort(400, message=str(e))


# ----------------------------------------------------
# 2. Resource for a single item : /users/<user_id> (GET, PUT, DELETE)
# ----------------------------------------------------
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
        """Retrieve a User by ID"""
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        
        if current_user != user_id and is_admin is not True:
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
    @users_ns.response(400, 'Invalid input', error_model)
    @users_ns.response(404, 'User not found', error_model)
    @users_ns.response(401, 'Unauthorized', error_model)
    @users_ns.response(403, 'Forbidden', error_model)
    def put(self, user_id):
        """Update user's first_name and last_name only"""
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        
        # Authorization: only the user themselves or an admin
        if current_user != user_id and not is_admin:
            users_ns.abort(403, message="Access forbidden: You can only modify your own profile.")

        try:
            user_data = request.get_json()
        except Exception:
            users_ns.abort(400, message="Invalid JSON data")
        
        if not user_data:
            users_ns.abort(400, message="No data provided")
        
        try:
            updated_user = facade.update_user(user_id, user_data)
            if updated_user is None:
                users_ns.abort(404, message=f"User with ID {user_id} not found")
            
            return updated_user.to_dict(), 200
            
        except ValueError as e:
            users_ns.abort(400, message=str(e))
        except Exception as e:
            if "already exists" in str(e).lower():
                users_ns.abort(409, message=str(e))
            users_ns.abort(400, message=str(e))

    @users_ns.doc('delete_user', security='jwt')
    @jwt_required()
    @users_ns.response(204, 'User successfully deleted')
    @users_ns.response(404, 'User not found', error_model)
    @users_ns.response(403, 'Forbidden: Admin privilege required', error_model)
    def delete(self, user_id):
        """Delete a User by ID (ADMIN ONLY)"""
        claims = get_jwt()
        
        # Authorization Check: Must be Admin
        if claims.get("is_admin", False) is not True:
            users_ns.abort(403, message="Access forbidden: Admin privilege required.")
            
        # Prevent Admin from deleting their own account
        current_user_id = get_jwt_identity()
        if user_id == current_user_id:
            users_ns.abort(403, message="Cannot delete your own admin account.")

        # Proceed with deletion
        is_deleted = facade.delete_user(user_id)
        
        if not is_deleted:
            users_ns.abort(404, message=f"User with ID {user_id} not found")

        return '', 204


# ----------------------------------------------------
# 3. Resource for admin updates : /users/<user_id>/admin (PUT)
# ----------------------------------------------------
@users_ns.route('/<string:user_id>/admin')
@users_ns.param('user_id', 'The user unique identifier')
class UserAdminResource(Resource):
    
    @users_ns.doc('update_user_by_admin', security='jwt')
    @admin_required()
    @users_ns.expect(user_admin_update_model, validate=True)
    @users_ns.marshal_with(user_response_model)
    @users_ns.response(200, 'User updated successfully')
    @users_ns.response(404, 'User not found', error_model)
    @users_ns.response(403, 'Forbidden: Admin required', error_model)
    @users_ns.response(400, 'Invalid input', error_model)
    @users_ns.response(409, 'Email already exists', error_model)
    def put(self, user_id):
        """Update any user field (Admin only) - including email and password"""
        
        try:
            user_data = request.get_json()
        except Exception:
            users_ns.abort(400, message="Invalid JSON data")
        
        if not user_data:
            users_ns.abort(400, message="No data provided")
        
        try:
            updated_user = facade.update_user(user_id, user_data)
            if updated_user is None:
                users_ns.abort(404, message=f"User with ID {user_id} not found")
            
            return updated_user.to_dict(), 200
            
        except ValueError as e:
            users_ns.abort(400, message=str(e))
        except Exception as e:
            if "already exists" in str(e).lower():
                users_ns.abort(409, message=str(e))
            users_ns.abort(400, message=str(e))