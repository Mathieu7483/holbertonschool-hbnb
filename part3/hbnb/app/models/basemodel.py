import uuid
from datetime import datetime
from app.extensions import db

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """save the object and commit it."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """delete on the database."""
        db.session.delete(self)
        db.session.commit()

    def update(self, data: dict):
        """update the attributes."""
        for key, value in data.items():
            # verification if attribute is on the model
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit() # Commit the changes

    def to_dict(self):
        """Serialize the data"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }