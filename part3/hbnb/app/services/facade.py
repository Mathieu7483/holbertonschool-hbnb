from typing import Optional, Dict
from app.models import User, Amenity, Place, Review
from app.extensions import db
from app.persistence.UserRepository import UserRepository
from app.persistence.PlaceRepository import PlaceRepository
from app.persistence.ReviewRepository import ReviewRepository
from app.persistence.AmenityRepository import AmenityRepository

class HBnBFacade:
    """
    Centralizes the business logic and orchestrates communication between the API
    and the persistence layer.
    """

    def __init__(self):
        # Initializes repositories for each entity.
        self.user_repository = UserRepository()
        self.place_repository = PlaceRepository()
        self.review_repository = ReviewRepository()
        self.amenity_repository = AmenityRepository()

    # ==================================
    # ===== USER METHODS (CRUD) ========
    # ==================================

    def create_user(self, user_data: Dict) -> User:
        """Creates a new user and persists it."""
        email = user_data.get('email')
        if not email:
            raise ValueError("Email is required.")
        if self.get_user_by_email(email):
            raise ValueError(f"User with email '{email}' already exists.")

        # Password hashing is handled by the @password.setter in the User model
        new_user = User(**user_data)
        
        # Save via the repository
        self.user_repository.add(new_user)
        return new_user

    def get_all_users(self) -> list[User]:
        """Retrieves all users."""
        return self.user_repository.get_all()

    def get_user(self, user_id: str) -> Optional[User]:
        """Retrieves a user by their ID."""
        return self.user_repository.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieves a user by their email."""
        return self.user_repository.get_by_attribute('email', email)

    def update_user(self, user_id: str, profile_data: Dict) -> Optional[User]:
        """Updates a user's basic profile (first name, last name)."""
        user = self.get_user(user_id)
        if not user:
            return None

        # Fields allowed for a standard profile update
        allowed_fields = {'first_name', 'last_name'}
        data_to_update = {
            key: value for key, value in profile_data.items() if key in allowed_fields
        }

        if data_to_update:
            user.update(data_to_update) # The BaseModel.update method saves the changes

        return user

    def update_user_by_admin(self, user_id: str, admin_data: Dict) -> Optional[User]:
        """Updates any user attribute as an administrator."""
        user = self.get_user(user_id)
        if not user:
            return None
        
        new_email = admin_data.get('email')
        if new_email and new_email != user.email:
            if self.get_user_by_email(new_email):
                raise ValueError(f"User with email '{new_email}' already exists.")
        
        # The model handles attribute assignment and password hashing
        user.update(admin_data)
        return user

    def delete_user(self, user_id: str) -> bool:
        """Deletes a user by their ID."""
        user_to_delete = self.get_user(user_id)
        if not user_to_delete:
            return False
        
        self.user_repository.delete(user_to_delete)
        
        return True

    # ==================================
    # ===== AMENITY METHODS (CRUD) =====
    # ==================================

    def create_amenity(self, amenity_data: Dict) -> Amenity:
        """Creates a new amenity."""
        name = amenity_data.get('name')
        if not name:
            raise ValueError("Amenity name is required.")
        if self.amenity_repository.get_by_attribute('name', name):
            raise ValueError(f"Amenity with name '{name}' already exists.")
        
        new_amenity = Amenity(**amenity_data)
        self.amenity_repository.add(new_amenity)
        return new_amenity

    def get_all_amenities(self) -> list[Amenity]:
        """Retrieves all amenities."""
        return self.amenity_repository.get_all()

    def get_amenity(self, amenity_id: str) -> Optional[Amenity]:
        """Retrieves an amenity by its ID."""
        return self.amenity_repository.get(amenity_id)

    def update_amenity(self, amenity_id: str, amenity_data: Dict) -> Optional[Amenity]:
        """Updates an amenity."""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        
        # Check for uniqueness of the new name if provided
        new_name = amenity_data.get('name')
        if new_name and new_name != amenity.name:
            if self.amenity_repository.get_by_attribute('name', new_name):
                 raise ValueError(f"Amenity with name '{new_name}' already exists.")

        amenity.update(amenity_data)
        return amenity

    def delete_amenity(self, amenity_id: str) -> bool:
        """Deletes an amenity."""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return False
        self.amenity_repository.delete(amenity)
        return True
    
    # ==================================
    # ===== PLACE METHODS (CRUD) =======
    # ==================================

    def create_place(self, place_data: Dict) -> Place:
        owner_id = place_data.get('owner_id')
        if not owner_id:
            raise ValueError("owner_id is required to create a place.")
        if not self.get_user(owner_id):
            raise ValueError(f"Owner with ID '{owner_id}' not found.")

        # 1. Pop 'amenities' IDs
        amenity_ids = place_data.pop('amenities', []) 
        
        # 2. Create Place instance with simple attributes
        new_place = Place(**place_data)
        
        # 3. Convert IDs to Amenity objects and link them
        if amenity_ids:
            # Fetch Amenity objects using the IDs
            amenity_objects = db.session.scalars(
                db.select(Amenity).filter(Amenity.id.in_(amenity_ids))
            ).all()
            
            new_place.amenities.extend(amenity_objects)

        # 4. Save
        self.place_repository.add(new_place)
        
        return new_place

    def get_all_places(self) -> list[Place]:
        """Retrieves all places."""
        return self.place_repository.get_all()

    def get_place(self, place_id: str) -> Optional[Place]:
        """Retrieves a place by its ID."""
        return self.place_repository.get(place_id)

    def update_place(self, place_id: str, place_data: Dict) -> Optional[Place]:
        """Updates a place."""
        place = self.get_place(place_id)
        if not place:
            return None
        
        # Amenity management (ADDING AMENITY LOGIC)
        amenity_ids = place_data.pop('amenities', None)
        if amenity_ids is not None:
            amenity_objects = db.session.scalars(
                db.select(Amenity).filter(Amenity.id.in_(amenity_ids))
            ).all()
            if len(amenity_objects) != len(amenity_ids):
                raise ValueError("One or more amenities not found.")
            place.amenities = amenity_objects  # Replaces the old list

        # Protect non-modifiable fields like owner_id
        place_data.pop('owner_id', None)
        
        place.update(place_data)
        return place
        
    def delete_place(self, place_id: str) -> bool:
        """Deletes a place."""
        place = self.get_place(place_id)
        if not place:
            return False
        self.place_repository.delete(place)
        return True

    # ==================================
    # ===== REVIEW METHODS (CRUD/CUSTOM) ======
    # ==================================
    
    # NEW METHOD REQUIRED FOR API CHECK
    def user_has_reviewed_place(self, user_id: str, place_id: str) -> bool:
        """Checks if a user has already written a review for a given place."""
        # Requires the ReviewRepository to have a get_by_attributes (or equivalent) method
        existing_review = self.review_repository.get_by_attributes(
            user_id=user_id,
            place_id=place_id
        )
        return existing_review is not None
    
    # MODIFICATION OF SIGNATURE AND LOGIC
    # The API is corrected to pass clean review_data (containing place_id and user_id)
    def create_review(self, review_data: Dict) -> Review:
        """Creates a new review."""
        
        place_id = review_data.get('place_id')
        user_id = review_data.get('user_id')
        
        if not place_id or not user_id:
            raise ValueError("place_id and user_id are required in review_data.")

        place = self.get_place(place_id)
        user = self.get_user(user_id)
        
        if not place:
            raise ValueError(f"Place with ID '{place_id}' not found.")
        if not user:
            raise ValueError(f"User with ID '{user_id}' not found.")

        # AUTHORIZATION LOGIC (for consistency with the test)
        if place.owner_id == user_id:
             raise ValueError("Owner cannot review their own place.") # API should return 403 Forbidden
        
        # DUPLICATION LOGIC (the one that caused the previous error)
        if self.user_has_reviewed_place(user_id, place_id):
             raise ValueError("User has already reviewed this place.") # API should return 409 Conflict

        new_review = Review(**review_data)
        self.review_repository.add(new_review)
        return new_review

    def get_reviews_for_place(self, place_id: str) -> list[Review]:
        """Retrieves all reviews for a specific place."""
        place = self.get_place(place_id)
        if not place:
            raise ValueError(f"Place with ID '{place_id}' not found.")
        
        # Uses the relationship defined in the Place model
        return place.reviews

    def get_review(self, review_id: str) -> Optional[Review]:
        """Retrieves a review by its ID."""
        return self.review_repository.get(review_id)
        
    def update_review(self, review_id: str, review_data: Dict) -> Optional[Review]:
        """Updates a review."""
        review = self.get_review(review_id)
        if not review:
            return None
        
        # Protect non-modifiable fields
        review_data.pop('user_id', None)
        review_data.pop('place_id', None)

        review.update(review_data)
        return review

    def delete_review(self, review_id: str) -> bool:
        """Deletes a review."""
        review = self.get_review(review_id)
        if not review:
            return False
        self.review_repository.delete(review)
        return True