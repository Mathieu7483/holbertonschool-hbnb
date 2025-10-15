from app.models.basemodel import BaseModel


class Amenity(BaseModel):
    def __init__(self, id, name, created_at, updated_at):
        super().__init__()
        self.id = id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at

    @property
    def validate(self):
        """Validate the attributes of the Amenity instance."""
        if not isinstance(self.id, str):
            raise TypeError("id must be a string")
        if not isinstance(self.name, str):
            raise TypeError("name must be a string")
        if not isinstance(self.created_at, str):
            raise TypeError("created_at must be a string")
        if not isinstance(self.updated_at, str):
            raise TypeError("updated_at must be a string")
        if len(self.id) == 0:
            raise ValueError("id cannot be empty")
        if len(self.name) == 0:
            raise ValueError("name cannot be empty")
        if len(self.name) > 50:
            raise ValueError("name cannot be longer than 50 characters")
        return True

    def __str__(self):
        return f"Amenity(id={self.id}, name={self.name})"

    def to_dict(self):
        """Return a dictionary representation of the Amenity instance."""
        amenity_dict = super().to_dict()
        amenity_dict.update({
            "name": self.name,
        })
        return amenity_dict

    def update(self, data):
        """Update the attributes of the Amenity instance based on the provided dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.validate  # Validate the updated attributes
        self.save()  # Update the updated_at timestamp
        return self