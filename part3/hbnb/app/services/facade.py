from uuid import uuid4
from datetime import datetime
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from typing import Optional, Dict
from app.persistence import UserRepository, AmenityRepository, PlaceRepository, ReviewRepository


class HBnBFacade:
    """
    The Facade pattern implementation for the HBnB application.
    It centralizes the business logic and orchestrates communication
    between the Presentation layer (API) and the Persistence layer (Repository).
    """

    def __init__(self):
        # Initializes separate repositories for each entity type.
        self.user_repository = UserRepository()
        self.place_repository = PlaceRepository()
        self.review_repository = ReviewRepository()
        self.amenity_repository = AmenityRepository()

    # ==================================
    # ===== USER METHODS (CRUD) ========
    # ==================================

    def create_user(self, user_data: Dict) -> User:
        """Creates a new User instance, validates it, and persists it."""
        email = user_data.get('email')
        if not email:
            raise ValueError("Email is required to create a User.")

        if self.get_user_by_email(email):
            raise ValueError(f"User with email '{email}' already exists.")

        user = User(**user_data)

        # Validation is handled within the User model's __init__
        user.validate()
        self.user_repository.add(user)
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        """Retrieves a User by ID."""
        return self.user_repository.get(user_id)

    def get_all_users(self) -> list[User]:
        """Retrieves all Users."""
        return self.user_repository.get_all()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieves a User by email attribute."""
        # Requires the InMemoryRepository to implement 'get_by_attribute'
        return self.user_repository.get_by_attribute('email', email)

    def update_user(self, user_id: str, user_data: Dict) -> Optional[User]:
        """Updates a User's attributes."""
        user = self.user_repository.get(user_id)
        if not user:
            return None
        # Only allow updating certain fields
        allowed_fields = {'first_name', 'last_name'}
        filtered_data = {}
        for key, value in user_data.items():
            if key in allowed_fields:
                filtered_data[key] = value
    
        if filtered_data:
            user.update(filtered_data)
    
        return user.to_dict()

    # ==================================
    # ===== AMENITY METHODS (CRUD) =====
    # ==================================

    def create_amenity(self, amenity_data: Dict) -> Amenity:
        """Creates a new Amenity instance, validates it, and persists it."""
        amenity = Amenity(**amenity_data)
        amenity.validate()
        self.amenity_repository.add(amenity)
        return amenity

    def get_amenity(self, amenity_id: str) -> Optional[Amenity]:
        """Retrieves an Amenity by ID."""
        return self.amenity_repository.get(amenity_id)

    def get_all_amenities(self) -> list[Amenity]:
        """Retrieves all Amenities."""
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id: str, amenity_data: Dict) -> Optional[Amenity]:
        """Updates an Amenity's attributes."""
        amenity = self.amenity_repository.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)
        return amenity

    # ==================================
    # ===== PLACE METHODS (CRUD) =======
    # ==================================

    def create_place(self, place_data: Dict) -> Place:
        """
        Creates a new Place and establishes the relationship with its owner (User).
        """
        owner_id = place_data.get('owner_id')
        owner = self.get_user(owner_id)
        if not owner:
            raise LookupError(f"Owner with ID '{owner_id}' not found")

        place_data = place_data.copy()
        place_data['owner'] = owner
        place = Place(**place_data)
        place.validate()
        self.place_repository.add(place)
        return place.to_dict()

    def get_place(self, place_id: str) -> Optional[Place]:
        """Retrieves a Place by ID."""
        place = self.place_repository.get(place_id)
        return place.to_dict() if place else None

    def get_all_places(self) -> list[Place]:
        """Retrieves all Places."""
        places = self.place_repository.get_all()
        return [place.to_dict() for place in places]

    def update_place(self, place_id: str, place_data: Dict) -> Optional[Place]:
        """Updates a Place's attributes."""
        place = self.place_repository.get(place_id)
        if place:
            place.update(place_data)
        return place.to_dict() if place else None

    # ==================================
    # ===== REVIEW METHODS (CRUD+) =====
    # ==================================

    def create_review(self, review_data: Dict) -> Review:
        """
        Creates a new Review, links it to Place and User, and updates the Place's review list.
        """
        place = self.get_place(review_data.get('place_id'))
        user = self.get_user(review_data.get('user_id'))

        if not place or not user:
            raise LookupError("Place or User ID not found for review creation.")

        review_data = review_data.copy()
        review_data['place'] = place
        review_data['user'] = user

        review = Review(**review_data)
        review.validate()
        self.review_repository.add(review)

        if not hasattr(place, 'reviews'):
            place.reviews = []
        place.reviews.append(review)

        return review

    def get_review(self, review_id: str) -> Optional[Review]:
        """Retrieves a Review by ID."""
        return self.review_repository.get(review_id)

    def get_all_reviews(self) -> list[Review]:
        """Retrieves all Reviews."""
        return self.review_repository.get_all()

    def get_reviews_by_place(self, place_id: str) -> list[Review]:
        """
        Retrieves all Reviews associated with a specific Place.
        Requires the Repository to implement 'get_by_attribute'.
        """
        place_obj = self.get_place(place_id)
        if not place_obj:
            return []

        # Find reviews where the 'place' attribute is the Place object
        return self.review_repository.get_by_attribute('place', place_obj)

    def update_review(self, review_id: str, review_data: Dict) -> Optional[Review]:
        """Updates a Review's attributes (PUT)."""
        review = self.review_repository.get(review_id)
        if review:
            review.update(review_data)
        return review

    def delete_review(self, review_id: str) -> bool:
        """
        Deletes a Review (DELETE), and removes the reference from the parent Place,
        maintaining data consistency. (Required for Task 5).
        """
        return self.review_repository.delete(review_id)
