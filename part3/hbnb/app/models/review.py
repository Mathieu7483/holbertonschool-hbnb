from app.models.basemodel import BaseModel
from app.extensions import db

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Add unique constraint
    __table_args__ = (
        db.UniqueConstraint('user_id', 'place_id', name='unique_user_place_review'),
    )

    def to_dict(self):
        """Complete serialization of the review"""
        data = super().to_dict()
        data.update({
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id,
        })

        # Use nested dict to avoid exposing sensitive user data
        if self.user:
            data['user'] = self.user.to_nested_dict()
            
        if hasattr(self, 'place') and self.place: 
            data['place'] = self.place.to_nested_dict()
            
        return data

    def __repr__(self):
        return f"<Review {self.id} - Rating: {self.rating}>"