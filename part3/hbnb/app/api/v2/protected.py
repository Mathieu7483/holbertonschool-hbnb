from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

protected_ns = Namespace('protected', description='Protected operations')


@protected_ns.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
         """A protected endpoint that requires a valid JWT token"""
         print("jwt------")
         print(get_jwt_identity())
         current_user = get_jwt_identity() # Retrieve the user's identity from the token
         claims = get_jwt()  # Retrieve additional claims if needed
         return {
              'message': f'Hello, user {current_user}',
              "is-admin": claims["is_admin"]
         }, 200