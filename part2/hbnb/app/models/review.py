from app.models.basemodel import BaseModel
from app.models.place import Place
from app.models.user import User

class Review(BaseModel):
    def __init__(self, id, text, rating, place, user, created_at, updated_at):
        super().__init__()
        self.id = id
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        self.created_at = created_at
        self.updated_at =   updated_at
        self.reviews = [] #list to store related reviews

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def to_dict(self):
        """Return a dictionary representation of the Review instance."""
        review_dict = super().to_dict()
        review_dict.update({
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place.id if self.place else None,
            "user_id": self.user.id if self.user else None
        })
        return review_dict

    @property
    def validate(self):
        """Validate the attributes of the Review instance."""
        if not isinstance(self.id, str):
            raise TypeError("id must be a string")
        if not isinstance(self.text, str):
            raise TypeError("text must be a string")
        if not isinstance(self.rating, int):
            raise TypeError("rating must be an integer")
        if not isinstance(self.place, Place):
            raise TypeError("place must be a Place instance")
        if not isinstance(self.user, User):
            raise TypeError("user must be a User instance")
        if not isinstance(self.created_at, str):
            raise TypeError("created_at must be a string")
        if not isinstance(self.updated_at, str):
            raise TypeError("updated_at must be a string")
        if len(self.id) == 0:
            raise ValueError("id cannot be empty")
        if len(self.text) == 0:
            raise ValueError("text cannot be empty")
        if not (1 <= self.rating <= 5):
            raise ValueError("rating must be between 1 and 5")
        return True