from abc import ABC, abstractmethod
from typing import Dict, List, Optional


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
    """Single shared repository for all models"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Singleton pattern to ensure only one instance exists"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize storage only once"""
        if not InMemoryRepository._initialized:
            # Separate storage by entity type
            self._storage: Dict[str, Dict[str, object]] = {
                'User': {},
                'Place': {},
                'Review': {},
                'Amenity': {}
            }
            InMemoryRepository._initialized = True
    
    def _get_entity_type(self, obj):
        """Determine entity type from class name"""
        return obj.__class__.__name__
    
    def add(self, obj):
        """Add an object to the repository"""
        entity_type = self._get_entity_type(obj)
        if entity_type not in self._storage:
            self._storage[entity_type] = {}
        self._storage[entity_type][obj.id] = obj
    
    def get(self, obj_id, entity_type=None):
        """
        Retrieve an object by ID
        If entity_type is not provided, searches all types
        """
        if entity_type:
            return self._storage.get(entity_type, {}).get(obj_id)
        
        # Search across all types
        for storage in self._storage.values():
            if obj_id in storage:
                return storage[obj_id]
        return None
    
    def get_all(self, entity_type=None):
        """
        Retrieve all objects of a specific type
        If entity_type is not provided, returns all objects
        """
        if entity_type:
            return list(self._storage.get(entity_type, {}).values())
        
        # Return all objects from all types
        all_objects = []
        for storage in self._storage.values():
            all_objects.extend(storage.values())
        return all_objects
    
    def update(self, obj_id, data, entity_type=None):
        """Update an object"""
        obj = self.get(obj_id, entity_type)
        if obj:
            obj.update(data)
    
    def delete(self, obj_id, entity_type=None):
        """Delete an object"""
        if entity_type:
            if obj_id in self._storage.get(entity_type, {}):
                del self._storage[entity_type][obj_id]
                return True
        else:
            # Search across all types
            for storage in self._storage.values():
                if obj_id in storage:
                    del storage[obj_id]
                    return True
        return False
    
    def get_by_attribute(self, attr_name, attr_value, entity_type=None):
        """Find an object by attribute"""
        objects = self.get_all(entity_type)
        return next((obj for obj in objects if getattr(obj, attr_name, None) == attr_value), None)
    
    def get_all_by_attribute(self, attr_name, attr_value, entity_type=None):
        """Find all objects matching an attribute"""
        objects = self.get_all(entity_type)
        return [obj for obj in objects if getattr(obj, attr_name, None) == attr_value]


# Global singleton instance
repo = InMemoryRepository()


