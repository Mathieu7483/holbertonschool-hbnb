from app.models.basemodel import BaseModel
from app.models.user import User
# from typing import Optional, List # Omitted as requested

class Place(BaseModel):
    def __init__(self, id=None, title=None, description=None, price=0, latitude=0.0, longitude=0.0, owner=None, created_at=None, updated_at=None):
        
        # Call the parent constructor to handle ID, created_at, and updated_at.
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        
        # Specific attributes for Place
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner 
        
        # Relationship lists (stores object references)
        self.amenities = []
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
        place_dict = super().to_dict()
        place_dict.update({
            "title": self.title, 
            "price": self.price,
            # Note: We return the owner object's dictionary representation
            "owner": self.owner.to_dict() if self.owner else None,
            # We only return the list of amenities as dicts, not the full objects
            "amenities": [a.to_dict() for a in self.amenities], 
            # Useful for API endpoints: count the number of reviews
            "reviews_count": len(self.reviews) 
        })
        return place_dict