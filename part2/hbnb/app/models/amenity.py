from app.models.basemodel import BaseModel
# from typing import Optional # Omitted as requested

class Amenity(BaseModel):
    def __init__(self, id=None, name=None, created_at=None, updated_at=None):
        
        # Call the parent constructor to handle ID, created_at, and updated_at.
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        
        # Specific attribute for Amenity
        self.name = name
        
        self.validate()
        
    # CRUCIAL: Add the overloaded update method for PUT operations.
    def update(self, data: dict):
        """
        Overloads BaseModel.update to apply data changes, then re-validate the object.
        """
        super().update(data)
        self.validate()
        
    def validate(self):
        """Validate the attributes of the Amenity instance."""
        if not self.name or len(str(self.name)) > 50:
            raise ValueError("Invalid or too long name for amenity")
        return True
        
    def to_dict(self):
        """Return a dictionary representation of the Amenity instance."""
        amenity_dict = super().to_dict()
        amenity_dict.update({"name": self.name})
        return amenity_dict