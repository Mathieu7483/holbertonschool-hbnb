from app.models.basemodel import BaseModel


class User(BaseModel):
    def __init__(self, id : str, first_name : str, last_name : str, email : str, is_admin :bool, created_at, updated_at):
        super().__init__()
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.created_at = created_at
        self.updated_at = updated_at
        self.users = [] #list to store related users

    def add_user(self, user):
        """Add a user to the place."""
        self.users.append(user)
    
    @property
    def validate(self):
        """Validate the attributes of the User instance."""
        if not isinstance(self.id, str):
            raise TypeError("id must be a string")
        if not isinstance(self.first_name, str):
            raise TypeError("first_name must be a string")
        if not isinstance(self.last_name, str):
            raise TypeError("last_name must be a string")
        if not isinstance(self.email, str):
            raise TypeError("email must be a string")
        if not isinstance(self.is_admin, bool):
            raise TypeError("is_admin must be a boolean")
        if not isinstance(self.created_at, str):
            raise TypeError("created_at must be a string")
        if not isinstance(self.updated_at, str):
            raise TypeError("updated_at must be a string")
        if "@" not in self.email or "." not in self.email:
            raise ValueError("email must be a valid email address")
        if len(self.first_name) == 0:
            raise ValueError("first_name cannot be empty")
        if len(self.last_name) == 0:
            raise ValueError("last_name cannot be empty")
        if len(self.id) == 0:
            raise ValueError("id cannot be empty")
        if len(self.first_name) > 50:
            raise ValueError("first_name cannot be longer than 50 characters")
        if len(self.last_name) > 50:
            raise ValueError("last_name cannot be longer than 50 characters")
        if len(self.email) > 100:
            raise ValueError("email cannot be longer than 100 characters")
        return True
    def __str__(self):
        return f"User(id={self.id}, first_name={self.first_name}, last_name={self.last_name})"
    def to_dict(self):
        """Return a dictionary representation of the User instance."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
    def update(self, data):
        """Update the attributes of the User instance based on the provided dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.validate  # Validate the updated attributes
        self.save()  # Update the updated_at timestamp
        return self