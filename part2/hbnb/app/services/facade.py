from uuid import uuid4
from datetime import datetime
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ===== USER METHODS =====
    def create_user(self, user_data):
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
        
        user.validate
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if user:
            user.update(user_data)
        return user
    


    # ===== AMENITY METHODS =====
    def create_amenity(self, amenity_data):
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

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)
        return amenity
    


    # ===== PLACE METHODS =====
    def create_place(self, place_data):
        """Create a new place and return the Place object"""
        place_id = str(uuid4())
        now = datetime.now().isoformat()
        
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
            owner=owner,
            created_at=now,
            updated_at=now
        )
        
        place.validate
        self.place_repo.add(place)
        
        return place

    def get_place(self, place_id):
        """Retrieve a place by ID and return the Place object"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places and return a list of Place objects"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place and return the updated Place object"""
        place = self.place_repo.get(place_id)
        if place:
            place.update(place_data)
        return place
    


    # ===== REVIEW METHODS =====
    def create_review(self, review_data):
        review_id = str(uuid4())
        now = datetime.now().isoformat()
        
        review = Review(
            id=review_id,
            text=review_data.get('text'),
            rating=review_data.get('rating'),
            place=review_data.get('place'),
            user=review_data.get('user'),
            created_at=now,
            updated_at=now
        )
        
        review.validate
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return self.review_repo.get_by_attribute('place', place_id) 

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if review:
            review.update(review_data)
        return review
    