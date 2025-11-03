from app.models.basemodel import BaseModel
from app.extensions import db
# from app.models.associations import place_amenity # si dans un fichier séparé

# Table d'association
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # --- RELATIONS ---
    reviews = db.relationship('Review', backref='place', cascade="all, delete-orphan", lazy=True)
    amenities = db.relationship('Amenity', secondary=place_amenity, backref=db.backref('places', lazy='dynamic'))

    # --- SUPPRESSION DE __init__, validate, update ---

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "owner": self.owner.to_dict() if self.owner else None,
            "amenities": [a.to_dict() for a in self.amenities],
            "reviews_count": len(self.reviews) if self.reviews else 0
        })
        return data