from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta
from app.services import facade

auth_ns = Namespace('auth', description='Authentication operations')

# Login input model
login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# Token response model
token_response_model = auth_ns.model('TokenResponse', {
    'access_token': fields.String(description='JWT access token')
})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.doc('user_login')
    @auth_ns.expect(login_model, validate=True)
    @auth_ns.marshal_with(token_response_model, code=200)
    @auth_ns.response(200, 'Login successful')
    @auth_ns.response(401, 'Invalid credentials')
    @auth_ns.response(400, 'Bad request')
    def post(self):
        """Authenticate user and return JWT token"""
        credentials = auth_ns.payload
        
        # Validate input
        if not credentials.get('email') or not credentials.get('password'):
            auth_ns.abort(400, message='Email and password are required')

        # Retrieve user by email
        user = facade.get_user_by_email(credentials['email'])

        # Verify user exists and password is correct
        if not user or not user.verify_password(credentials['password']):
            auth_ns.abort(401, message='Invalid credentials')

        # Create JWT token with user ID and admin status
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin},
            expires_delta=timedelta(hours=3)
        )

        return {'access_token': access_token}, 200

@auth_ns.route('/protected')
class ProtectedResource(Resource):
    @auth_ns.doc('protected_endpoint', security='jwt')
    @auth_ns.response(200, 'Access granted')
    @auth_ns.response(401, 'Unauthorized')
    @jwt_required()
    def get(self):
        """A protected endpoint requiring valid JWT token"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        
        return {
            'message': f'Hello, user {current_user_id}',
            'is_admin': claims.get('is_admin', False)
        }, 200