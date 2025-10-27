import uuid
from datetime import datetime
from typing import Optional, Dict
from abc import ABC, abstractmethod
import time

# =========================================================
# 1. Classes de Base et Persistence (Adaptation du modèle corrigé)
# =========================================================

class BaseModel:
    def __init__(self, id: Optional[str] = None, created_at: Optional[str] = None, updated_at: Optional[str] = None):
        now = datetime.now().isoformat()
        self.id = id if id is not None else str(uuid.uuid4())
        self.created_at = created_at if created_at is not None else now
        self.updated_at = updated_at if updated_at is not None else now

    def save(self):
        """Met à jour l'horodatage updated_at."""
        time.sleep(0.01) # Petit délai pour s'assurer que le timestamp change.
        self.updated_at = datetime.now().isoformat()

    def update(self, data: dict):
        """Mise à jour des attributs du modèle, protégeant l'ID et les dates."""
        protected_keys = ['id', 'created_at', 'updated_at']
        
        for key, value in data.items():
            if hasattr(self, key) and key not in protected_keys:
                setattr(self, key, value)
        
        # Le modèle enfant doit appeler self.validate() après super().update()
        self.save()
        
    def to_dict(self):
        return {
            "id": self.id, 
            "created_at": self.created_at, 
            "updated_at": self.updated_at
        }

class Repository(ABC):
     @abstractmethod
     def get(self, obj_id, entity_type=None): pass
     @abstractmethod
     def add(self, obj): pass

class InMemoryRepository(Repository):
    def __init__(self):
        self._storage: Dict[str, Dict[str, object]] = {
            'User': {}, 'Place': {}, 'Review': {}, 'Amenity': {}
        }
    
    def _get_entity_type(self, obj):
        return obj.__class__.__name__
        
    def add(self, obj):
        entity_type = self._get_entity_type(obj)
        if entity_type not in self._storage:
             self._storage[entity_type] = {}
        self._storage[entity_type][obj.id] = obj

    def get(self, obj_id, entity_type=None):
        if entity_type:
             return self._storage.get(entity_type, {}).get(obj_id)
        return None

    def update(self, obj_id, data, entity_type=None):
        obj = self.get(obj_id, entity_type)
        if obj:
            # Le repository appelle la méthode update du modèle.
            obj.update(data)
            return obj
        return None
        
    def delete(self, obj_id, entity_type=None):
        if entity_type and obj_id in self._storage.get(entity_type, {}):
             del self._storage[entity_type][obj_id]
             return True
        return False
        
repo = InMemoryRepository()

# =========================================================
# 2. Modèles (avec la surcharge de update() et la validation)
# =========================================================

class User(BaseModel):
    def __init__(self, id, first_name, last_name, email, is_admin, created_at, updated_at):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.validate()

    def validate(self):
        if not self.first_name or not self.email:
            raise ValueError("First name or email missing")
        if "@" not in self.email:
             raise ValueError("Invalid email format")
        return True
    
    def update(self, data: dict):
        super().update(data)
        self.validate() # ⬅️ SURCHARGE AVEC VALIDATION

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict.update({"first_name": self.first_name, "last_name": self.last_name, "email": self.email})
        return user_dict
    
class Amenity(BaseModel):
    def __init__(self, id, name, created_at, updated_at):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.name = name
        self.validate()
        
    def validate(self):
        if not self.name or len(self.name) > 50:
            raise ValueError("Invalid or too long name for amenity")
        return True
        
    def update(self, data: dict):
        super().update(data)
        self.validate() # ⬅️ SURCHARGE AVEC VALIDATION
        
    def to_dict(self):
        amenity_dict = super().to_dict()
        amenity_dict.update({"name": self.name})
        return amenity_dict

class Place(BaseModel):
    def __init__(self, id, title, description, price, latitude, longitude, owner, created_at, updated_at):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.amenities = []
        self.reviews = []
        self.validate()

    def validate(self):
        if not isinstance(self.owner, User) or self.price < 0:
            raise ValueError("Invalid owner or price")
        if not (-90 <= self.latitude <= 90):
             raise ValueError("Latitude out of range")
        return True
        
    def update(self, data: dict):
        super().update(data)
        self.validate() # ⬅️ SURCHARGE AVEC VALIDATION

    def to_dict(self):
        place_dict = super().to_dict()
        place_dict.update({
            "title": self.title, 
            "price": self.price,
            "owner": self.owner.to_dict(),
            "amenities": [a.to_dict() for a in self.amenities],
            "reviews_count": len(self.reviews)
        })
        return place_dict
    
