from app.models.base import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        assert len(title) <= 100
        assert price > 0
        assert -90.0 <= latitude <= 90.0
        assert -180.0 <= longitude <= 180.0
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner= owner
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
            "owner": self.owner.to_dict() if self.owner else None,
            "amenities": [amenity.to_dict() for amenity in self.amenities]
        })
        return base
