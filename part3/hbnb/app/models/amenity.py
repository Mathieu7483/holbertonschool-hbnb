from app.models.basemodel import BaseModel
from app.extensions import db

class Amenity(BaseModel):
    __tablename__ = 'amenities'
    name = db.Column(db.String(128), unique=True, nullable=False)

    # --- SUPPRESSION DE __init__, validate, update ---
    
    def to_dict(self):
        data = super().to_dict()
        data.update({"name": self.name})
        return data