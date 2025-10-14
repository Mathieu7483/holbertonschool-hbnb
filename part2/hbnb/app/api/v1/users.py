from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

# Model for user response (without password and internal fields)
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'is_admin': fields.Boolean(description='Whether the user is an admin'),
    'created_at': fields.String(description='Creation date'),
    'updated_at': fields.String(description='Last update date')
})

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_response_model)
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve the list of all users"""
        users = facade.get_all_users()
        return users, 200

    @api.doc('create_user')
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Check if email already exists
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            # Create new user
            new_user = facade.create_user(user_data)
            if new_user is None:
                return {'error': 'Failed to create user'}, 400
            
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'is_admin': new_user.is_admin,
                'created_at': new_user.created_at,
                'updated_at': new_user.updated_at
            }, 201
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'error': f'Error: {str(e)}'}, 400

@api.route('/<user_id>')
class UserResource(Resource):
    @api.doc('get_user')
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        }, 200

    # ===== METHODE PUT - MISE À JOUR D'UN UTILISATEUR =====
    @api.doc('update_user')
    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user information"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        user_data = api.payload

        # Check if new email is already in use by another user
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400

        try:
            # Update user using the model's update method
            updated_user = user.update(user_data)
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email,
                'is_admin': updated_user.is_admin,
                'created_at': updated_user.created_at,
                'updated_at': updated_user.updated_at
            }, 200
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400