class Review(BaseModel):
    def __init__(self, id, text, rating, place, user, created_at, updated_at):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        self.validate()

    def validate(self):
        if not isinstance(self.rating, int) or not (1 <= self.rating <= 5):
            raise ValueError("Invalid rating (must be 1-5)")
        if not self.text:
            raise ValueError("Review text is missing")
        return True
        
    def update(self, data: dict):
        super().update(data)
        self.validate() # ⬅️ SURCHARGE AVEC VALIDATION
    
    def to_dict(self):
        review_dict = super().to_dict()
        review_dict.update({
            "text": self.text, 
            "rating": self.rating, 
            "user_id": self.user.id,
            "place_id": self.place.id
        })
        return review_dict

# =========================================================
# 3. Facades (CORRIGÉES AVEC LES MÉTHODES GET ET DELETE)
# =========================================================

class UserFacade:
    def create_user(self, user_data):
        now = datetime.now().isoformat()
        user_id = str(uuid.uuid4())
        user = User(
            id=user_id, **user_data, created_at=now, updated_at=now
        )
        repo.add(user)
        return user
        
    def get_user(self, user_id): # ✅ MÉTHODE AJOUTÉE
        return repo.get(user_id, 'User')
        
    def update_user(self, user_id, data):
        return repo.update(user_id, data, 'User')

class PlaceFacade:
    def create_place(self, place_data):
        now = datetime.now().isoformat()
        place_id = str(uuid.uuid4())
        owner = repo.get(place_data.pop('owner_id'), 'User')
        if not owner: raise LookupError("Owner not found")
        place = Place(id=place_id, owner=owner, **place_data, created_at=now, updated_at=now)
        repo.add(place)
        return place
        
    def get_place(self, place_id): # ✅ MÉTHODE AJOUTÉE
        return repo.get(place_id, 'Place')
        
    def update_place(self, place_id, data):
        return repo.update(place_id, data, 'Place')

class AmenityFacade:
    def create_amenity(self, amenity_data):
        now = datetime.now().isoformat()
        amenity_id = str(uuid.uuid4())
        amenity = Amenity(id=amenity_id, **amenity_data, created_at=now, updated_at=now)
        repo.add(amenity)
        return amenity
        
    def get_amenity(self, amenity_id): # ✅ MÉTHODE AJOUTÉE
        return repo.get(amenity_id, 'Amenity')

    def update_amenity(self, amenity_id, data):
        return repo.update(amenity_id, data, 'Amenity')

class ReviewFacade:
    def create_review(self, review_data):
        now = datetime.now().isoformat()
        review_id = str(uuid.uuid4())
        place = repo.get(review_data.pop('place_id'), 'Place')
        user = repo.get(review_data.pop('user_id'), 'User')
        if not place or not user: raise LookupError("Place or User not found for review.")

        review = Review(id=review_id, place=place, user=user, **review_data, created_at=now, updated_at=now)
        repo.add(review)
        place.reviews.append(review)
        return review
        
    def get_review(self, review_id): # ✅ MÉTHODE AJOUTÉE
        return repo.get(review_id, 'Review')
        
    def update_review(self, review_id, data):
        return repo.update(review_id, data, 'Review')
        
    def delete_review(self, review_id): # ✅ MÉTHODE AJOUTÉE
        review = repo.get(review_id, 'Review')
        if review:
            # Récupérer l'objet Place lié pour maintenir la cohérence
            place = repo.get(review.place.id, 'Place') 
            
            if place and review in place.reviews:
                place.reviews.remove(review)
            return repo.delete(review_id, 'Review')
        return False

# =========================================================
# 4. Fonction de Simulation et de Test
# =========================================================

