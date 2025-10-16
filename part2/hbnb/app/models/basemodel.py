import uuid
from datetime import datetime

class BaseModel:
    """
    Base class for all models, providing core attributes (id, created_at, updated_at)
    and methods (save, update, to_dict).
    """
    
    # Core attributes are set to None by default, allowing the Facade to pass existing values.
    def __init__(self, id=None, created_at=None, updated_at=None):
        
        now = datetime.now().isoformat()
        
        # Initialize attributes, using provided values if available, otherwise generating new ones.
        # This handles both creation (ID is None) and loading (ID is provided).
        self.id = id if id is not None else str(uuid.uuid4())
        self.created_at = created_at if created_at is not None else now
        self.updated_at = updated_at if updated_at is not None else now

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
        return {
            "id": self.id, 
            "created_at": self.created_at, 
            "updated_at": self.updated_at
        }