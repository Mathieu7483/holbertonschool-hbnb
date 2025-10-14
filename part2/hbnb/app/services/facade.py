from uuid import uuid4
from datetime import datetime
from app.persistence.repository import InMemoryRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ===== USER METHODS =====
    def create_user(self, user_data):
        """Create a new user"""
        # Generate ID and timestamps
        user_id = str(uuid4())
        now = datetime.now().isoformat()
        
        # Create user with all required parameters
        user = User(
            id=user_id,
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=user_data.get('email'),
            is_admin=user_data.get('is_admin', False),
            created_at=now,
            updated_at=now
        )
        
        # Validate user
        user.validate
        
        # Add to repository
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID"""
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """Retrieve all users"""
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        """Retrieve a user by email"""
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        """Update a user"""
        user = self.user_repo.get(user_id)
        if user:
            user.update(user_data)
        return user

    # ===== AMENITY METHODS =====
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        pass

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID"""
        pass

    def get_all_amenities(self):
        """Retrieve all amenities"""
        pass

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity"""
        pass

    # ===== PLACE METHODS =====
    def create_place(self, place_data):
        """Create a new place"""
        pass

    def get_place(self, place_id):
        """Retrieve a place by ID"""
        pass

    def get_all_places(self):
        """Retrieve all places"""
        pass

    def update_place(self, place_id, place_data):
        """Update a place"""
        pass

    # ===== REVIEW METHODS =====
    def create_review(self, review_data):
        """Create a new review"""
        pass

    def get_review(self, review_id):
        """Retrieve a review by ID"""
        pass

    def get_all_reviews(self):
        """Retrieve all reviews"""
        pass

    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place"""
        pass

    def update_review(self, review_id, review_data):
        """Update a review"""
        pass

    def delete_review(self, review_id):
        """Delete a review"""
        pass