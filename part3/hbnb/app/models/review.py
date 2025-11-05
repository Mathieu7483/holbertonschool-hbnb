from app.models.basemodel import BaseModel
from app.extensions import db

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)


    def to_dict(self):
        """Sérialisation complète de la Review, en utilisant la sérialisation imbriquée pour les objets liés."""
        data = super().to_dict()
        data.update({
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id,
        })

        if self.user:
            # Assuming User model has a simple to_dict() or to_nested_dict() for the nested output
            data['user'] = self.user.to_dict() 
            
        if hasattr(self, 'place') and self.place: 
            data['place'] = self.place.to_nested_dict() 
            
        return data