from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import HBnB_FACADE


# Initialize the Facade
facade = HBnB_FACADE

# Namespace definition for the 'reviews' API section
reviews_ns = Namespace('reviews', description='Review operations')

# --- NESTED MODELS (For the response) ---

# Model for user data (simplified for review response)
user_nested_model = reviews_ns.model('ReviewUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Model for place data (simplified for review response)
place_nested_model = reviews_ns.model('ReviewPlace', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place')
})

# Define the review input model (used for POST - receives IDs, all fields required)
review_input_model = reviews_ns.model('ReviewInput', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user who wrote the review'), 
    'place_id': fields.String(required=True, description='ID of the place being reviewed')
})

# Model for the complete response (used in GET/POST/PUT - returns nested objects)
review_response_model = reviews_ns.model('ReviewResponse', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    # Nested fields automatically use the marshal_with logic for nested models
    'user': fields.Nested(user_nested_model, description='User details'),
    'place': fields.Nested(place_nested_model, description='Place details'),
    'created_at': fields.String(description='Creation date'),
    'updated_at': fields.String(description='Last update date')
})

# Model for the update (Used in PUT - fields are optional for partial updates)
review_update_model = reviews_ns.model('ReviewUpdate', {
    'text': fields.String(required=False, description='The review content'),
    'rating': fields.Integer(required=False, description='Rating (1-5)'),
})

# -------------------------------------------------------------
# Resource: /reviews
# -------------------------------------------------------------

@reviews_ns.route('/')
class ReviewList(Resource):
    
    @reviews_ns.doc('create_review', security='jwt')
    @reviews_ns.expect(review_input_model, validate=True)
    @reviews_ns.marshal_with(review_response_model, code=201)
    @reviews_ns.response(201, 'Review successfully created')
    @reviews_ns.response(400, 'Invalid input data')
    @reviews_ns.response(403, 'Forbidden action (Owner review or Unauthorized user)')
    @reviews_ns.response(409, 'Conflict (User already reviewed this place)')
    @reviews_ns.response(404, 'User or Place not found')
    @jwt_required()
    def post(self):
        """Register a new review"""
        user_id = get_jwt_identity()
        review_data = reviews_ns.payload

        if review_data.get('user_id') != user_id:
            # This is a clear authorization failure
            reviews_ns.abort(403, message="Unauthorized: Review must be created by the authenticated user.")
        
        place_id = review_data.get('place_id')

        # 1. Check for User and Place existence before calling Facade
        user = facade.get_user(user_id)
        place = facade.get_place(place_id)

        if not user:
            reviews_ns.abort(404, message=f"User with ID '{review_data.get('user_id')}' not found")
        if not place:
            reviews_ns.abort(404, message=f"Place with ID '{review_data.get('place_id')}' not found")


        place_owner_id = place.owner_id
        if place_owner_id == user_id:
            # This is a forbidden action based on business logic
            reviews_ns.abort(403, message="Forbidden: You cannot review your own place.")
        
        if facade.user_has_reviewed_place(user_id, place_id):
             # This is a data conflict error
            reviews_ns.abort(409, message="Conflict: You have already reviewed this place.")
        
        # 4. Replace IDs with model objects for Facade consumption
        review_data['user'] = user
        review_data['place'] = place
        
        try:
            new_review = facade.create_review(review_data)
            return new_review, 201
        
        # --- Catching specific exceptions from the Facade (if you had them) ---
        except (TypeError, ValueError) as e:
            # Catching validation errors or bad data from the Facade/Model
            reviews_ns.abort(400, message=str(e))
        except Exception as e:
            # Generic error catcher
            reviews_ns.abort(500, message=f"Internal Server Error during review creation: {str(e)}")
            
    @reviews_ns.doc('list_reviews')
    @reviews_ns.marshal_list_with(review_response_model)
    @reviews_ns.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return reviews, 200

# -------------------------------------------------------------
# Resource: /reviews/<review_id>
# -------------------------------------------------------------

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
        
        return review, 200

    # Implemented PUT method
    @reviews_ns.doc('update_review', security='jwt')
    @reviews_ns.expect(review_update_model, validate=True) # Use the partial update model
    @reviews_ns.marshal_with(review_response_model)
    @reviews_ns.response(200, 'Review updated successfully')
    @reviews_ns.response(404, 'Review not found')
    @reviews_ns.response(400, 'Invalid input data')
    @reviews_ns.response(403, 'Unauthorized to update the review')
    @jwt_required()
    def put(self, review_id):
        """Update a review's content or rating"""
        user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False) # Check for Admin claim
        
        review_data = reviews_ns.payload

        review = facade.get_review(review_id)
        if not review:
            reviews_ns.abort(404, message=f"Review with ID '{review_id}' not found")

        review_author_id = review.user_id
        
        # Check 1: Must be the author
        # Check 2: OR must be an Admin
        if review_author_id != user_id and not is_admin:
            reviews_ns.abort(403, message="Unauthorized: You can only update your own reviews unless you are an Admin.")

        # process the update          
        try:
            updated_review = facade.update_review(review_id, review_data)
            
            if not updated_review:
                reviews_ns.abort(404, message=f"Review with ID '{review_id}' not found")
                
            return updated_review, 200 
            
        except (TypeError, ValueError) as e:
            reviews_ns.abort(400, message=str(e))


    # Finalized DELETE method (removed 501 placeholder)
    @reviews_ns.doc('delete_review', security='jwt')
    @reviews_ns.response(204, 'Review deleted successfully (No Content)')
    @reviews_ns.response(404, 'Review not found')
    @reviews_ns.response(403, 'Unauthorized to delete the review')
    @jwt_required()
    def delete(self, review_id):
        user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        
        review = facade.get_review(review_id)
        
        if not review:
            reviews_ns.abort(404, message=f"Review with ID '{review_id}' not found")
            
        review_author_id = review.user_id 
        
        # Authorization Check: Allow Author OR Admin to delete
        if review_author_id != user_id and not is_admin:
            reviews_ns.abort(403, message="Unauthorized: You can only delete your own reviews or be an Admin.")
        
        is_deleted = facade.delete_review(review_id)
        
        if not is_deleted:
            reviews_ns.abort(404, message=f"Review with ID '{review_id}' not found")

        return None, 204

# -------------------------------------------------------------
# Resource: /places/<place_id>/reviews
# -------------------------------------------------------------

@reviews_ns.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    
    @reviews_ns.doc('list_place_reviews')
    @reviews_ns.marshal_list_with(review_response_model)
    @reviews_ns.response(200, 'List of reviews for the place retrieved successfully')
    @reviews_ns.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        # 1. Check if the Place exists (recommended for a clean 404)
        place = facade.get_place(place_id)
        if not place:
            reviews_ns.abort(404, message=f"Place with ID '{place_id}' not found")
        
        # 2. Retrieve reviews via the Facade (which should return a list of Review objects)
        reviews = facade.get_reviews_by_place(place_id)
        return reviews, 200