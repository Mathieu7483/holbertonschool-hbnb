from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # USER
    def create_user(self, data):
        user = User(**data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        self.user_repo.update(user_id, data)
        return self.user_repo.get(user_id)

    # PLACE
    def create_place(self, data):
        owner = self.user_repo.get(data['owner_id'])
        if not owner:
            return None
        place = Place(
            title=data['title'],
            description=data.get('description', ''),
            price=data['price'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            owner=owner
        )
        self.place_repo.add(place)
        owner.places.append(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        self.place_repo.update(place_id, data)
        return self.place_repo.get(place_id)

    # REVIEW
    def create_review(self, data):
        user = self.user_repo.get(data['user_id'])
        place = self.place_repo.get(data['place_id'])
        if not user or not place:
            return None
        review = Review(
            text=data['text'],
            rating=data['rating'],
            place=place,
            user=user
        )
        self.review_repo.add(review)
        place.add_review(review)
        user.reviews.append(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, data):
        self.review_repo.update(review_id, data)
        return self.review_repo.get(review_id)

    # AMENITY
    def create_amenity(self, data):
        amenity = Amenity(**data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        self.amenity_repo.update(amenity_id, data)
        return self.amenity_repo.get(amenity_id)

    def link_amenity_to_place(self, amenity_id, place_id):
        amenity = self.amenity_repo.get(amenity_id)
        place = self.place_repo.get(place_id)
        if not amenity or not place:
            return None
        place.add_amenity(amenity)
        return place
