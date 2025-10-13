from hbnb.app.models.basemodel import BaseModel


class Amenity(BaseModel):
    def __init__(self, id, name, created_at, updated_at):
        super().__init__()
        self.id = id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at
        self.amenities = [] #list to store related amenities
    
    def add_amenity(self, amenity):
        """Add an amenity to a place"""
        self.amenities.append(amenity)