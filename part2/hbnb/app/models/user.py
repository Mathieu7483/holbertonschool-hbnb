from app.models.basemodel import BaseModel
# from typing import Optional # Omitted as requested

class User(BaseModel):
    def __init__(self, first_name=None, last_name=None, email=None, is_admin=False, **kwargs):

        # Call the parent constructor to handle ID, created_at, and updated_at.
        super().__init__(**kwargs)

        # Specific attributes for User
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        self.validate()

    # CRUCIAL: Add the overloaded update method for PUT operations.
    def update(self, data: dict):
        """
        Overloads BaseModel.update to apply data changes, then re-validate the object.
        """
        super().update(data)
        self.validate()

    def validate(self):
        """Validate the attributes of the User instance."""
        if not self.first_name or not self.email:
            raise ValueError("First name or email missing")
        if "@" not in str(self.email):
             raise ValueError("Invalid email format")
        return True

    def to_dict(self):
        """Return a dictionary representation of the User instance."""
        user_dict = super().to_dict()
        user_dict.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        })
        return user_dict