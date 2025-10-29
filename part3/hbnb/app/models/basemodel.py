import uuid
from datetime import datetime
from app.extensions import db

class BaseModel(db.Model):
    """
    Base class for all models, providing core attributes (id, created_at, updated_at)
    and methods (save, update, to_dict).
    """
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,default=datetime.utcnow, onupdate=datetime.utcnow)

    # Core attributes are set to None by default, allowing the Facade to pass existing values.
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
