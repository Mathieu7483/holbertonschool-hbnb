#!/usr/bin/python3


from base_model import Base_Model


class amenity(Base_Model):
    def __init__(self,name):
        super().__init__()
        assert len(name) <= 50
        self.name = name
