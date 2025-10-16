from app.models.basemodel import BaseModel
from app.models.place import Place
from app.models.user import User

class Review(BaseModel):
    
    # 1. Correct __init__ signature to accept arguments and pass them to the parent.
    def __init__(self, id=None, text=None, rating=None, place=None, user=None, created_at=None, updated_at=None):
        
        # Call the parent constructor to handle ID, created_at, and updated_at.
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        
        # Specific attributes for Review
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        
        # Call validation upon creation
        self.validate()

    # 2. Add the overloaded update method. CRUCIAL for passing UPDATE tests.
    def update(self, data: dict):
        """
        Overloads BaseModel.update to apply data changes, then re-validate the object.
        """
        # Apply changes and update the 'updated_at' timestamp via BaseModel
        super().update(data) 
        
        # Re-validate the object's integrity
        self.validate()      

    def to_dict(self):
        """Return a dictionary representation of the Review instance."""
        review_dict = super().to_dict()
        review_dict.update({
            "text": self.text,
            "rating": self.rating,
            # Ensure safe access to linked object IDs
            "place_id": self.place.id if self.place else None,
            "user_id": self.user.id if self.user else None
        })
        return review_dict

    # 3. Standard validation method (removed @property)
    def validate(self):
        """Validate the attributes of the Review instance."""
        
        # Check instance types for relationships (essential business logic)
        if not isinstance(self.place, Place) or not isinstance(self.user, User):
             raise TypeError("place and user must be instances of Place and User")
             
        if not isinstance(self.text, str):
            raise TypeError("text must be a string")
        if not isinstance(self.rating, int):
            raise TypeError("rating must be an integer")
            
        if len(self.text) == 0:
            raise ValueError("text cannot be empty")
        if not (1 <= self.rating <= 5):
            raise ValueError("rating must be between 1 and 5")
            
        return True
    