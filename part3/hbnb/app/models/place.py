from app.models.basemodel import BaseModel
from app.models.user import User
from app.extensions import db
# from typing import Optional, List # Omitted as requested

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    latitude = db.Column(db.Float, nullable=False, default=0.0)
    longitude = db.Column(db.Float, nullable=False, default=0.0)
    owner_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
   


    def __init__(self, title=None, description=None, price=0, latitude=0.0, longitude=0.0, owner=None, amenities=None, **kwargs):

        # Call the parent constructor to handle ID, created_at, and updated_at.
        super().__init__(**kwargs)

        # Specific attributes for Place
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

        # Relationship lists (stores object references)
        self.amenities = amenities if amenities is not None else []
        self.reviews = []

        self.validate()

    # CRUCIAL: Add the overloaded update method for PUT operations.
    def update(self, data: dict):
        """
        Overloads BaseModel.update to apply data changes, then re-validate the object.
        """
        super().update(data)
        self.validate()

    def validate(self):
        """Validate the attributes of the Place instance."""
        if not isinstance(self.owner, User) or self.price < 0:
            raise ValueError("Invalid owner or price must be non-negative")
        if not (-90 <= self.latitude <= 90):
             raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= self.longitude <= 180):
             raise ValueError("Longitude must be between -180 and 180")
        return True

    def to_dict(self):
        """Return a dictionary representation of the Place instance."""
        # start with the base dictionary
        place_dict = super().to_dict()
        
        # add Place-specific fields
        place_dict.update({
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,  
            "owner_id": self.owner_id,        
            "owner": self.owner.to_dict() if self.owner else None,
            "amenities": [a.to_dict() for a in self.amenities] if self.amenities else [],
            "reviews_count": len(self.reviews) if self.reviews else 0
        })
        return place_dict