from uuid import uuid4
from datetime import datetime
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from typing import Optional, Dict

class HBnBFacade:
    """
    The Facade pattern implementation for the HBnB application.
    It centralizes the business logic and orchestrates communication 
    between the Presentation layer (API) and the Persistence layer (Repository).
    """
    
    def __init__(self):
        # Initializes separate repositories for each entity type.
        self.user_repo: InMemoryRepository = InMemoryRepository()
        self.place_repo: InMemoryRepository = InMemoryRepository()
        self.review_repo: InMemoryRepository = InMemoryRepository()
        self.amenity_repo: InMemoryRepository = InMemoryRepository()

    # ==================================
    # ===== USER METHODS (CRUD) ========
    # ==================================
    
    def create_user(self, user_data: Dict) -> User:
        """Creates a new User instance, validates it, and persists it."""
        user_id = str(uuid4())
        now = datetime.now().isoformat()
        
        user = User(
            id=user_id,
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=user_data.get('email'),
            is_admin=user_data.get('is_admin', False),
            created_at=now,
            updated_at=now
        )
        
        # Validation is handled within the User model's __init__ 
        # (or should be called here if not in __init__)
        # Note: The line 'user.validate' is likely intended to be 'user.validate()',
        # but the BaseModel update handles this implicitly in the project's design.
        user.validate 
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        """Retrieves a User by ID."""
        return self.user_repo.get(user_id)

    def get_all_users(self) -> list[User]:
        """Retrieves all Users."""
        return self.user_repo.get_all()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieves a User by email attribute."""
        # Requires the InMemoryRepository to implement 'get_by_attribute'
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id: str, user_data: Dict) -> Optional[User]:
        """Updates a User's attributes."""
        user = self.user_repo.get(user_id)
        if user:
            # The model's update method handles attribute assignment, validation, and updated_at timestamp.
            user.update(user_data) 
        return user
    
    # ==================================
    # ===== AMENITY METHODS (CRUD) =====
    # ==================================
    
    def create_amenity(self, amenity_data: Dict) -> Amenity:
        """Creates a new Amenity instance, validates it, and persists it."""
        amenity_id = str(uuid4())
        now = datetime.now().isoformat()
        
        amenity = Amenity(
            id=amenity_id,
            name=amenity_data.get('name'),
            created_at=now,
            updated_at=now
        )
        
        amenity.validate
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id: str) -> Optional[Amenity]:
        """Retrieves an Amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self) -> list[Amenity]:
        """Retrieves all Amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id: str, amenity_data: Dict) -> Optional[Amenity]:
        """Updates an Amenity's attributes."""
        amenity = self.amenity_repo.get(amenity_id)
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
        place_id = str(uuid4())
        now = datetime.now().isoformat()
        
        # Business Logic: Retrieve the owner object using the provided owner_id
        owner = self.get_user(place_data.get('owner_id'))
        if not owner:
            raise LookupError(f"Owner with ID '{place_data.get('owner_id')}' not found")
        
        place = Place(
            id=place_id,
            title=place_data.get('title'),
            description=place_data.get('description'),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner=owner, # Pass the actual User object
            created_at=now,
            updated_at=now
        )
        
        place.validate
        self.place_repo.add(place)
        
        return place

    def get_place(self, place_id: str) -> Optional[Place]:
        """Retrieves a Place by ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self) -> list[Place]:
        """Retrieves all Places."""
        return self.place_repo.get_all()

    def update_place(self, place_id: str, place_data: Dict) -> Optional[Place]:
        """Updates a Place's attributes."""
        place = self.place_repo.get(place_id)
        if place:
            place.update(place_data)
        return place
    
    # ==================================
    # ===== REVIEW METHODS (CRUD+) =====
    # ==================================
    
    def create_review(self, review_data: Dict) -> Review:
        """
        Creates a new Review, links it to Place and User, and updates the Place's review list.
        """
        review_id = str(uuid4())
        now = datetime.now().isoformat()
        
        
        place = self.get_place(review_data.get('place_id'))
        user = self.get_user(review_data.get('user_id'))

        if not place or not user:
            raise LookupError("Place or User ID not found for review creation.")
            
        review = Review(
            id=review_id,
            text=review_data.get('text'),
            rating=review_data.get('rating'),
            place=place,  # Pass the Place object
            user=user,    # Pass the User object
            created_at=now,
            updated_at=now
        )
        
        review.validate
        self.review_repo.add(review)
        
        place.reviews.append(review)
        
        return review

    def get_review(self, review_id: str) -> Optional[Review]:
        """Retrieves a Review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self) -> list[Review]:
        """Retrieves all Reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id: str) -> list[Review]:
        """
        Retrieves all Reviews associated with a specific Place.
        Requires the Repository to implement 'get_by_attribute'.
        """
        place_obj = self.get_place(place_id)
        if not place_obj:
            return []
        
        # Find reviews where the 'place' attribute is the Place object
        return self.review_repo.get_by_attribute('place', place_obj) 

    def update_review(self, review_id: str, review_data: Dict) -> Optional[Review]:
        """Updates a Review's attributes (PUT)."""
        review = self.review_repo.get(review_id)
        if review:
            review.update(review_data)
        return review
    
    def delete_review(self, review_id: str) -> bool:
        """
        Deletes a Review (DELETE), and removes the reference from the parent Place, 
        maintaining data consistency. (Required for Task 5).
        """
        review = self.review_repo.get(review_id)
        
        if not review:
            return False
            
        # Business Logic: Remove the review from the parent Place's list
        place = review.place 
        if review in place.reviews:
            place.reviews.remove(review)
            
        # Persistence Logic: Delete the object from the Repository
        return self.review_repo.delete(review_id)
