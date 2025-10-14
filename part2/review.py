#!/usr/bin/python3


from base_model import Base_Model


class review(Base_Model):
    def __init__(self, text, rating, place, user):
        super().__init__()
        asser 1 <= rating <= 5
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
