from app.models.basemodel import BaseModel
from app.extensions import db

class Amenity(BaseModel):
    __tablename__ = 'amenities'
    
    name = db.Column(db.String(128), unique=True, nullable=False, index=True)

    def to_dict(self):
        """Serialization of Amenity"""
        data = super().to_dict()
        data.update({"name": self.name})
        return data

    def __repr__(self):
        return f"<Amenity {self.name}>"