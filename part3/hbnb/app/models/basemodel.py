import uuid
from datetime import datetime
from app.extensions import db

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Sauvegarde l'objet dans la session et commit."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Supprime l'objet de la base de données."""
        db.session.delete(self)
        db.session.commit()

    def update(self, data: dict):
        """Met à jour les attributs à partir d'un dictionnaire."""
        for key, value in data.items():
            # Vérifie si l'attribut existe sur le modèle avant de l'assigner
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit() # Commit les changements

    def to_dict(self):
        """Sérialise les champs de base."""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }