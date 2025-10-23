import uuid
from datetime import datetime

class BaseModel:
    """
    Base class for all models, providing core attributes (id, created_at, updated_at)
    and methods (save, update, to_dict).
    """

    # Core attributes are set to None by default, allowing the Facade to pass existing values.
    def __init__(self, **kwargs):

        now = datetime.now().isoformat()

        # Attributes with default values if not provided
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = kwargs.get('created_at', now)
        self.updated_at = kwargs.get('updated_at', now)

    def save(self):
        """Update the updated_at timestamp whenever the object is modified."""
        self.updated_at = datetime.now().isoformat()

    def update(self, data: dict):
        """
        Updates the mutable attributes of the object based on the provided dictionary.
        This method protects critical attributes (ID, creation date) from being modified.
        """

        # Critical: List of attributes that must be protected against external modification.
        protected_keys = ['id', 'created_at', 'updated_at']

        for key, value in data.items():
            # Only update the attribute if it exists and is not in the protected list.
            if hasattr(self, key) and key not in protected_keys:
                setattr(self, key, value)

        # Update the timestamp, proving the object has changed. Crucial for tests.
        self.save()

    def to_dict(self):
        """Return a dictionary representation of the object."""
        result = self.__dict__.copy()
        return result
