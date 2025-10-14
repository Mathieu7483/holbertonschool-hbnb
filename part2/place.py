#!/usr/bin/python3


from base_model import Base_Model


class place(Base_Model):
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
