from hbnb.app.models.basemodel import BaseModel

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