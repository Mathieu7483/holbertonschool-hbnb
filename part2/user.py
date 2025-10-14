#!/usr/bin/python3


from base_model import Base_Model


class user(Base_Model):
    def __init__(self, first_name, last_name, email, is_admin=False):
        supper().__init__()
	assert len(first_name) <= 50
	assert len(last_name) <= 50
        assert '@' in email and '.' in email
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
