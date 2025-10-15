from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def add(self, obj): pass

    @abstractmethod
    def get(self, obj_id): pass

    @abstractmethod
    def get_all(self): pass

    @abstractmethod
    def update(self, obj_id, data): pass

    @abstractmethod
    def delete(self, obj_id): pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value): pass

class InMemoryRepository:
    def __init__(self):
        self.storage = {}

    def add(self, obj):
        self.storage[obj.id] = obj

    def get(self, obj_id):
        return self.storage.get(obj_id)

    def get_all(self):
        return list(self.storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def get_by_attribute(self, attr_name, value):
        for obj in self.storage.values():
            if hasattr(obj, attr_name) and getattr(obj, attr_name) == value:
                return obj
        return None
