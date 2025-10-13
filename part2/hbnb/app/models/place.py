from hbnb.app.models.basemodel import BaseModel
from hbnb.app.models.user import User
from hbnb.app.models.amenity import Amenity


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    @property
    def validate(self):
        """Validate the attributes of the Place instance."""
        if not isinstance(self.title, str):
            raise TypeError("title must be a string")
        if not isinstance(self.description, str):
            raise TypeError("description must be a string")
        if not isinstance(self.price, (int, float)):
            raise TypeError("price must be a number")
        if not isinstance(self.latitude, (int, float)):
            raise TypeError("latitude must be a number")
        if not isinstance(self.longitude, (int, float)):
            raise TypeError("longitude must be a number")
        if not isinstance(self.owner, User):
            raise TypeError("owner must be a User instance")
        if len(self.title) == 0:
            raise ValueError("title cannot be empty")
        if len(self.title) > 100:
            raise ValueError("title cannot be longer than 100 characters")
        if self.price < 0:
            raise ValueError("price must positive")
        if not (-90 <= self.latitude <= 90):
            raise ValueError("latitude must be between -90 and 90")
        if not (-180 <= self.longitude <= 180):
            raise ValueError("longitude must be between -180 and 180")
        return True