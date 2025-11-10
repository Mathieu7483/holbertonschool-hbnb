from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import HBnB_FACADE

facade = HBnB_FACADE
reviews_ns = Namespace('reviews', description='Review operations')

# Nested models
user_nested_model = reviews_ns.model('ReviewUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name'),
    'email': fields.String(description='Email')
})

place_nested_model = reviews_ns.model('ReviewPlace', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Place title')
})

# Input model
review_input_model = reviews_ns.model('ReviewInput', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'user_id': fields.String(required=True, description='User ID'),
    'place_id': fields.String(required=True, description='Place ID')
})

# Response model
review_response_model = reviews_ns.model('ReviewResponse', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating (1-5)'),
    'user': fields.Nested(user_nested_model, description='User details'),
    'place': fields.Nested(place_nested_model, description='Place details'),
    'created_at': fields.String(description='Creation date'),
    'updated_at': fields.String(description='Last update date')
})

# Update model
review_update_model = reviews_ns.model('ReviewUpdate', {
    'text': fields.String(required=False, description='Review content'),
    'rating': fields.Integer(required=False, description='Rating (1-5)'),
})

@reviews_ns.route('/')
class ReviewList(Resource):
    @reviews_ns.doc('create_review', security='jwt')
    @reviews_ns.expect(review_input_model, validate=True)
    @reviews_ns.marshal_with(review_response_model, code=201)
    @reviews_ns.response(201, 'Review successfully created')
    @reviews_ns.response(400, 'Invalid input data')
    @reviews_ns.response(403, 'Forbidden (Owner cannot review own place)')
    @reviews_ns.response(409, 'Conflict (User already reviewed this place)')
    @reviews_ns.response(404, 'User or Place not found')
    @jwt_required()
    def post(self):
        """Create a new review"""
        user_id = get_jwt_identity()
        review_data = reviews_ns.payload

        # Security: ensure user_id matches authenticated user
        if review_data.get('user_id') != user_id:
            reviews_ns.abort(403, message="Unauthorized: Review must be created by authenticated user.")
        
        place_id = review_data.get('place_id')

        # Verify user and place exist
        user = facade.get_user(user_id)
        place = facade.get_place(place_id)

        if not user:
            reviews_ns.abort(404, message=f"User with ID '{user_id}' not found")
        if not place:
            reviews_ns.abort(404, message=f"Place with ID '{place_id}' not found")

        # Check if owner is trying to review their own place
        if place.owner_id == user_id:
            reviews_ns.abort(403, message="Forbidden: You cannot review your own place.")
        
        # Check for duplicate review
        if facade.user_has_reviewed_place(user_id, place_id):
            reviews_ns.abort(409, message="Conflict: You have already reviewed this place.")
        
        try:
            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201
        except ValueError as e:
            reviews_ns.abort(400, message=str(e))
        except Exception as e:
            reviews_ns.abort(500, message=f"Internal error: {str(e)}")

    @reviews_ns.doc('list_reviews')
    @reviews_ns.marshal_list_with(review_response_model)
    @reviews_ns.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200

@reviews_ns.route('/<string:review_id>')
class ReviewResource(Resource):
    @reviews_ns.doc('get_review')
    @reviews_ns.marshal_with(review_response_model)
    @reviews_ns.response(200, 'Review details retrieved successfully')
    @reviews_ns.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            reviews_ns.abort(404, message=f"Review with ID '{review_id}' not found")
        
        return review.to_dict(), 200

    @reviews_ns.doc('update_review', security='jwt')
    @reviews_ns.expect(review_update_model, validate=True)
    @reviews_ns.marshal_with(review_response_model)
    @reviews_ns.response(200, 'Review updated successfully')
    @reviews_ns.response(404, 'Review not found')
    @reviews_ns.response(400, 'Invalid input data')
    @reviews_ns.response(403, 'Unauthorized')
    @jwt_required()
    def put(self, review_id):
        """Update a review (Author or Admin only)"""
        user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        
        review_data = reviews_ns.payload

        review = facade.get_review(review_id)
        if not review:
            reviews_ns.abort(404, message=f"Review with ID '{review_id}' not found")

        # Authorization: author or admin
        if review.user_id != user_id and not is_admin:
            reviews_ns.abort(403, message="Unauthorized: You can only update your own reviews.")

        try:
            updated_review = facade.update_review(review_id, review_data)
            
            if not updated_review:
                reviews_ns.abort(404, message=f"Review with ID '{review_id}' not found")
                
            return updated_review.to_dict(), 200
            
        except ValueError as e:
            reviews_ns.abort(400, message=str(e))

    @reviews_ns.doc('delete_review', security='jwt')
    @reviews_ns.response(204, 'Review deleted successfully')
    @reviews_ns.response(404, 'Review not found')
    @reviews_ns.response(403, 'Unauthorized')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review (Author or Admin only)"""
        user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        
        review = facade.get_review(review_id)
        
        if not review:
            reviews_ns.abort(404, message=f"Review with ID '{review_id}' not found")
        
        # Authorization: author or admin
        if review.user_id != user_id and not is_admin:
            reviews_ns.abort(403, message="Unauthorized: You can only delete your own reviews.")
        
        is_deleted = facade.delete_review(review_id)
        
        if not is_deleted:
            reviews_ns.abort(404, message=f"Review with ID '{review_id}' not found")

        return None, 204

@reviews_ns.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    @reviews_ns.doc('list_place_reviews')
    @reviews_ns.marshal_list_with(review_response_model)
    @reviews_ns.response(200, 'List of reviews for the place retrieved successfully')
    @reviews_ns.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            reviews_ns.abort(404, message=f"Place with ID '{place_id}' not found")
        
        reviews = facade.get_reviews_by_place(place_id)
        return [review.to_dict() for review in reviews], 200