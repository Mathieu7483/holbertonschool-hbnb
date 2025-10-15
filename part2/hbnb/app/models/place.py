from app.models.basemodel import BaseModel
from app.models.user import User


class Place(BaseModel):
    def __init__(self, id, title, description, price, latitude, longitude, owner, created_at, updated_at):
        super().__init__()
        self.id = id
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.created_at = created_at
        self.updated_at = updated_at
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    def add_review(self, review):
        """Add a review to the place."""
        from app.models.review import Review
        if not isinstance(review, Review):
            raise TypeError("review must be an instance of the Review class.")
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        from app.models.amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise TypeError("amenity must be an instance of the Amenity class.")
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    @property
    def validate(self):
        """Validate the attributes of the Place instance."""
        if not isinstance(self.id, str):
            raise TypeError("id must be a string")
        if not isinstance(self.title, str):
            raise TypeError("title must be a string")
        if not isinstance(self.description, str):
            raise TypeError("description must be a string")
        if not isinstance(self.price, (int, float)):
            raise TypeError("price must be a positive number")
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
            raise ValueError("price must be positive")
        if not (-90 <= self.latitude <= 90):
            raise ValueError("latitude must be between -90 and 90")
        if not (-180 <= self.longitude <= 180):
            raise ValueError("longitude must be between -180 and 180")
        return True

    def __str__(self):
        return f"Place(id={self.id}, title={self.title}, owner={self.owner})"

    def to_dict(self):
        """Return a dictionary representation of the Place instance."""
        place_dict = super().to_dict()
        place_dict.update({
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": self.owner.to_dict() if self.owner else None,
            "amenities": [amenity.to_dict() for amenity in self.amenities],
        })
        return place_dict

    def update(self, data):
        """Update the attributes of the Place instance based on the provided dictionary."""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'owner']:
                setattr(self, key, value)
        self.validate  # Validate the updated attributes
        self.save()  # Update the updated_at timestamp
        return self