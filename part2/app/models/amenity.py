from app.models.base import BaseModel


class Amenity(BaseModel):
    def __init__(self,name):
        super().__init__()
        assert len(name) <= 50
        self.name = name

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "name": self.name
        })
        return base
