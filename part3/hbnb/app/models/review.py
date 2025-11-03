from app.models.basemodel import BaseModel
from app.extensions import db

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # Clés étrangères (le type doit être cohérent avec l'ID du BaseModel)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # --- SUPPRESSION DE __init__, validate, update ---

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id,
        })
        # Optionnel: inclure les objets liés s'ils sont chargés
        if self.user:
            data['user'] = self.user.to_dict()
        if hasattr(self, 'place') and self.place: # 'place' existe grâce au backref
             data['place'] = self.place.to_dict()
        return data