from typing import Optional, Dict, List
from app.models import User, Amenity, Place, Review
from app.extensions import db
from app.persistence.UserRepository import UserRepository
from app.persistence.PlaceRepository import PlaceRepository
from app.persistence.ReviewRepository import ReviewRepository
from app.persistence.AmenityRepository import AmenityRepository
from sqlalchemy.orm import selectinload, joinedload

class HBnBFacade:
    
    def __init__(self):
        self.user_repository = UserRepository()
        self.place_repository = PlaceRepository()
        self.review_repository = ReviewRepository()
        self.amenity_repository = AmenityRepository()

    # ==================================
    # ===== USER METHODS (CRUD) ========
    # ==================================

    def create_user(self, user_data: Dict) -> User:
        email = user_data.get('email')
        if not email:
            raise ValueError("Email is required.")
        
        if self.get_user_by_email(email):
            raise ValueError(f"User with email '{email}' already exists.")

        new_user = User(**user_data)
        self.user_repository.add(new_user)
        return new_user

    def get_all_users(self) -> List[User]:
        return self.user_repository.get_all()

    def get_user(self, user_id: str) -> Optional[User]:
        return self.user_repository.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_repository.get_by_attribute('email', email)

    def update_user(self, user_id: str, profile_data: Dict) -> Optional[User]:
        user = self.get_user(user_id)
        if not user:
            return None

        allowed_fields = {'first_name', 'last_name'}
        data_to_update = {
            key: value for key, value in profile_data.items() if key in allowed_fields
        }

        if data_to_update:
            user.update(data_to_update)

        return user

    def update_user_by_admin(self, user_id: str, admin_data: Dict) -> Optional[User]:
        user = self.get_user(user_id)
        if not user:
            return None
        
        new_email = admin_data.get('email')
        if new_email and new_email != user.email:
            if self.get_user_by_email(new_email):
                raise ValueError(f"User with email '{new_email}' already exists.")
        
        user.update(admin_data)
        return user

    def delete_user(self, user_id: str) -> bool:
        user_to_delete = self.get_user(user_id)
        if not user_to_delete:
            return False
        
        self.user_repository.delete(user_to_delete)
        return True

    # ==================================
    # ===== AMENITY METHODS (CRUD) =====
    # ==================================

    def create_amenity(self, amenity_data: Dict) -> Amenity:
        name = amenity_data.get('name')
        if not name:
            raise ValueError("Amenity name is required.")
        
        if self.amenity_repository.get_by_attribute('name', name):
            raise ValueError(f"Amenity with name '{name}' already exists.")
        
        new_amenity = Amenity(**amenity_data)
        self.amenity_repository.add(new_amenity)
        return new_amenity

    def get_all_amenities(self) -> List[Amenity]:
        return self.amenity_repository.get_all()

    def get_amenity(self, amenity_id: str) -> Optional[Amenity]:
        return self.amenity_repository.get(amenity_id)

    def update_amenity(self, amenity_id: str, amenity_data: Dict) -> Optional[Amenity]:
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        
        new_name = amenity_data.get('name')
        if new_name and new_name != amenity.name:
            if self.amenity_repository.get_by_attribute('name', new_name):
                raise ValueError(f"Amenity with name '{new_name}' already exists.")

        amenity.update(amenity_data)
        return amenity

    def delete_amenity(self, amenity_id: str) -> bool:
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

        amenity_ids = place_data.get('amenities', [])
        place_data_copy = {k: v for k, v in place_data.items() if k != 'amenities'}
        
        new_place = Place(**place_data_copy)
        
        if amenity_ids:
            amenity_objects = db.session.scalars(
                db.select(Amenity).filter(Amenity.id.in_(amenity_ids))
            ).all()
            
            if len(amenity_objects) != len(amenity_ids):
                raise ValueError("One or more amenities not found.")
            
            new_place.amenities.extend(amenity_objects)

        self.place_repository.add(new_place)
        return new_place

    def get_place(self, place_id: str) -> Optional[Place]:
        query = db.select(Place).filter_by(id=place_id).options(
            selectinload(Place.amenities),
            selectinload(Place.reviews),
            joinedload(Place.owner)
        )
        return db.session.execute(query).scalar_one_or_none()

    def get_all_places(self) -> List[Place]:
        query = db.select(Place).options(
            selectinload(Place.amenities),
            selectinload(Place.reviews),
            joinedload(Place.owner)
        )
        return db.session.execute(query).unique().scalars().all()

    def update_place(self, place_id: str, place_data: Dict) -> Optional[Place]:
        place = self.get_place(place_id)
        if not place:
            return None

        amenity_ids = place_data.pop('amenities', None)
        if amenity_ids is not None:
            amenity_objects = db.session.scalars(
                db.select(Amenity).filter(Amenity.id.in_(amenity_ids))
            ).all()
            if len(amenity_objects) != len(amenity_ids):
                raise ValueError("One or more amenities not found.")
            place.amenities = amenity_objects

        place_data.pop('owner_id', None)
        
        place.update(place_data)
        return place

    def delete_place(self, place_id: str) -> bool:
        place = self.get_place(place_id)
        if not place:
            return False
        self.place_repository.delete(place)
        return True

    # ==================================
    # ===== REVIEW METHODS (CRUD) ======
    # ==================================

    def user_has_reviewed_place(self, user_id: str, place_id: str) -> bool:
        existing_review = self.review_repository.get_by_attributes(
            user_id=user_id,
            place_id=place_id
        )
        return existing_review is not None

    def create_review(self, review_data: Dict) -> Review:
        place_id = review_data.get('place_id')
        user_id = review_data.get('user_id')
        
        if not place_id or not user_id:
            raise ValueError("place_id and user_id are required.")

        place = self.get_place(place_id)
        user = self.get_user(user_id)
        
        if not place:
            raise ValueError(f"Place with ID '{place_id}' not found.")
        if not user:
            raise ValueError(f"User with ID '{user_id}' not found.")

        if place.owner_id == user_id:
            raise ValueError("Owner cannot review their own place.")
        
        if self.user_has_reviewed_place(user_id, place_id):
            raise ValueError("User has already reviewed this place.")

        new_review = Review(**review_data)
        self.review_repository.add(new_review)
        return new_review

    def get_reviews_by_place(self, place_id: str) -> List[Review]:
        place = self.get_place(place_id)
        if not place:
            raise ValueError(f"Place with ID '{place_id}' not found.")
        return place.reviews

    def get_all_reviews(self) -> List[Review]:
        return self.review_repository.get_all()

    def get_review(self, review_id: str) -> Optional[Review]:
        return self.review_repository.get(review_id)

    def update_review(self, review_id: str, review_data: Dict) -> Optional[Review]:
        review = self.get_review(review_id)
        if not review:
            return None

        review_data.pop('user_id', None)
        review_data.pop('place_id', None)

        review.update(review_data)
        return review

    def delete_review(self, review_id: str) -> bool:
        review = self.get_review(review_id)
        if not review:
            return False
        self.review_repository.delete(review)
        return True