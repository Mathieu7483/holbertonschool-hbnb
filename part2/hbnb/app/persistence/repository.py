from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    """Single shared repository for all models"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Singleton pattern to ensure only one instance exists"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize storage only once"""
        if not InMemoryRepository._initialized:
            # Separate storage by entity type
            self._storage: Dict[str, Dict[str, object]] = {
                'User': {},
                'Place': {},
                'Review': {},
                'Amenity': {}
            }
            InMemoryRepository._initialized = True
    
    def _get_entity_type(self, obj):
        """Determine entity type from class name"""
        return obj.__class__.__name__
    
    def add(self, obj):
        """Add an object to the repository"""
        entity_type = self._get_entity_type(obj)
        if entity_type not in self._storage:
            self._storage[entity_type] = {}
        self._storage[entity_type][obj.id] = obj
    
    def get(self, obj_id, entity_type=None):
        """
        Retrieve an object by ID
        If entity_type is not provided, searches all types
        """
        if entity_type:
            return self._storage.get(entity_type, {}).get(obj_id)
        
        # Search across all types
        for storage in self._storage.values():
            if obj_id in storage:
                return storage[obj_id]
        return None
    
    def get_all(self, entity_type=None):
        """
        Retrieve all objects of a specific type
        If entity_type is not provided, returns all objects
        """
        if entity_type:
            return list(self._storage.get(entity_type, {}).values())
        
        # Return all objects from all types
        all_objects = []
        for storage in self._storage.values():
            all_objects.extend(storage.values())
        return all_objects
    
    def update(self, obj_id, data, entity_type=None):
        """Update an object"""
        obj = self.get(obj_id, entity_type)
        if obj:
            obj.update(data)
    
    def delete(self, obj_id, entity_type=None):
        """Delete an object"""
        if entity_type:
            if obj_id in self._storage.get(entity_type, {}):
                del self._storage[entity_type][obj_id]
                return True
        else:
            # Search across all types
            for storage in self._storage.values():
                if obj_id in storage:
                    del storage[obj_id]
                    return True
        return False
    
    def get_by_attribute(self, attr_name, attr_value, entity_type=None):
        """Find an object by attribute"""
        objects = self.get_all(entity_type)
        return next((obj for obj in objects if getattr(obj, attr_name, None) == attr_value), None)
    
    def get_all_by_attribute(self, attr_name, attr_value, entity_type=None):
        """Find all objects matching an attribute"""
        objects = self.get_all(entity_type)
        return [obj for obj in objects if getattr(obj, attr_name, None) == attr_value]


# Global singleton instance
repo = InMemoryRepository()


# ============================================================
# FACADES for each model
# ============================================================

class UserFacade:
    """Facade to manage users"""
    
    def __init__(self):
        self.repository = repo  # Use the singleton repository
    
    def create_user(self, user_data: dict):
        """Create a user"""
        from models.user import User
        user = User(**user_data)
        self.repository.add(user)
        return user
    
    def get_user(self, user_id: str):
        """Retrieve a user by ID"""
        return self.repository.get(user_id, 'User')
    
    def get_user_by_email(self, email: str):
        """Retrieve a user by email"""
        return self.repository.get_by_attribute('email', email, 'User')
    
    def get_all_users(self):
        """Retrieve all users"""
        return self.repository.get_all('User')
    
    def update_user(self, user_id: str, data: dict):
        """Update a user"""
        self.repository.update(user_id, data, 'User')
        return self.get_user(user_id)
    


class PlaceFacade:
    """Facade to manage places"""
    
    def __init__(self):
        self.repository = repo  # Same repository!
    
    def create_place(self, place_data: dict):
        """Create a place with reference to User"""
        from models.place import Place
        
        # Retrieve the owner from the SAME repository
        owner_id = place_data.get('owner_id')
        owner = self.repository.get(owner_id, 'User')
        
        if not owner:
            raise ValueError(f"Owner with id {owner_id} not found")
        
        # Create the place
        place = Place(**place_data)
        place.owner = owner  # Attach the complete User object
        
        self.repository.add(place)
        return place
    
    def get_place(self, place_id: str):
        """Retrieve a place by ID"""
        place = self.repository.get(place_id, 'Place')
        if place and place.owner_id:
            # Load owner if not already loaded
            if not hasattr(place, 'owner') or place.owner is None:
                place.owner = self.repository.get(place.owner_id, 'User')
        return place
    
    def get_all_places(self):
        """Retrieve all places"""
        places = self.repository.get_all('Place')
        # Load owners for all places
        for place in places:
            if place.owner_id and (not hasattr(place, 'owner') or place.owner is None):
                place.owner = self.repository.get(place.owner_id, 'User')
        return places
    
    def get_places_by_owner(self, owner_id: str):
        """Retrieve all places of an owner"""
        return self.repository.get_all_by_attribute('owner_id', owner_id, 'Place')
    
    def update_place(self, place_id: str, data: dict):
        """Update a place"""
        self.repository.update(place_id, data, 'Place')
        return self.get_place(place_id)
    


class ReviewFacade:
    """Facade to manage reviews"""
    
    def __init__(self):
        self.repository = repo
    
    def create_review(self, review_data: dict):
        """Create a review with references to User and Place"""
        from models.review import Review
        
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        
        # Verify that user and place exist in the SAME repository
        user = self.repository.get(user_id, 'User')
        place = self.repository.get(place_id, 'Place')
        
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        if not place:
            raise ValueError(f"Place with id {place_id} not found")
        
        review = Review(**review_data)
        review.user = user
        review.place = place
        
        self.repository.add(review)
        return review
    
    def get_review(self, review_id: str):
        """Retrieve a review by ID"""
        review = self.repository.get(review_id, 'Review')
        if review:
            # Load relationships
            if not hasattr(review, 'user') or review.user is None:
                review.user = self.repository.get(review.user_id, 'User')
            if not hasattr(review, 'place') or review.place is None:
                review.place = self.repository.get(review.place_id, 'Place')
        return review
    
    def get_all_reviews(self):
        """Retrieve all reviews"""
        return self.repository.get_all('Review')
    
    def get_reviews_by_place(self, place_id: str):
        """Retrieve all reviews of a place"""
        return self.repository.get_all_by_attribute('place_id', place_id, 'Review')
    
    def get_reviews_by_user(self, user_id: str):
        """Retrieve all reviews of a user"""
        return self.repository.get_all_by_attribute('user_id', user_id, 'Review')
    
    def update_review(self, review_id: str, data: dict):
        """Update a review"""
        self.repository.update(review_id, data, 'Review')
        return self.get_review(review_id)
    


class AmenityFacade:
    """Facade to manage amenities"""
    
    def __init__(self):
        self.repository = repo
    
    def create_amenity(self, amenity_data: dict):
        """Create an amenity"""
        from models.amenity import Amenity
        amenity = Amenity(**amenity_data)
        self.repository.add(amenity)
        return amenity
    
    def get_amenity(self, amenity_id: str):
        """Retrieve an amenity by ID"""
        return self.repository.get(amenity_id, 'Amenity')
    
    def get_all_amenities(self):
        """Retrieve all amenities"""
        return self.repository.get_all('Amenity')
    
    def update_amenity(self, amenity_id: str, data: dict):
        """Update an amenity"""
        self.repository.update(amenity_id, data, 'Amenity')
        return self.get_amenity(amenity_id)
    