def run_simulation():
    # 1. Création des Facades
    user_facade = UserFacade()
    place_facade = PlaceFacade()
    amenity_facade = AmenityFacade()
    review_facade = ReviewFacade()
    
    # Stockage des ID pour les tests
    user_id = None
    place_id = None
    amenity_id = None
    review_id = None

    # --- Test 1 : Création (User, Amenity, Place, Review) ---
    try:
        owner = user_facade.create_user({'first_name': 'Mathieu', 'last_name': 'Testeur', 'email': 'mathieu@hbnb.fr', 'is_admin': False})
        user_id = owner.id
        wifi_amenity = amenity_facade.create_amenity({'name': 'WiFi Gratuit'})
        amenity_id = wifi_amenity.id
        place = place_facade.create_place({'owner_id': owner.id, 'title': 'Appartement Lumineux', 'description': 'Test', 'price': 150, 'latitude': 45.75, 'longitude': 4.85})
        place_id = place.id
        review = review_facade.create_review({'user_id': owner.id, 'place_id': place.id, 'text': "Excellent lieu", 'rating': 5})
        review_id = review.id
        
        place.amenities.append(wifi_amenity)
        
        print("CRÉATION : OKAY")
    except Exception as e:
        print(f"CRÉATION : ÉCHEC ({e})")
        return 

    # --- Test 2 : Mise à jour de l'Utilisateur (PUT) ---
    try:
        user_before = user_facade.get_user(user_id)
        old_updated_at = user_before.updated_at
        
        updated_user = user_facade.update_user(user_id, {'last_name': 'NouveauNom'})
        
        assert updated_user.last_name == 'NouveauNom'
        assert updated_user.updated_at != old_updated_at 
        print("UPDATE USER : OKAY")
    except Exception as e:
        print(f"UPDATE USER : ÉCHEC ({e})")

    # --- Test 3 : Mise à jour de la Commodité (PUT) ---
    try:
        amenity_before = amenity_facade.get_amenity(amenity_id)
        old_updated_at = amenity_before.updated_at
        
        updated_amenity = amenity_facade.update_amenity(amenity_id, {'name': 'Super WiFi'})
        
        assert updated_amenity.name == 'Super WiFi'
        assert updated_amenity.updated_at != old_updated_at
        print("UPDATE AMENITY : OKAY")
    except Exception as e:
        print(f"UPDATE AMENITY : ÉCHEC ({e})")
        
    # --- Test 4 : Mise à jour du Lieu (PUT) ---
    try:
        place_before = place_facade.get_place(place_id)
        old_updated_at = place_before.updated_at
        
        updated_place = place_facade.update_place(place_id, {'price': 200, 'latitude': 45.77})
        
        assert updated_place.price == 200
        assert updated_place.latitude == 45.77
        assert updated_place.updated_at != old_updated_at
        print("UPDATE PLACE : OKAY")
    except Exception as e:
        print(f"UPDATE PLACE : ÉCHEC ({e})")
        
    # --- Test 5 : Mise à jour de l'Évaluation (PUT) ---
    try:
        review_before = review_facade.get_review(review_id)
        old_updated_at = review_before.updated_at
        
        updated_review = review_facade.update_review(review_id, {'text': 'Très bon séjour, 4/5.', 'rating': 4})
        
        assert updated_review.rating == 4
        assert updated_review.updated_at != old_updated_at
        print("UPDATE REVIEW : OKAY")
    except Exception as e:
        print(f"UPDATE REVIEW : ÉCHEC ({e})")

    # --- Test 6 : Suppression de l'Évaluation (DELETE) ---
    try:
        place = place_facade.get_place(place_id)
        initial_reviews_count = len(place.reviews)
        
        review_facade.delete_review(review_id)
        
        assert review_facade.get_review(review_id) is None
        assert len(place_facade.get_place(place_id).reviews) == initial_reviews_count - 1
        print("DELETE REVIEW : OKAY")
    except Exception as e:
        print(f"DELETE REVIEW : ÉCHEC ({e})")


if __name__ == '__main__':
    print("--- 🎬 Démarrage de la simulation des CRUD (tests unitaires) ---")
    run_simulation()
    print("--- 🏁 Fin de la simulation ---")