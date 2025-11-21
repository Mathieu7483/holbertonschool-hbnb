from app.models.basemodel import BaseModel
from app.extensions import db

place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    reviews = db.relationship('Review', backref='place', cascade="all, delete-orphan", lazy='selectin')
    amenities = db.relationship('Amenity', secondary=place_amenity, backref=db.backref('places', lazy='dynamic'), lazy='selectin')

    def to_nested_dict(self):
        return {
            "id": self.id,
            "title": self.title,
        }

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
        })
        
        if hasattr(self, 'owner') and self.owner: 
            data["owner"] = self.owner.to_nested_dict()
        
        # CORRECTION : Sérialisation complète de la relation Many-to-Many
        if hasattr(self, 'amenities') and self.amenities:
            data["amenities"] = [a.to_dict() for a in self.amenities]
        else:
            data["amenities"] = []
        
        return data

    def __repr__(self):
        return f"<Place {self.title}>"