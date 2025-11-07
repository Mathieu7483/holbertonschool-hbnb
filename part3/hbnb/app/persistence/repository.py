from abc import ABC, abstractmethod
from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from typing import Any

__all__ = ["User", "Place", "Amenity", "Review"]

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)
    

class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_or_id: Any) -> bool:
        """
        Deletes an object. Accepts either the ID (string) or the full ORM instance.
        This fixes the 'ProgrammingError' encountered when the cleanup logic 
        (or DELETE API route) passed the ORM object instead of just its ID.
        """
        obj_to_delete = None

        if isinstance(obj_or_id, str):
            # If it's an ID, we fetch the object first
            obj_to_delete = self.get(obj_or_id)
        elif hasattr(obj_or_id, 'id'):
            # If it's an ORM instance (it has an 'id' attribute), use it directly
            obj_to_delete = obj_or_id
        
        if obj_to_delete:
            try:
                db.session.delete(obj_to_delete)
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                print(f"Error during deletion: {e}")
                return False
        return False

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).first()